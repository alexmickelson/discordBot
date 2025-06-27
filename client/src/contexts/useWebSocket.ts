import { createContext, useContext } from "react";

interface WebSocketConnectionContextType {
  ws: WebSocket | undefined;
}

export const WebSocketConnectionContext = createContext<
  WebSocketConnectionContextType | undefined
>(undefined);

export const useWebSocketConnection = () => {
  const context = useContext(WebSocketConnectionContext);
  if (!context) {
    throw new Error(
      "useWebSocketConnection must be used within a WebSocketConnectionProvider"
    );
  }
  return context;
};