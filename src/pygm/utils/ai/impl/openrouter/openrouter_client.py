from openai import OpenAI

from pygm.utils.ai.ai_client import AIClient
from pygm.utils.ai.ai_prompt import AIPrompt
from pygm.utils.ai.ai_response import AIResponse
from pygm.utils.ai.ai_response_builder import AIResponseBuilder


class OpenRouterClient(AIClient):
    """
    AI Client for OpenRouter using an injected OpenAI-compatible client.
    """

    def __init__(self, client: OpenAI, model: str) -> None:
        """
        Initialize the OpenRouter client.
        :param client: Pre-configured OpenAI client for OpenRouter.
        :param model: model to use for requests.
        """
        self._client: OpenAI = client
        self._model: str = model

    def send_prompt(self, prompt: AIPrompt) -> AIResponse:
        """
        Send a prompt to OpenRouter and return the response.
        :param prompt: The prompt to send.
        :return: The AI response.
        """
        messages = self._build_messages(prompt)
        builder = AIResponseBuilder(prompt.get_prompt_id())
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=prompt.get_temperature(),
                max_tokens=prompt.get_max_output_tokens(),
            )
            self._handle_success(response, builder)
        except Exception as e:
            self._handle_error(e, builder)
        return builder.build()

    @classmethod
    def _build_messages(cls, prompt: AIPrompt) -> list[dict[str, str]]:
        """
        Build the messages list for the API call.
        :param prompt: The prompt containing messages.
        :return: List of message dictionaries.
        """
        return [
            {"role": msg.get_role().value, "content": msg.get_content()}
            for msg in prompt.get_messages()
        ]

    @classmethod
    def _handle_success(cls, response, builder: AIResponseBuilder) -> None:
        """
        Handle a successful API response.
        :param response: The API response object.
        :param builder: The response builder to populate.
        """
        content = response.choices[0].message.content or ""
        finish_reason = response.choices[0].finish_reason or ""
        builder.set_content(content)
        builder.set_finish_reason(finish_reason)

    @classmethod
    def _handle_error(cls, error: Exception, builder: AIResponseBuilder) -> None:
        """
        Handle an API error.
        :param error: The exception that occurred.
        :param builder: The response builder to populate.
        """
        builder.set_content("")
        builder.set_error(str(error))
