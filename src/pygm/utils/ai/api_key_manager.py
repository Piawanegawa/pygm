import os
from dotenv import load_dotenv, set_key

from pygm.utils.ai.ai_provider_type import AIProviderType
from pygm.utils.ai.api_key import ApiKey


class ApiKeyManager:
    """
    Manages API keys for different AI providers with persistence via dotenv.
    """

    ENV_FILE = "pygm.env"

    def __init__(self) -> None:
        """
        Initialize the ApiKeyManager and load existing keys from env file.
        """
        self._api_keys: dict[AIProviderType, ApiKey] = {}
        self._load_from_env()

    def set_api_key(self, provider_type: AIProviderType, api_key: ApiKey) -> None:
        """
        Set an API key for a provider and persist it.

        :param provider_type: The type of AI provider.
        :param api_key: The ApiKey object to store.
        """
        self._api_keys[provider_type] = api_key
        env_key = self._get_env_key_name(provider_type)
        set_key(self.ENV_FILE, env_key, api_key.get_api_key())

    def get_api_key(self, provider_type: AIProviderType) -> ApiKey:
        """
        Get the API key for a provider.

        :param provider_type: The type of AI provider.
        :return: The ApiKey object.
        :raises KeyError: If no API key is set for the provider.
        """
        if provider_type not in self._api_keys:
            raise KeyError(f"No API key set for provider: {provider_type.value}")
        return self._api_keys[provider_type]

    def _load_from_env(self) -> None:
        """
        Load API keys from the environment file.
        """
        if os.path.exists(self.ENV_FILE):
            load_dotenv(self.ENV_FILE)
            for provider_type in AIProviderType:
                env_key = self._get_env_key_name(provider_type)
                api_key_value = os.getenv(env_key)
                if api_key_value:
                    self._api_keys[provider_type] = ApiKey(provider_type, api_key_value)

    @staticmethod
    def _get_env_key_name(provider_type: AIProviderType) -> str:
        """
        Get the environment variable name for a provider type.

        :param provider_type: The AI provider type.
        :return: The environment variable name.
        """
        return f"{provider_type.value}_API_KEY"
