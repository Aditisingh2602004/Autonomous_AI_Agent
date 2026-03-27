import os

from dotenv import load_dotenv
from langchain_core.tools import tool
from playwright.sync_api import sync_playwright

from auth_manager import AuthManager

load_dotenv(override=True)


@tool
def read_local_instructions(file_path: str) -> str:
    """
    Read the local instructions file and return its content.
    """
    print("==== READ INSTRUCTIONS START ====")
    print("File Path:", file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        print("Read successful")
        print("==== READ INSTRUCTIONS END ====")
        return content
    except Exception as e:
        print("Read failed:", str(e))
        print("==== READ INSTRUCTIONS END ====")
        return f"ERROR reading instructions: {str(e)}"


@tool
def login_agent() -> str:
    """
    Log in to the backend using credentials from environment variables.
    Returns the access token or an error message.
    """
    print("==== LOGIN AGENT START ====")
    print("DEBUG USERNAME FROM ENV:", os.getenv("USERNAME"))

    if not os.getenv("USERNAME"):
        print("==== LOGIN AGENT END ====")
        return "ERROR: USERNAME not found in environment"

    try:
        auth = AuthManager.from_env()
        token = auth.login()
        access = token.get("access")

        if not access:
            raise ValueError("No access token returned from backend")

        print("Login successful")
        print("==== LOGIN AGENT END ====")
        return access
    except Exception as e:
        print("Login failed:", str(e))
        print("==== LOGIN AGENT END ====")
        return f"ERROR login failed: {str(e)}"


@tool
def get_me() -> str:
    """
    Verify authentication by calling /api/auth/me/ and returning user details.
    """
    print("==== GET ME START ====")

    try:
        auth = AuthManager.from_env()
        auth.login()
        response = auth.make_request("GET", "/api/auth/me/")
        print("get_me successful")
        print("==== GET ME END ====")
        return response.text
    except Exception as e:
        print("get_me failed:", str(e))
        print("==== GET ME END ====")
        return f"ERROR get_me failed: {str(e)}"


@tool
def login_frontend() -> str:
    """
    Open browser and login to frontend UI automatically.
    """
    load_dotenv(override=True)

    url = "http://localhost:5173/login"
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")

    print("Opening browser...")

    if not username or not password:
        return "Frontend login failed: USERNAME or PASSWORD missing in environment"

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()

            page.goto(url)

            print("Filling login form...")

            page.fill('input[name="username"]', username)
            page.fill('input[name="password"]', password)
            page.click('button[type="submit"]')

            page.wait_for_timeout(5000)

            print("Frontend login successful")
            browser.close()
            return "Frontend login successful"
    except Exception as e:
        return f"Frontend login failed: {str(e)}"
