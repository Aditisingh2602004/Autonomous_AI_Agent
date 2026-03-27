#designed for authentication and API communication
import os
from typing import Any            #allow flexible data types

import requests                   #used to call api 
from dotenv import load_dotenv


class AuthManager:
    """Manage login and authenticated requests for a Django REST API."""

    def __init__(self, base_url: str, username: str, password: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.timeout = timeout
        self.access_token: str | None = None
        self.session = requests.Session()

    def login(self, force: bool = False) -> dict[str, str]:
        """
        Login and store access token.
        Avoid repeated login unless force=True.
        """

        # ✅ reuse token
        if self.access_token and not force:
            print("🔁 Using cached token")
            return {"access": self.access_token}

        url = f"{self.base_url}/api/auth/login/"    #build login API request
        payload = {
            "username": self.username,
            "password": self.password,
        }

        print(f"\n🔐 LOGIN → {url}")

        response = self.session.post(url, json=payload, timeout=self.timeout) #send request to login

        if response.status_code != 200:
            print("❌ Login failed:", response.text)
            raise Exception(f"Login failed: {response.text}")

        data = response.json()                #getting JWT token
        access = data.get("access")

        if not access:
            raise Exception(f"No access token in response: {data}")

        self.access_token = access
        print("✅ Login successful")           #token is saved for future use 

        return {"access": access}

    def get_headers(self) -> dict[str, str]:
        """Return auth headers with valid token."""
        if not self.access_token:
            self.login()

        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def make_request(
        self,
        method: str,
        endpoint: str,
        data: dict[str, Any] | None = None,
    ) -> requests.Response:
        """Make authenticated request and retry once if token expired."""

        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self.get_headers()

        print(f"\n📡 {method.upper()} → {url}")

        response = self.session.request(
            method=method.upper(),
            url=url,
            json=data,
            headers=headers,
            timeout=self.timeout,
        )

        # ✅ retry on expired token
        if response.status_code == 401:           #auto recovery logic for handel token expiry 
            print("🔄 Token expired, refreshing...")
            self.login(force=True)
            headers = self.get_headers()

            response = self.session.request(
                method=method.upper(),
                url=url,
                json=data,
                headers=headers,
                timeout=self.timeout,
            )

        print(f"Status: {response.status_code}")

        return response

    @classmethod
    def from_env(cls) -> "AuthManager":
        """Load config from .env"""
        load_dotenv(override=True)

        base_url = os.getenv("BASE_URL")
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")

        if not base_url or not username or not password:
            raise ValueError("Missing BASE_URL / USERNAME / PASSWORD in .env")

        return cls(base_url, username, password)


# ✅ SINGLE GLOBAL INSTANCE (CRITICAL)
_AUTH_INSTANCE: AuthManager | None = None


def get_auth_manager() -> AuthManager:
    global _AUTH_INSTANCE

    if _AUTH_INSTANCE is None:
        _AUTH_INSTANCE = AuthManager.from_env()

    return _AUTH_INSTANCE


# ✅ Manual test
if __name__ == "__main__":
    load_dotenv(override=True)

    auth = get_auth_manager()

    auth.login()  # login once
    res = auth.make_request("GET", "/api/auth/me/")

    print("\n👤 USER:")
    print(res.text)