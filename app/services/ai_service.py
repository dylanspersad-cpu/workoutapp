import requests
from app.config import get_settings


class AIService:
    def __init__(self):
        settings = get_settings()
        self.api_key = settings.ai_api_key
        self.base_url = settings.ai_base_url.rstrip("/")
        self.model_name = settings.ai_model_name

    def ask(self, user_prompt: str) -> str:
        url = f"{self.base_url}/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful workout assistant for a workout planning app. "
                        "Give practical, beginner-friendly and gym-friendly fitness advice. "
                        "Keep answers clear and concise."
                    ),
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            "temperature": 0.7,
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)

        print("AI status code:", response.status_code)
        print("AI raw response:", response.text)

        response.raise_for_status()

        data = response.json()

        if "choices" not in data:
            raise ValueError(f"Unexpected AI response format: {data}")

        return data["choices"][0]["message"]["content"]