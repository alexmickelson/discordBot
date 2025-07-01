import React from "react";
import { useMusicWebSocket } from "../../contexts/useMusicWebSocketContexts";
import { useInfoTask } from "../useRefreshInfoTask";

export const PlaybackStatus: React.FC = () => {
  const { error, message, botStatus } = useMusicWebSocket();

  useInfoTask();

  return (
    <div className="flex justify-end my-3">
      <div className="inline-block">
        <div className="border rounded-lg p-3 bg-gray-800">
          <h5 className="text-center text-lg font-semibold mb-2">
            Status Messages
          </h5>
          {botStatus && <div>status: {botStatus}</div>}
          {error && <div>error: {error}</div>}
          {message && <div>message: {message}</div>}
        </div>
      </div>
    </div>
  );
};
