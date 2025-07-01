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
      <div className="bg-gray-900 rounded-lg shadow p-4">
        {allSongsList.length === 0 && (
          <div className="text-center text-gray-400 py-6">
            No songs available.
          </div>
        )}
        <div className="flex flex-wrap gap-4 justify-center">
          {allSongsList.map((song, idx) => (
            <div
              key={idx}
              className="flex flex-col items-center w-44 bg-gray-800 rounded-lg p-3 mb-2 shadow hover:bg-gray-700 transition-colors group cursor-pointer"
              onClick={() =>
                sendMessage({ action: "add_song_to_queue", filename: song.filename })
              }
              title={
                isInQueue(song.filename) ? "Already in queue" : "Add to queue"
              }
            >
              {song.thumbnail && (
                <img
                  src={`/api/get_song_thumbnail?thumbnail=${encodeURIComponent(song.thumbnail)}`}
                  alt="thumbnail"
                  className="w-24 h-24 rounded mb-2 object-cover bg-gray-700"
                  loading="lazy"
                />
              )}
              <span className="mr-2">{isInQueue(song.filename) ? "🎶" : ""}</span>
              <span className="flex-1 text-gray-100 truncate text-center w-full">
                {song.filename
                  .substring(song.filename.lastIndexOf("/") + 1)
                  .replace(".mp3", "")}
              </span>
              <span className="mt-1 text-gray-400 text-sm">
                {Math.floor(song.duration / 60)}:
                {(song.duration % 60).toString().padStart(2, "0")}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
