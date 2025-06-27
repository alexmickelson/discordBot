import { useMusicWebSocket } from "../contexts/useMusicWebSocketContexts";

export const AllSongs = () => {
  const { allSongsList, songQueue, sendMessage } = useMusicWebSocket();

  const isInQueue = (filename: string) => {
    if (!songQueue || !songQueue.song_file_list) return false;
    return songQueue.song_file_list.some((item) => item.filename === filename);
  };

  return (
    <div className="max-w-2xl mx-auto mt-8">
      <h2 className="text-2xl font-bold mb-4 text-center text-gray-200">
        All Songs
      </h2>
      <div className="bg-gray-900 rounded-lg shadow divide-y divide-gray-800">
        {allSongsList.length === 0 && (
          <div className="text-center text-gray-400 py-6">
            No songs available.
          </div>
        )}
        {allSongsList.map((song, idx) => (
          <div
            key={idx}
            className="flex items-center px-4 py-3 hover:bg-gray-800 transition-colors group cursor-pointer"
            onClick={() =>
              sendMessage({ action: "add_song_to_queue", filename: song.filename })
            }
            title={
              isInQueue(song.filename) ? "Already in queue" : "Add to queue"
            }
          >
            <span className="mr-2">{isInQueue(song.filename) ? "🎶" : ""}</span>
            <span className="flex-1 text-gray-100 truncate">
              {song.filename
                .substring(song.filename.lastIndexOf("/") + 1)
                .replace(".mp3", "")}
            </span>
            <span className="ml-4 text-gray-400 text-sm">
              {Math.floor(song.duration / 60)}:
              {(song.duration % 60).toString().padStart(2, "0")}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
