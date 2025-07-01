import React from "react";
import ReactDOM from "react-dom/client";
import "bootstrap-icons/font/bootstrap-icons.css";
import "@fortawesome/fontawesome-free/css/all.min.css";
import { App } from "./App";
import "./index.css";
import { WebSocketConnectionProvider } from "./contexts/WebSocketContextProvicer";
import { MusicWebSocketProvider } from "./contexts/MusicWebSocketProvider";
import { CustomToaster } from "./features/CustomToaster";
import { QueryClientProvider } from "@tanstack/react-query";
import { getQueryClient } from "./utils/getQueryClient";
import { SuspenseAndError } from "./utils/SuspenseAndError";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <CustomToaster />
    <QueryClientProvider client={getQueryClient()}>
      <SuspenseAndError>
        <WebSocketConnectionProvider>
          <MusicWebSocketProvider>
            <App />
          </MusicWebSocketProvider>
        </WebSocketConnectionProvider>
      </SuspenseAndError>
    </QueryClientProvider>
  </React.StrictMode>
);
