import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from types import SimpleNamespace


class GeminiProvider:
    def __init__(self, model: str, **kwargs):
        if not os.environ.get("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        self.model = model
        self.kwargs = kwargs

    async def achat(self, messages, model=None, config={}):
        model_to_use = model or self.model
        generation_config = config.get("generation_config", {})
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        gemini_model = genai.GenerativeModel(
            model_name=model_to_use,
            generation_config=generation_config,
            safety_settings=safety_settings,
            **self.kwargs,
        )

        # Gemini uses 'user' and 'model' roles. We map from OpenAI's roles.
        # 'system' prompts are not directly supported in the same way,
        # but we can prepend it to the first user message.
        gemini_messages = []
        system_prompt = ""
        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
                continue
            # Map assistant to model
            role = "model" if msg["role"] == "assistant" else msg["role"]
            content = msg["content"]
            if system_prompt and role == "user":
                content = f"{system_prompt}\n\n{content}"
                system_prompt = ""  # Clear after prepending
            gemini_messages.append({"role": role, "parts": [content]})

        response = await gemini_model.generate_content_async(gemini_messages)

        # Adapt the response to resemble the OpenAI message format (a SimpleNamespace is sufficient)
        return SimpleNamespace(content=response.text)