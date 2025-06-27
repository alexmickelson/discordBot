import { useMusicWebSocket } from "../contexts/useMusicWebSocketContexts";
import { SongIcon } from "./SongIcon";

export const SongQueue = () => {
  const { songQueue } = useMusicWebSocket();

  return (
    <div className="bg-violet-950/50 rounded-xl shadow-lg p-4 max-w-xl mx-auto mt-6">
      {songQueue && (
        <div>
          <div className="">
            {songQueue.song_file_list.map((s, i) => {
              const isCurrent = i === songQueue.position;
              return (
                <div
                  key={i}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors duration-150 mb-2 last:mb-0 cursor-pointer hover:bg-violet-900/80 ${
                    isCurrent
                      ? "bg-gradient-to-r from-violet-800 to-violet-950 shadow-md scale-[1.02]"
                      : "bg-violet-950/60"
                  }`}
                  style={{ minHeight: 56 }}
                >
                  <div className="flex-none w-10 text-right">
                    <SongIcon index={i} />
                  </div>
                  <div
                    className={`flex-1 font-medium truncate ${
                      isCurrent ? "text-violet-100" : "text-violet-300"
                    }`}
                  >
                    {s.filename
                      .substring(s.filename.lastIndexOf("/") + 1)
                      .replace(".mp3", "")}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};
