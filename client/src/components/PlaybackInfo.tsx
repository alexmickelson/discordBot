import React from "react";
import { useInfoTask } from "./useInfoTask";
import { useWebSocket } from "../contexts/useWebSocket";

export const PlaybackInfo: React.FC = () => {
  const { ws, error, message, botStatus } = useWebSocket();

  useInfoTask(ws);

  return (
    <div className="flex justify-end my-3">
      <div className="inline-block">
        <div className="border rounded-lg p-3 bg-gray-800">
          <h5 className="text-center text-lg font-semibold mb-2">Status Messages</h5>
          {botStatus && <div>status: {botStatus}</div>}
          {error && <div>error: {error}</div>}
          {message && <div>message: {message}</div>}
        </div>
      </div>
    </div>
  );
};
