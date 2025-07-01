import { useMutation, useSuspenseQuery } from "@tanstack/react-query";
import axiosClient from "../utils/axiosClient";
import { PlaybackInfoData, SongMetadata, SongQueue } from "../models";

export const playbackKeys = {
  allSongs: ["allSongs"],
  playbackInfo: ["playbackInfo"],
  songQueue: ["songQueue"],
};

export const useSeekToPositionMutation = () => {
  return useMutation({
    mutationFn: async (position: number) => {
      const response = await axiosClient.post("/api/seek_to_position", null, {
        params: { position },
      });
      return response.data;
    },
  });
};

export const usePlaySongByIndexMutation = () => {
  return useMutation({
    mutationFn: async (position: number) => {
      const response = await axiosClient.post("/api/play_song_by_index", null, {
        params: { position },
      });
      return response.data;
    },
  });
};

export const useAddSongToQueueMutation = () => {
  return useMutation({
    mutationFn: async (filename: string) => {
      const response = await axiosClient.post("/api/add_song_to_queue", null, {
        params: { filename },
      });
      return response.data;
    },
  });
};

export const usePauseMutation = () => {
  return useMutation({
    mutationFn: async () => {
      const response = await axiosClient.post("/api/pause_song");
      return response.data;
    },
  });
};

export const useUnpauseMutation = () => {
  return useMutation({
    mutationFn: async () => {
      const response = await axiosClient.post("/api/unpause_song");
      return response.data;
    },
  });
};

export const useAddToQueueMutation = () => {
  return useMutation({
    mutationFn: async (url: string) => {
      const response = await axiosClient.post("/api/add_to_queue", null, {
        params: { url },
      });
      return response.data;
    },
  });
};

export const useGetAllSongsQuery = () => {
  return useSuspenseQuery({
    queryKey: playbackKeys.allSongs,
    queryFn: async () => {
      const response = await axiosClient.get<SongMetadata[]>(
        "/api/get_all_songs"
      );
      return response.data;
    },
  });
};

export const usePlaybackInfoQuery = () => {
  return useSuspenseQuery({
    queryKey: playbackKeys.playbackInfo,
    queryFn: async () => {
      const response = await axiosClient.get<PlaybackInfoData>(
        "/api/get_playback_info"
      );
      return response.data;
    },
  });
};

export const useSongQueueQuery = () => {
  return useSuspenseQuery({
    queryKey: playbackKeys.songQueue,
    queryFn: async () => {
      const response = await axiosClient.get<SongQueue>("/api/get_song_queue");
      return response.data;
    },
  });
};
