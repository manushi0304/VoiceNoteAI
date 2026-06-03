import requests
import streamlit as st

from utils.api import API_BASE as BASE_URL



def login_user(email, password):
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            data={
                "username": email,
                "password": password
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        if response.status_code == 200:
            token = response.json()["access_token"]
            st.session_state["token"] = token
            st.session_state["authenticated"] = True
            return True, "Success"
        else:
            try:
                detail = response.json().get("detail", "Login failed")
                if isinstance(detail, list):
                    detail = "; ".join(str(item) for item in detail)
            except Exception:
                detail = response.text or "Login failed"
            return False, detail

    except Exception as e:
        return False, f"Connection error: {str(e)}"


def register_user(email, password, full_name):
    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json={
                "email": email,
                "password": password,
                "full_name": full_name
            }
        )

        if response.status_code == 200:
            return True, "Success"
        else:
            try:
                detail = response.json().get("detail", "Registration failed")
                if isinstance(detail, list):
                    detail = "; ".join(str(item) for item in detail)
            except Exception:
                detail = response.text or "Registration failed"
            return False, detail

    except Exception as e:
        return False, f"Connection error: {str(e)}"