import os
from agency_swarm.tools import BaseTool
from pydantic import Field
from google import genai
from ad_creator_agent.tools.utils import (
    IMAGES_DIR,
    validate_num_variants,
    get_api_key,
    extract_image_from_response,
    process_variant_result,
    run_parallel_variants,
    create_result_summary,
    create_image_urls,
    compress_image_for_base64,
)
from typing import Literal, Optional

# Constants
MODEL_NAME = "gemini-2.5-flash-image-preview"


class GenerateImage(BaseTool):
    """
    Generate images using Google's Gemini 2.5 Flash Image (Nano Banana) model.
    """

    prompt: str = Field(
        ...,
        description="The text prompt describing the image to generate. Start with 'Generate an image of' and describe the image in detail.",
    )

    file_name: str = Field(
        ...,
        description="The name for the generated image file (without extension)",
    )

    num_variants: Optional[int] = Field(
        default=1,
        description="Number of image variants to generate (1-4, default is 1)",
    )

    aspect_ratio: Optional[
        Literal["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]
    ] = Field(
        default="1:1",
        description="The aspect ratio of the generated image (default is 1:1)",
    )

    def run(self):
        try:
            # Validate num_variants
            validation_error = validate_num_variants(self.num_variants)
            if validation_error:
                return validation_error

            # Get API key from environment
            api_key, api_error = get_api_key()
            if api_error:
                return api_error

            print(f"Generating image with prompt: {self.prompt}")
            print(f"Generating {self.num_variants} variant(s)")

            # Initialize the Google AI client
            client = genai.Client(api_key=api_key)

            # Create output directory if it doesn't exist
            os.makedirs(IMAGES_DIR, exist_ok=True)

            def generate_single_variant(variant_num):
                """Generate a single image variant"""
                try:
                    print(f"Generating variant {variant_num}/{self.num_variants}")

                    # Generate image using Gemini 2.5 Flash Image
                    response = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=[self.prompt],
                        config=genai.types.GenerateContentConfig(
                            image_config=genai.types.ImageConfig(
                                aspect_ratio=self.aspect_ratio,
                            )
                        ),
                    )

                    # Extract the generated image
                    image, text_output = extract_image_from_response(response)

                    if image is None:
                        print(
                            f"Warning: No image was generated for variant {variant_num}. Text output: {text_output}"
                        )
                        return None

                    # Process variant result
                    return process_variant_result(
                        variant_num,
                        image,
                        self.file_name,
                        self.num_variants,
                        compress_image_for_base64,
                    )
                except Exception as e:
                    print(f"Error generating variant {variant_num}: {str(e)}")
                    return None

            # Run variants in parallel
            results = run_parallel_variants(generate_single_variant, self.num_variants)

            if not results:
                return "Error: No variants were successfully generated."

            # Create and print result summary
            result_text = create_result_summary(results, "Generated")
            print(result_text)

            # Return array of image URLs
            return create_image_urls(results, include_text_labels=True)

        except Exception as e:
            return f"Error generating image: {str(e)}"


# Create alias for Agency Swarm tool loading
generate_image = GenerateImage

if __name__ == "__main__":
    # Example usage with Google Gemini 2.5 Flash Image
    tool = GenerateImage(
        prompt="Generate an image of a clean, modern black laptop computer that is placed closed on a white marble surface with soft natural lighting, professional product photography style, shallow depth of field, premium aesthetic, commercial advertisement quality. No logo images. No text",
        file_name="test_image",
        aspect_ratio="16:9",
    )
    result = tool.run()
    print(result)

    # tool = GenerateImage(
    #     prompt="Generate a round logo for a laptop brand called 'OmegaTech'. Ensure the logo is simple, modern, and recognizable. Use black and red color scheme for the logo.",
    #     file_name="logo_image",
    #     num_variants=2
    # )
    # result = tool.run()
    # print(result)
