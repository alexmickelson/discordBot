import { useWebSocket } from "../contexts/useWebSocket";
import classes from "./SongQueue.module.css";

export const SongQueue = () => {
  const { songQueue, sendMessage } = useWebSocket();

  return (
    <div>
      {songQueue && (
        <div>
          <ul className="border rounded shadow">
            {songQueue.song_file_list.map((s, i) => {
              const isCurrent = i === songQueue.position;
              return (
                <li
                  key={i}
                  className={`p-0 m-0 ${isCurrent ? "bg-blue-950" : ""} ${
                    classes.songListItem
                  }`}
                >
                  <div className="flex h-full items-center">
                    <div className="flex-none text-right my-auto w-10">
                      {!isCurrent && (
                        <i
                          className="fas fa-play text-blue-500 text-3xl cursor-pointer"
                          role="button"
                          onClick={() => {
                            sendMessage({
                              action: "play_song_by_index",
                              position: i,
                            });
                          }}
                        ></i>
                      )}
                      {isCurrent && (
                        <i
                          className="fas fa-pause text-blue-500 text-3xl cursor-pointer"
                          role="button"
                          onClick={() => {
                            sendMessage({
                              action: "pause_song",
                            });
                          }}
                        ></i>
                      )}
                    </div>
                    <div className="flex-1 my-auto">
                      {s.filename
                        .substring(s.filename.lastIndexOf("/") + 1)
                        .replace(".mp3", "")}
                    </div>
                  </div>
                </li>
              );
            })}
          </ul>
        </div>
      )}
    </div>
  );
};
