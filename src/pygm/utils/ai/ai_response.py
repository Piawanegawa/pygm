from pydantic import BaseModel


class AIResponse(BaseModel):
    """
    Represents a response from an AI provider.
    """

    prompt_id: str
    content: str
    finish_reason: str | None = None
    error: str | None = None

    def get_prompt_id(self) -> str:
        """
        Get the prompt ID.

        :return: The prompt ID.
        """
        return self.prompt_id

    def get_content(self) -> str:
        """
        Get the response content.

        :return: The response content.
        """
        return self.content

    def get_finish_reason(self) -> str | None:
        """
        Get the finish reason.

        :return: The finish reason or None.
        """
        return self.finish_reason

    def get_error(self) -> str | None:
        """
        Get the error message.

        :return: The error message or None.
        """
        return self.error