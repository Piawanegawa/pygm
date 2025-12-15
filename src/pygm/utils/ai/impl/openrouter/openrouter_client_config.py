from pygm.utils.ai.ai_client_config import AIClientConfig
from pygm.utils.ai.api_key import ApiKey


class OpenRouterClientConfig(AIClientConfig):
    """
    Configuration for the OpenRouter AI client.
    """

    def __init__(self, api_key: ApiKey, model_id: str | None) -> None:
        """
        Initialize the OpenRouterClientConfig.

        :param api_key: The API key for OpenRouter.
        """
        super().__init__(api_key=api_key, model_id=model_id)