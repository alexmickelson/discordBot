import { useMusicWebSocket } from "../../contexts/useMusicWebSocketContexts";
import { Slider } from "./Slider";
import { Spinner } from "../../utils/Spinner";
import { useSeekToPositionMutation } from "../playbackHooks";

export const CurrentSong = () => {
  const { playbackInfo } = useMusicWebSocket();
  const seekToPositionMutation = useSeekToPositionMutation();
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
                <Slider
                  min={0}
                  max={playbackInfo.duration}
                  current={playbackInfo.current_position}
                  onChange={(v) => {
                    seekToPositionMutation.mutate(v);
                  }}
                />
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center h-full p-2">
            <Spinner />
            <div className="text-gray-400">No song is currently playing</div>
          </div>
        )}
      </div>
    </>
  );
};
