from agency_swarm.tools import BaseTool
from pydantic import Field
import os
from dotenv import load_dotenv
from typing import Literal
import json
load_dotenv()

class OnboardingTool(BaseTool):
    """
    Takes the required inputs to customize an agent to help the user to onboard and start using it immidiately.
    """
    agent_name: str = Field(..., description="Name of your agent visible to the user.")
    agent_description: str = Field(..., description="Description of your agent visible to the user.")
    business_overview: str = Field(..., description="Brief business overview of the client for better results.")
    files: str = Field(
        ...,
        description="Files to upload as knowledge to the agent.",
        json_schema_extra={
        "x-file-upload-path": "./rag_agent/files",           # standard JSON Schema
        },
    )
    files_description: str = Field(..., description="Description of the content of the files..")
    output_format: str = Field(..., description="Desired output format of the agent.")
    additional_notes: str = Field(..., description="Any additional notes for the agent to go into prompt.")
    

    def run(self):
        """
        Saves the configuration as a Python file with a config object
        """
        import json

        tool_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(tool_dir, "onboarding_config.py")

        config = self.model_dump()

        try:
            # Generate Python code with the config as a dictionary
            python_code = f"# Auto-generated onboarding configuration\n\nconfig = {json.dumps(config, indent=4)}\n"
            
            with open(config_path, "w", encoding="utf-8") as f:
                f.write(python_code)
            return f"Configuration saved at: {config_path}\n\nYou can now import it with:\nfrom onboarding_config import config"
        except Exception as e:
            return f"Error writing config file: {str(e)}"

if __name__ == "__main__":
    # Test with some sample data
    # tool = OnboardingTool(
    #     agent_name="Onboarding Agent",
    #     agent_description="Helps new clients get set up smoothly.",
    #     business_overview="A brief business overview of the client for better results.",
    #     files="/path/to/firebase/storage/files",
    #     files_description="Contains onboarding templates and example docs.",
    #     output_format="respond as friendly and helpful as possible",
    #     additional_notes="No sensitive info in files."
    # )
    # print(tool.run())

    # generate schema
    schema = OnboardingTool.model_json_schema()
		path = os.path.realpath(os.path.abspath("./onboarding_tool_schema.json"))
    with open(path, "w") as f:
        json.dump(schema, f, indent=4)