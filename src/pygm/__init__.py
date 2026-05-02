#!/usr/bin/env python3

"""
pygm - Gamemaster Toolbox.

This package provides tools for tabletop RPG game masters, including
AI-powered generation of plot hooks, NPC descriptions, scene descriptions,
random encounters, secrets, puzzles, loot, and battlemaps.
"""

from pygm.utils.ai.ai_client import AIClient
from pygm.utils.ai.ai_client_config import AIClientConfig
from pygm.utils.ai.ai_client_config_builder import AIClientConfigBuilder
from pygm.utils.ai.ai_message_role import AIMessageRole
from pygm.utils.ai.ai_prompt import AIPrompt
from pygm.utils.ai.ai_prompt_builder import AIPromptBuilder
from pygm.utils.ai.ai_provider_factory import AIProviderFactory
from pygm.utils.ai.ai_provider_type import AIProviderType

DEFAULT_MODEL_ID: str = "openai/gpt-4o-mini"


def main() -> None:
    """
    Run a small interactive AI chatbot in the console.
    :return: None.
    """
    print("pygm AI Chatbot")
    print("Type 'exit', 'quit', or press Ctrl+C to close.")
    print()

    model_id = _ask_model_id()
    try:
        ai_client = _create_ai_client(model_id)
    except Exception as error:
        print(f"Could not create AI client: {error}")
        input("Press Enter to close...")
        return

    _run_chat(ai_client)


def _ask_model_id() -> str:
    """
    Ask for the OpenRouter model identifier.
    :return: The selected model identifier.
    """
    model_id = input(f"OpenRouter model [{DEFAULT_MODEL_ID}]: ").strip()
    if not model_id:
        model_id = DEFAULT_MODEL_ID
    return model_id


def _create_ai_client(model_id: str) -> AIClient:
    """
    Create the configured AI client.
    :param model_id: The model identifier to use.
    :return: The created AI client.
    """
    config: AIClientConfig = (
        AIClientConfigBuilder(AIProviderType.OPENROUTER).set_model_id(model_id).build()
    )
    provider = AIProviderFactory.create_ai_provider(config)
    return provider.create_ai_client(config)


def _run_chat(ai_client: AIClient) -> None:
    """
    Run the interactive chat loop.
    :param ai_client: The AI client to use for chat messages.
    :return: None.
    """
    messages: list[tuple[AIMessageRole, str]] = [
        (
            AIMessageRole.SYSTEM,
            "You are pygm, a helpful assistant for tabletop RPG game masters.",
        )
    ]
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if user_input.lower() in {"exit", "quit"}:
            break
        if user_input:
            _send_chat_message(ai_client, messages, user_input)


def _send_chat_message(
    ai_client: AIClient,
    messages: list[tuple[AIMessageRole, str]],
    user_input: str,
) -> None:
    """
    Send one user message and print the assistant response.
    :param ai_client: The AI client to use.
    :param messages: The conversation history.
    :param user_input: The user message.
    :return: None.
    """
    messages.append((AIMessageRole.USER, user_input))
    prompt = _build_prompt(messages)
    response = ai_client.send_prompt(prompt)
    if response.get_error():
        print(f"AI error: {response.get_error()}")
    else:
        content = response.get_content()
        print(f"AI: {content}")
        messages.append((AIMessageRole.ASSISTANT, content))


def _build_prompt(messages: list[tuple[AIMessageRole, str]]) -> AIPrompt:
    """
    Build an AI prompt from the current conversation history.
    :param messages: The conversation history.
    :return: The prompt to send.
    """
    builder = AIPromptBuilder("pygm-console-chat").set_temperature(0.7)
    for role, content in messages:
        builder.add_message(role, content)
    return builder.build()
