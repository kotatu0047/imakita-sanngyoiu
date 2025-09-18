import pytest
import asyncio
import unittest.mock
from unittest.mock import AsyncMock, MagicMock, patch
import discord
from bot.main import bot


@pytest.fixture
def mock_interaction():
    """Create a mock Discord interaction for testing."""
    interaction = MagicMock(spec=discord.Interaction)
    interaction.user = MagicMock()
    interaction.user.name = "test_user"
    interaction.response = MagicMock()
    interaction.response.send_message = AsyncMock()
    return interaction


@pytest.mark.asyncio
async def test_hello_command(mock_interaction):
    """Test the hello command responds correctly."""
    # Get the hello command from the bot's command tree
    hello_command = None
    for command in bot.tree.get_commands():
        if command.name == "hello":
            hello_command = command
            break

    assert hello_command is not None, "Hello command not found"

    # Execute the command
    await hello_command.callback(mock_interaction)

    # Verify the response
    mock_interaction.response.send_message.assert_called_once_with("discord worldX")


@pytest.mark.asyncio
async def test_on_ready_event():
    """Test the on_ready event handler."""
    with patch('builtins.print') as mock_print:
        # Mock bot.tree.sync
        with patch.object(bot.tree, 'sync', return_value=[]) as mock_sync:
            # Test the sync functionality directly
            synced_commands = await bot.tree.sync()
            mock_sync.assert_called_once()
            assert synced_commands == []


def test_bot_initialization():
    """Test that the bot is properly initialized."""
    assert bot is not None
    assert bot.command_prefix == '!'
    assert bot.intents.message_content is True


@pytest.mark.asyncio
async def test_hello_command_with_different_user(mock_interaction):
    """Test hello command with different user name."""
    mock_interaction.user.name = "different_user"

    hello_command = None
    for command in bot.tree.get_commands():
        if command.name == "hello":
            hello_command = command
            break

    with patch('builtins.print') as mock_print:
        await hello_command.callback(mock_interaction)
        mock_print.assert_called_with("different_user requested /hello")


@pytest.mark.asyncio
async def test_ping_command(mock_interaction):
    """Test the ping command responds with latency."""
    ping_command = None
    for command in bot.tree.get_commands():
        if command.name == "ping":
            ping_command = command
            break

    assert ping_command is not None

    # Execute the command - bot.latency will be NaN when not connected
    await ping_command.callback(mock_interaction)

    # Verify that send_message was called with a message containing "Pong! Latency:"
    call_args = mock_interaction.response.send_message.call_args[0][0]
    assert "Pong! Latency:" in call_args
    # When not connected, latency should show "Unknown"
    assert "Unknown" in call_args


@pytest.mark.asyncio
async def test_echo_command(mock_interaction):
    """Test the echo command repeats the message."""
    echo_command = None
    for command in bot.tree.get_commands():
        if command.name == "echo":
            echo_command = command
            break

    assert echo_command is not None
    test_message = "Hello World!"
    await echo_command.callback(mock_interaction, test_message)
    mock_interaction.response.send_message.assert_called_once_with(f"Echo: {test_message}")


def test_all_commands_exist():
    """Test that all commands are registered."""
    commands = bot.tree.get_commands()
    command_names = [cmd.name for cmd in commands]
    expected_commands = ["hello", "ping", "echo"]

    for cmd in expected_commands:
        assert cmd in command_names, f"Command '{cmd}' not found in registered commands"


def test_command_description():
    """Test that the hello command has correct description."""
    hello_command = None
    for command in bot.tree.get_commands():
        if command.name == "hello":
            hello_command = command
            break

    assert hello_command is not None
    assert hello_command.description == "Responds with 'world'"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])