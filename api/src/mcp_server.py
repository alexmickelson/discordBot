from mcp import MCPServer, expose
from src.music_controls import MusicControls

controls = MusicControls()

class MusicControlsMCP:
    @expose()
    def seek_to_position(self, data):
        return controls.seek_to_position(data)

    @expose()
    def play_song_by_index(self, data):
        return controls.play_song_by_index(data)

    @expose()
    def get_playback_info(self, data):
        return controls.get_playback_info(data)

    @expose()
    def get_all_songs(self, data):
        return controls.get_all_songs(data)

    @expose()
    def add_song_to_queue(self, data):
        return controls.add_song_to_queue(data)

    @expose()
    def pause_song(self, data):
        return controls.pause_song(data)

    @expose()
    def unpause_song(self, data):
        return controls.unpause_song(data)


def start_mcp_server():
    server = MCPServer()
    server.register(MusicControlsMCP())
    server.serve_in_background()
