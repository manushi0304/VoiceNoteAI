import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8000"


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
            return True
        else:
            print("LOGIN ERROR:", response.text)
            return False

    except Exception as e:
        print("Login Exception:", e)
        return False


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

        return response.status_code == 200

    except Exception as e:
        print("Register Exception:", e)
        return False