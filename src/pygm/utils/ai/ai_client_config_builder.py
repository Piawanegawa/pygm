from pygm.utils.ai.ai_client_config import AIClientConfig
from pygm.utils.ai.ai_provider_type import AIProviderType
from pygm.utils.ai.api_key import ApiKey


class AIClientConfigBuilder:
    """
    Builder for creating AIClientConfig instances.
    """

    def __init__(self, provider_type: AIProviderType) -> None:
        """
        Initialize the AIClientConfigBuilder.
        :param provider_type: The AI provider type.
        """
        self._provider_type: AIProviderType = provider_type
        self._api_key: str | None = None
        self._model_id: str | None = None

    def set_api_key(self, api_key: str) -> "AIClientConfigBuilder":
        """
        Set the API key.
        :param api_key: The API key.
        :return: The builder instance.
        """
        self._api_key: str = api_key
        return self

    def build(self) -> AIClientConfig:
        """
        Build the AIClientConfig.
        :return: The constructed AIClientConfig.
        :raises ValueError: If required fields are missing.
        """
        if self._api_key is None:
            raise ValueError("API key is required")
        api_key = ApiKey(provider_type=self._provider_type, api_key=self._api_key)
        from .impl.openrouter.openrouter_client_config import OpenRouterClientConfig
        if self._provider_type == AIProviderType.OPENROUTER:
            return OpenRouterClientConfig(api_key=api_key, model_id=self._model_id)
        raise ValueError(f"Unsupported provider type: {self._provider_type}")