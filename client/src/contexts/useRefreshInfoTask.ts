import { useEffect } from "react";
import { useWebSocketConnection } from "../contexts/useWebSocket";

const updateInterval = 100;

const getPlaybackInfo = (ws: WebSocket) => {
  ws.send(JSON.stringify({ action: "get_playback_info" }));
};
export const useInfoTask = () => {
  const { ws } = useWebSocketConnection();
  useEffect(() => {
    const interval = setInterval(() => {
      if (
        ws &&
        ws.readyState === ws.OPEN
      ) {
        getPlaybackInfo(ws);
      }
    }, updateInterval);

    return () => clearInterval(interval);
  }, [ws]);
};
