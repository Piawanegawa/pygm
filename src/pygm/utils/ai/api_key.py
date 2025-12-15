from pygm.utils.ai.ai_provider_type import AIProviderType


class ApiKey:
    """
    Represents an API key for a specific AI provider.
    """

    def __init__(self, provider_type: AIProviderType, api_key: str) -> None:
        """
        Initialize the ApiKey.

        :param provider_type: The type of AI provider.
        :param api_key: The API key string.
        """
        self._provider_type = provider_type
        self._api_key = api_key

    def get_provider_type(self) -> AIProviderType:
        """
        Get the provider type.

        :return: The AI provider type.
        """
        return self._provider_type

    def get_api_key(self) -> str:
        """
        Get the API key.

        :return: The API key string.
        """
        return self._api_key