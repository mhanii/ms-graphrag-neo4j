import os
from openai import AsyncOpenAI


class OpenAIProvider:
    def __init__(self, model: str, **kwargs):
        if not os.environ.get("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.model = model
        self._openai_client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    async def achat(self, messages, model=None, config={}):
        model_to_use = model or self.model
        response = await self._openai_client.chat.completions.create(
            model=model_to_use,
            messages=messages,
            **config,
        )
        return response.choices[0].message