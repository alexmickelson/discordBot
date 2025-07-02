import {
  useGetAllSongsQuery,
} from "../playbackHooks";
import { SongListItem } from "./SongListItem";

export const AllSongs = () => {
  const { data: allSongsList } = useGetAllSongsQuery();
  console.log("all songs list",allSongsList);
  return (
    <div className="max-w-2xl mx-auto overflow-y-auto h-full">
      <div className=" font-bold mb-2 text-center text-violet-200">All</div>
      <div className="bg-violet-950/40 rounded-lg shadow p-4">
        {allSongsList.length === 0 && (
          <div className="text-center text-gray-400 py-6">
            No songs available.
          </div>
        )}
        <div className="flex flex-wrap gap-4 justify-center">
          {allSongsList.map((song, i) => (
            <SongListItem key={i} song={song} />
          ))}
        </div>
      </div>
    </div>
  );
};
