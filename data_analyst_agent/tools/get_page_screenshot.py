import base64
from typing import Optional
from urllib.parse import urlparse

from agency_swarm.tools import BaseTool
from pydantic import Field

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import os
import time
# Add the tools directory to Python path for imports
tools_dir = os.path.dirname(os.path.abspath(__file__))
if tools_dir not in sys.path:
    sys.path.insert(0, tools_dir)

from utils.session_manager import get_persistent_driver, navigate_persistent_session, restart_session_if_needed  # noqa: E402


class GetPageScreenshot(BaseTool):
    """
    Get a screenshot of a webpage, specifically designed for localhost testing.
    """

    page_url: str = Field(
        ...,
        description="The URL of the page to get a screenshot of (e.g., http://localhost:3000, http://localhost:8080/path)",
    )
    
    wait_seconds: int = Field(
        default=5,
        description="Number of seconds to wait for the page to load before taking screenshot",
    )
    
    full_page: bool = Field(
        default=True,
        description="Whether to capture the full page (True) or just the viewport (False)",
    )
    
    headless: bool = Field(
        default=True,
        description="Whether to run the browser in headless mode",
    )
    
    enable_cookies: bool = Field(
        default=True,
        description="Whether to enable cookies for session persistence",
    )
    
    session_storage_dir: Optional[str] = Field(
        default="./browser_session",
        description="Directory to store session data (cookies, local storage). If not provided, uses temporary directory.",
    )
    
    default_window_width: int = Field(
        default=1920,
        description="Default window width to use for screenshots (prevents squashing)",
    )
    
    default_window_height: int = Field(
        default=1080,
        description="Default window height to use for screenshots (prevents squashing)",
    )

    def run(self):
        
        # Validate URL format
        parsed_url = urlparse(self.page_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return f"Error: Invalid URL format: {self.page_url}. Please provide a complete URL like http://localhost:3000"
        
        # Get persistent driver (stays alive across tool calls)
        driver = get_persistent_driver(
            session_storage_dir=self.session_storage_dir,
            headless=self.headless
        )
        
        # Restart session if it died
        restart_session_if_needed(
            session_storage_dir=self.session_storage_dir,
            headless=self.headless
        )
        
        # Navigate to the page
        navigate_persistent_session(self.page_url)
        
        # Wait for the page to load
        WebDriverWait(driver, self.wait_seconds).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Store original window size to restore later
        original_size = driver.get_window_size()
        
        # Take screenshot
        if self.full_page:
            # For full page screenshots, use a more reliable approach
            # First, ensure we have a reasonable window size
            current_size = driver.get_window_size()
            if current_size['width'] < 800:  # If window is too small, set a reasonable size
                driver.set_window_size(self.default_window_width, self.default_window_height)
            
            # Use JavaScript to get the full page dimensions
            total_width = driver.execute_script("return Math.max(document.body.scrollWidth, document.documentElement.scrollWidth)")
            total_height = driver.execute_script("return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
            
            # Set reasonable limits to prevent extreme window sizes
            max_width = 1920
            max_height = 10800  # 10x 1080p height
            
            # Calculate optimal window size
            window_width = min(total_width, max_width)
            window_height = min(total_height, max_height)
            
            # Only resize if the calculated size is significantly different
            if abs(window_width - current_size['width']) > 100 or abs(window_height - current_size['height']) > 100:
                driver.set_window_size(window_width, window_height)
                # Small delay to let the window resize
                time.sleep(1)

        time.sleep(max(0, int(self.wait_seconds or 0)))
        
        # Take the screenshot
        screenshot = driver.get_screenshot_as_png()
        
        # Always restore original window size to prevent cumulative squashing
        # Use fallback to default size if original size was too small
        restore_width = max(original_size['width'], self.default_window_width)
        restore_height = max(original_size['height'], self.default_window_height)
        driver.set_window_size(restore_width, restore_height)
        
        screenshot_b64 = base64.b64encode(screenshot).decode('utf-8')
        
        # Save to local screenshots directory (temporary change)
        # with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
        #     tmp_file.write(screenshot)
        #     temp_path = tmp_file.name
        #     print(temp_path)

        screenshots_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "screenshots"))
        os.makedirs(screenshots_dir, exist_ok=True)

        safe_host = parsed_url.netloc.replace(":", "-").replace("/", "-") or "localhost"
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"screenshot_{safe_host}_{timestamp}.png"
        save_path = os.path.join(screenshots_dir, filename)
        with open(save_path, "wb") as out_file:
            out_file.write(screenshot)
        print(save_path)
        
        return {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{screenshot_b64}"}}



# Create alias for Agency Swarm tool loading (expects class name = file name)
get_page_screenshot = GetPageScreenshot

if __name__ == "__main__":
    # Example usage with cookie persistence
    tool = GetPageScreenshot(
        page_url="https://app.databox.com/datawall/28ee867d4dd1f00d34a77fec44ba6d7032500dc68e0d07c",
        wait_seconds=5,
        full_page=True,
        headless=True,
        enable_cookies=True,  # Enable cookies for session persistence
        session_storage_dir="./browser_session"  # Same directory as other tools
    )
    result = tool.run()
    print(result)
