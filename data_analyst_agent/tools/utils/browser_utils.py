"""
Shared browser utilities for QA agent tools.
Contains cookie management and Chrome options setup.
"""

import tempfile
import os
from typing import Optional

try:
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


def setup_chrome_options(headless: bool = True, enable_cookies: bool = True, session_storage_dir: Optional[str] = None):
    """
    Set up Chrome options with cookie persistence support.
    
    Args:
        headless: Whether to run in headless mode
        enable_cookies: Whether to enable cookies and session persistence
        session_storage_dir: Directory to store session data
        
    Returns:
        Chrome Options object configured for the specified settings
    """
    if not SELENIUM_AVAILABLE:
        raise ImportError("Selenium is not installed. Please install it with: pip install selenium webdriver-manager")
    
    chrome_options = Options()
    
    # Basic Chrome options
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    
    # Enable cookies and local storage for session persistence
    if enable_cookies:
        chrome_options.add_argument("--enable-cookies")
        chrome_options.add_argument("--enable-local-storage")
        chrome_options.add_argument("--enable-session-storage")
        chrome_options.add_argument("--disable-web-security")  # Allow cross-origin requests
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")
        
        # Set user data directory for persistent storage
        if session_storage_dir:
            # Convert to absolute path and ensure it exists
            user_data_dir = os.path.abspath(session_storage_dir)
            os.makedirs(user_data_dir, exist_ok=True)
        else:
            user_data_dir = tempfile.mkdtemp(prefix="selenium_chrome_")
        
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        print(f"Using Chrome user data directory: {user_data_dir}")
    
    return chrome_options