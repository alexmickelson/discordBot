import { useWebSocket } from "../contexts/useWebSocket";

export const AllSongs = () => {
  const { allSongsList } = useWebSocket();

  return (
    <div className="max-w-2xl mx-auto mt-8">
      <h2 className="text-2xl font-bold mb-4 text-center text-gray-200">
        All Songs
      </h2>
      <ul className="bg-gray-900 rounded-lg shadow divide-y divide-gray-800">
        {allSongsList.length === 0 && (
          <li className="text-center text-gray-400 py-6">
            No songs available.
          </li>
        )}
        {allSongsList.map((song, idx) => (
          <li
            key={idx}
            className="flex items-center px-4 py-3 hover:bg-gray-800 transition-colors group"
          >
            <span className="flex-1 text-gray-100 truncate">
              {song.filename
                .substring(song.filename.lastIndexOf("/") + 1)
                .replace(".mp3", "")}
            </span>
            <span className="ml-4 text-gray-400 text-sm">
              {Math.floor(song.duration / 60)}:
              {(song.duration % 60).toString().padStart(2, "0")}
            </span>
            {/* Add more actions/icons here if needed */}
          </li>
        ))}
      </ul>
    </div>
  );
};
