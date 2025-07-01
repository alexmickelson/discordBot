from discord import VoiceClient


__voice_client: VoiceClient | None = None


def get_voice_client():
    global __voice_client
    return __voice_client


def set_voice_client(client: VoiceClient | None):
    global __voice_client
    __voice_client = client


def get_is_paused_from_voice_client():
    voice_client = get_voice_client()
    if voice_client is not None:
        return not voice_client.is_playing() and voice_client.is_connected()
    return False


async def stop_playback_and_disconnect():
    voice_client = get_voice_client()
    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await voice_client.disconnect()


def stop_playback():
    voice_client = get_voice_client()
    if voice_client and voice_client.is_playing():
        voice_client.stop()
