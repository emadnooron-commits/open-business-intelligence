import json
import os
import urllib.request
import urllib.error


class LLMProvider:
    def generate(self, prompt):
        raise NotImplementedError


class GeminiFreeProvider(LLMProvider):
    """
    Free-first Gemini provider.

    The provider never enables billing by itself.
    It requires GEMINI_API_KEY to be supplied by the environment.
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured."
            )

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash-lite"
        )

        self.url = (
            "https://generativelanguage.googleapis.com/v1beta/"
            f"models/{self.model}:generateContent"
            f"?key={self.api_key}"
        )

    def generate(self, prompt):
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json"
            }
        }

        body = json.dumps(
            payload,
            ensure_ascii=False
        ).encode("utf-8")

        request = urllib.request.Request(
            self.url,
            data=body,
            headers={
                "Content-Type": "application/json"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=120
            ) as response:

                raw = response.read().decode(
                    "utf-8"
                )

                data = json.loads(raw)

        except urllib.error.HTTPError as error:
            message = error.read().decode(
                "utf-8",
                errors="replace"
            )

            raise RuntimeError(
                f"Gemini API error {error.code}: "
                f"{message}"
            )

        except urllib.error.URLError as error:
            raise RuntimeError(
                f"Network error while calling Gemini: "
                f"{error}"
            )

        candidates = data.get(
            "candidates",
            []
        )

        if not candidates:
            raise RuntimeError(
                "Gemini returned no candidates."
            )

        parts = (
            candidates[0]
            .get("content", {})
            .get("parts", [])
        )

        if not parts:
            raise RuntimeError(
                "Gemini returned no content."
            )

        text = parts[0].get(
            "text",
            ""
        )

        if not text:
            raise RuntimeError(
                "Gemini returned empty text."
            )

        return json.loads(text)


def get_provider():
    return GeminiFreeProvider()
