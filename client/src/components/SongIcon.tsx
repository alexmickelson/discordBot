import React from "react";
import { useMusicWebSocket } from "../contexts/useMusicWebSocketContexts";

export const SongIcon: React.FC<{
  index: number;
}> = ({ index }) => {
  const { songQueue, sendMessage } = useMusicWebSocket();
  if (!songQueue) return null;
  const isCurrent = index === songQueue.position;
  const isPaused = songQueue.is_paused;

  if (!isCurrent) {
    return (
      <i
        className="fas fa-play text-blue-500 text-3xl cursor-pointer transition-transform duration-150 hover:scale-110 hover:text-blue-700"
        role="button"
        onClick={() =>
          sendMessage({ action: "play_song_by_index", position: index })
        }
      ></i>
    );
  }
  if (isPaused) {
    return (
      <i
        className="fas fa-play text-blue-500 text-3xl cursor-pointer transition-transform duration-150 hover:scale-110 hover:text-blue-700"
        role="button"
        onClick={() => sendMessage({ action: "unpause_song" })}
      ></i>
    );
  }
  return (
    <i
      className="fas fa-pause text-blue-500 text-3xl cursor-pointer transition-transform duration-150 hover:scale-110 hover:text-blue-700"
      role="button"
      onClick={() => sendMessage({ action: "pause_song" })}
    ></i>
  );
};
