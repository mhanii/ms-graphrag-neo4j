import os
from openai import AsyncAzureOpenAI


class AzureProvider:
    def __init__(self, model: str, **kwargs):
        if not os.environ.get("AZURE_OPENAI_API_KEY"):
            raise ValueError("AZURE_OPENAI_API_KEY not found in environment variables")
        if not os.environ.get("AZURE_OPENAI_ENDPOINT"):
            raise ValueError("AZURE_OPENAI_ENDPOINT not found in environment variables")

        self.model = model
        self._azure_client = AsyncAzureOpenAI(
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
            api_version=os.environ.get("OPENAI_API_VERSION", "2024-05-01-preview"),
            **kwargs,
        )

    async def achat(self, messages, model=None, config={}):
        model_to_use = model or self.model
        response = await self._azure_client.chat.completions.create(
            model=model_to_use,
            messages=messages,
            **config,
        )
        return response.choices[0].message