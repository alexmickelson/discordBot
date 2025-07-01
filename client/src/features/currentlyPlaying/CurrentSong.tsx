import { useMusicWebSocket } from "../../contexts/useMusicWebSocketContexts";
import { useWebSocketConnection } from "../../contexts/useWebSocket";
import { Slider } from "./Slider";
import { Spinner } from "../../utils/Spinner";

export const CurrentSong = () => {
  const { playbackInfo, sendMessage } = useMusicWebSocket();
  const { ws } = useWebSocketConnection();
  return (
    <>
      <div className="bg-gradient-to-r from-gray-900/30 via-violet-950/30 to-violet-950 bg-opacity-70 flex flex-col min-h-0 w-full">
        {playbackInfo ? (
          <div className="flex gap-5 p-5 align-middle">
            <div>
              <div className="font-medium ">
                {playbackInfo.file_name
                  ? playbackInfo.file_name.substring(
                      playbackInfo.file_name.lastIndexOf("/") + 1
                    )
                  : ""}
              </div>
            </div>
            <div className="flex-grow">
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
