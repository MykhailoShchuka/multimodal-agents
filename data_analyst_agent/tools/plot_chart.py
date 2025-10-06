import io
import base64
from typing import Literal, Optional

from agency_swarm.tools import BaseTool
from pydantic import Field

# Use non-interactive backend for headless environments
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image  # noqa: F401 imported for type consistency in environments, not required at runtime


class PlotChart(BaseTool):
    """Create a simple chart using matplotlib and return the image as output."""

    title: str = Field(..., description="Title displayed at the top of the chart")
    x_values: list[float] = Field(..., description="X-axis values")
    y_values: list[float] = Field(..., description="Y-axis values, same length as x_values")
    chart_type: Literal["line", "bar", "scatter"] = Field(
        default="line", description="Type of chart to render"
    )
    file_name: str = Field(
        ..., description="Base file name for the saved chart (without extension)"
    )
    x_label: Optional[str] = Field(default=None, description="Label for X axis")
    y_label: Optional[str] = Field(default=None, description="Label for Y axis")
    figsize_width: Optional[float] = Field(
        default=8.0, description="Figure width in inches"
    )
    figsize_height: Optional[float] = Field(
        default=5.0, description="Figure height in inches"
    )

    def run(self):
        try:
            if len(self.x_values) != len(self.y_values):
                return "Error: x_values and y_values must have the same length."

            fig, ax = plt.subplots(figsize=(self.figsize_width, self.figsize_height))

            if self.chart_type == "line":
                ax.plot(self.x_values, self.y_values, marker="o")
            elif self.chart_type == "bar":
                ax.bar(self.x_values, self.y_values)
            elif self.chart_type == "scatter":
                ax.scatter(self.x_values, self.y_values)
            else:
                return f"Error: Unsupported chart_type '{self.chart_type}'."

            if self.x_label:
                ax.set_xlabel(self.x_label)
            if self.y_label:
                ax.set_ylabel(self.y_label)

            ax.set_title(self.title)
            ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
            fig.tight_layout()

            # Render to in-memory PNG buffer (no disk write)
            buffer = io.BytesIO()
            fig.savefig(buffer, format="png")
            plt.close(fig)
            buffer.seek(0)
            image_b64 = base64.b64encode(buffer.getvalue()).decode()

            import os
            import time
            screenshots_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "screenshots"))
            os.makedirs(screenshots_dir, exist_ok=True)

            timestamp = time.strftime("%Y%m%d-%H%M%S")
            filename = f"screenshot_{self.title}_{timestamp}.png"
            save_path = os.path.join(screenshots_dir, filename)
            with open(save_path, "wb") as out_file:
                out_file.write(buffer.getvalue())
            print(save_path)
            return [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}}
            ]

        except Exception as e:
            return f"Error creating plot: {str(e)}"


# Alias for tool auto-loading
plot_chart = PlotChart

if __name__ == "__main__":
    tool = PlotChart(
        title="Test Chart",
        x_values=[1, 2, 3, 4, 5],
        y_values=[1, 2, 3, 4, 5],
        file_name="test_chart"
    )
    print(tool.run())
