import pytest
from faker import Faker

from pygm.utils.ai.ai_provider_type import AIProviderType
from pygm.utils.ai.api_key import ApiKey
from pygm.utils.ai.api_key_manager import ApiKeyManager


@pytest.fixture
def faker() -> Faker:
    """
    Provides a Faker instance for generating fake data.
    :return: the faker instance
    """
    return Faker()


@pytest.mark.repeat(10)
def test_api_key_manager(faker) -> None:
    """
    Test setting and getting API keys using ApiKeyManager.
    :param faker: Faker instance for generating fake data.
    """
    api_key: str = faker.sha1()
    ApiKeyManager.get_instance().set_api_key(AIProviderType.TEST, api_key)
    assert ApiKeyManager.get_instance().get_api_key(AIProviderType.TEST) == ApiKey(
        AIProviderType.TEST, api_key
    )
