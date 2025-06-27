import React from "react";
import ReactDOM from "react-dom/client";
import "bootstrap-icons/font/bootstrap-icons.css";
import "@fortawesome/fontawesome-free/css/all.min.css";
import { App } from "./App";
import "./index.css";
import { WebSocketConnectionProvider } from "./contexts/WebSocketContext";
import { MusicWebSocketProvider } from "./contexts/MusicWebSocketProvider";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <WebSocketConnectionProvider>
      <MusicWebSocketProvider>
        <App />
      </MusicWebSocketProvider>
    </WebSocketConnectionProvider>
  </React.StrictMode>
);
