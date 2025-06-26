import { useWebSocket } from "../contexts/useWebSocket";
import classes from "./SongQueue.module.css";
import { SongIcon } from "./SongIcon";

export const SongQueue = () => {
  const { songQueue } = useWebSocket();

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
                      <SongIcon index={i} />
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
