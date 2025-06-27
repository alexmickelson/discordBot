from fastmcp import FastMCP
from src.music_controls import MusicControls

discord_mcp = FastMCP("Discord Music MCP")
controls = MusicControls()


@discord_mcp.tool
def seek_to_position(position: int):
    return controls.seek_to_position(position)


@discord_mcp.tool
def play_song_by_index(position: int):
    return controls.play_song_by_index(position)


@discord_mcp.tool
def get_playback_info():
    return controls.get_playback_info()


@discord_mcp.tool
def get_all_songs():
    return controls.get_all_songs()


@discord_mcp.tool
def add_song_to_queue(filename: str):
    return controls.add_song_to_queue(filename)


@discord_mcp.tool
def pause_song():
    return controls.pause_song()


@discord_mcp.tool
def unpause_song():
    return controls.unpause_song()


@discord_mcp.tool(
    description="""
        Adds a YouTube video to the playback queue.

        Args:
            url (str): The URL of the YouTube video to add. The URL must be a valid YouTube video link containing only the 'v=' query parameter (e.g., 'https://www.youtube.com/watch?v=VIDEO_ID').

        Returns:
            The result of adding the video to the queue.

        Note:
            Ensure that the provided URL is a direct YouTube video link with only the 'v=' parameter and no additional query parameters.
        """
)
def add_to_queue(url: str):
    return controls.add_to_queue(url)
