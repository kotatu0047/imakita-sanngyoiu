import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
import discord


class TestBotCommands:
    """Test cases for bot commands."""

    @pytest.fixture
    def mock_interaction(self):
        """Create a mock Discord interaction."""
        interaction = MagicMock(spec=discord.Interaction)
        interaction.user = MagicMock()
        interaction.user.name = "test_user"
        interaction.response = MagicMock()
        interaction.response.send_message = AsyncMock()
        return interaction

    @pytest.mark.asyncio
    async def test_hello_command_response(self, mock_interaction):
        """Test that hello command sends correct response."""
        from main import bot

        # Find the hello command
        hello_command = None
        for command in bot.tree.get_commands():
            if command.name == "hello":
                hello_command = command
                break

        assert hello_command is not None

        # Execute the command
        await hello_command.callback(mock_interaction)

        # Verify response
        mock_interaction.response.send_message.assert_called_once_with("discord worldX")

    @pytest.mark.asyncio
    async def test_hello_command_logging(self, mock_interaction):
        """Test that hello command logs user request."""
        from main import bot

        mock_interaction.user.name = "test_logger"

        hello_command = None
        for command in bot.tree.get_commands():
            if command.name == "hello":
                hello_command = command
                break

        with patch('builtins.print') as mock_print:
            await hello_command.callback(mock_interaction)
            mock_print.assert_called_with("test_logger requested /hello")

    def test_bot_configuration(self):
        """Test bot configuration is correct."""
        from main import bot

        assert bot.command_prefix == '!'
        assert hasattr(bot, 'tree')
        assert bot.intents.message_content is True