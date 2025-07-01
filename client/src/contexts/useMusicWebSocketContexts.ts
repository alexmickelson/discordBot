import { createContext, useContext } from "react";

interface MusicWebSocketContextType {
  error: string;
  message: string;
  botStatus: string | undefined;
  // playbackInfo: PlaybackInfoData | undefined;
  // songQueue: SongQueue | undefined;
  // sendMessage: (message: unknown) => void;
  // allSongsList: SongMetadata[];
}

export const MusicWebSocketContext = createContext<
  MusicWebSocketContextType | undefined
>(undefined);

export const useMusicWebSocket = () => {
  const context = useContext(MusicWebSocketContext);
  if (!context) {
    throw new Error(
      "useMusicWebSocket must be used within a MusicWebSocketProvider"
    );
  }
  return context;
};
