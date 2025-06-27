import { FC, ReactNode, useEffect, useState } from "react";
import { WebSocketConnectionContext } from "./useWebSocket";

export const WebSocketConnectionProvider: FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [ws, setWs] = useState<WebSocket | undefined>();

  useEffect(() => {
    const websocket = new WebSocket(
      `${window.location.protocol === "https:" ? "wss" : "ws"}://${
        window.location.host
      }/discord_ws`
    );
    setWs(websocket);
    return () => {
      setWs(undefined);
      websocket.close();
    };
  }, []);

  return (
    <WebSocketConnectionContext.Provider value={{ ws }}>
      {children}
    </WebSocketConnectionContext.Provider>
  );
};
