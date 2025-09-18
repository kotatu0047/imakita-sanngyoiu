import pytest
import asyncio
import os
import tempfile
from unittest.mock import AsyncMock, MagicMock, patch, mock_open
from datetime import datetime
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
        interaction.followup = MagicMock()
        interaction.followup.send = AsyncMock()
        interaction.channel = MagicMock()
        interaction.channel.name = "test-channel"
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

    @pytest.fixture
    def mock_message(self):
        """Create a mock  Discord message."""
        message = MagicMock()
        message.created_at = datetime(2023, 1, 1, 12, 0, 0)
        message.author = MagicMock()
        message.author.display_name = "TestUser"
        message.content = "Test message content"
        message.attachments = []
        message.embeds = []
        return message

    @pytest.mark.asyncio
    async def test_maketxt_command_response(self, mock_interaction):
        """Test that maketxt command sends correct initial response."""
        from main import bot

        # Find the maketxt command
        maketxt_command = None
        for command in bot.tree.get_commands():
            if command.name == "maketxt":
                maketxt_command = command
                break

        assert maketxt_command is not None

        # Mock the channel history
        async def async_iter():
            for item in []:
                yield item

        mock_interaction.channel.history = MagicMock(return_value=async_iter())

        with patch('builtins.open', mock_open()) as mock_file:
            # Execute the command
            await maketxt_command.callback(mock_interaction)

            # Verify initial response
            mock_interaction.response.send_message.assert_called_once_with("📝 Starting to export channel messages to text file...")

    @pytest.mark.asyncio
    async def test_maketxt_command_with_messages(self, mock_interaction, mock_message):
        """Test maketxt command with actual messages."""
        from main import bot

        # Find the maketxt command
        maketxt_command = None
        for command in bot.tree.get_commands():
            if command.name == "maketxt":
                maketxt_command = command
                break

        # Mock channel history with one message
        async def async_iter():
            for item in [mock_message]:
                yield item

        mock_interaction.channel.history = MagicMock(return_value=async_iter())

        with patch('builtins.open', mock_open()) as mock_file, \
             patch('os.makedirs') as mock_makedirs:
            # Execute the command
            await maketxt_command.callback(mock_interaction)

            # Verify exports directory was created
            mock_makedirs.assert_called_once_with("exports", exist_ok=True)

            # Verify file was opened for writing
            mock_file.assert_called_once()
            handle = mock_file.return_value

            # Check that write was called multiple times (header + message)
            assert handle.write.call_count > 0

    @pytest.mark.asyncio
    async def test_maketxt_command_permission_error(self, mock_interaction):
        """Test maketxt command handles permission errors."""
        from main import bot

        # Find the maketxt command
        maketxt_command = None
        for command in bot.tree.get_commands():
            if command.name == "maketxt":
                maketxt_command = command
                break

        # Mock channel history to raise Forbidden exception
        async def async_iter():
            raise discord.Forbidden(MagicMock(), "Forbidden")
            yield  # This line never executes but is needed for the function to be a generator

        mock_interaction.channel.history = MagicMock(return_value=async_iter())

        # Execute the command
        await maketxt_command.callback(mock_interaction)

        # Verify error message was sent
        mock_interaction.followup.send.assert_called_once_with("❌ Error: I don't have permission to read message history in this channel.")

    @pytest.mark.asyncio
    async def test_maketxt_command_file_creation(self, mock_interaction, mock_message):
        """Test that maketxt command creates properly formatted file."""
        from main import bot

        # Find the maketxt command
        maketxt_command = None
        for command in bot.tree.get_commands():
            if command.name == "maketxt":
                maketxt_command = command
                break

        # Mock channel history with one message
        async def async_iter():
            for item in [mock_message]:
                yield item

        mock_interaction.channel.history = MagicMock(return_value=async_iter())

        mock_file_content = []
        def mock_write(content):
            mock_file_content.append(content)

        with patch('builtins.open', mock_open()) as mock_file, \
             patch('os.makedirs') as mock_makedirs:
            mock_file.return_value.write.side_effect = mock_write

            # Execute the command
            await maketxt_command.callback(mock_interaction)

            # Check file content structure
            written_content = ''.join(mock_file_content)
            assert "Channel Log Export:" in written_content
            assert "Total Messages:" in written_content
            assert "TestUser:" in written_content
            assert "Test message content" in written_content