import { useMusicWebSocket } from "../../contexts/useMusicWebSocketContexts";
import { useWebSocketConnection } from "../../contexts/useWebSocket";
import { Slider } from "./Slider";
import { Spinner } from "../../utils/Spinner";

export const CurrentSong = () => {
  const { playbackInfo, sendMessage } = useMusicWebSocket();
  const { ws } = useWebSocketConnection();
  return (
    <>
      <div className=" bg-gray-900 bg-opacity-50 flex flex-col items-center justify-center min-h-[80px]">
        {playbackInfo ? (
          <div>
            <h2 className="text-xl font-semibold mb-2">Playing Song</h2>
            <h5 className="text-lg font-medium mb-4">
              {playbackInfo.file_name}
            </h5>
            {ws && (
              <Slider
                min={0}
                max={playbackInfo.duration}
                current={playbackInfo.current_position}
                onChange={(v) => {
                  sendMessage({ action: "seek_to_position", position: v });
                }}
              />
            )}
          </div>
        ) : (
          <>
            <Spinner />
            <div className="text-gray-400">No song is currently playing</div>
          </>
        )}
      </div>
    </>
  );
};
