import { SongMetadata } from "../../models";
import { useSongQueueQuery, useAddSongToQueueMutation } from "../playbackHooks";

export const SongListItem = ({ song }: { song: SongMetadata }) => {
  const { data: songQueue } = useSongQueueQuery();
  const addSongToQueueMutation = useAddSongToQueueMutation();

  const isInQueue =
    songQueue &&
    songQueue.song_file_list &&
    songQueue.song_file_list.some((item) => item.filename === song.filename);

  return (
    <div
      className="flex flex-col items-center w-44 bg-gray-800 rounded-lg p-3 mb-2 shadow hover:bg-gray-700 transition-colors group cursor-pointer"
      onClick={() => addSongToQueueMutation.mutate(song.filename)}
      title={isInQueue ? "Already in queue" : "Add to queue"}
    >
      {song.thumbnail && (
        <img
          src={`/api/get_song_thumbnail?thumbnail=${encodeURIComponent(
            song.thumbnail
          )}`}
          alt="thumbnail"
          className="w-24 h-24 rounded mb-2 object-cover bg-gray-700"
          loading="lazy"
        />
      )}

      <span className="flex-1 text-gray-100 truncate text-center w-full">
        {song.filename
          .substring(song.filename.lastIndexOf("/") + 1)
          .replace(".mp3", "")}
      </span>
      <div className="flex gap-1 justify-start w-100">
        <div className="">{isInQueue ? "🎶" : ""}</div>
        <div className=" flex-1 text-gray-400 text-sm">
          {Math.floor(song.duration / 60)}:
          {(song.duration % 60).toString().padStart(2, "0")}
        </div>
      </div>
    </div>
  );
};
