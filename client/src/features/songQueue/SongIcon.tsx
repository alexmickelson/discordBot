import React from "react";
import { useSongQueueQuery, usePlaySongByIndexMutation, usePauseMutation, useUnpauseMutation } from "../playbackHooks";

export const SongIcon: React.FC<{
  index: number;
}> = ({ index }) => {
  const { data: songQueue } = useSongQueueQuery();
  const playSongByIndexMutation = usePlaySongByIndexMutation();
  const pauseMutation = usePauseMutation();
  const unpauseMutation = useUnpauseMutation();
  if (!songQueue) return null;
  const isCurrent = index === songQueue.position;
  const isPaused = songQueue.is_paused;

  if (!isCurrent) {
    return (
      <i
        className="fas fa-play text-blue-500 text-3xl cursor-pointer transition-transform duration-150 hover:scale-110 hover:text-blue-700"
        role="button"
        onClick={() => playSongByIndexMutation.mutate(index)}
      ></i>
    );
  }
  if (isPaused) {
    return (
      <i
        className="fas fa-play text-blue-500 text-3xl cursor-pointer transition-transform duration-150 hover:scale-110 hover:text-blue-700"
        role="button"
        onClick={() => unpauseMutation.mutate()}
      ></i>
    );
  }
  return (
    <i
      className="fas fa-pause text-blue-500 text-3xl cursor-pointer transition-transform duration-150 hover:scale-110 hover:text-blue-700"
      role="button"
      onClick={() => pauseMutation.mutate()}
    ></i>
  );
};
