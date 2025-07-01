import { AllSongs } from "./features/allSongs/AllSongs";
import { PlaybackStatus } from "./features/currentlyPlaying/PlaybackInfo";
import { AddUrlToQueue } from "./features/songQueue/AddUrlToQueue";
import { CurrentSong } from "./features/currentlyPlaying/CurrentSong";
import { SongQueue } from "./features/songQueue/SongQueue";

export const App = () => {
  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 px-5 mx-auto w-full min-h-0 flex flex-col">
        <div className="flex gap-5 justify-center">
          <div className="min-w-200">
            <AddUrlToQueue />
          </div>
          <PlaybackStatus />
        </div>
        <div className="flex gap-3 flex-1 min-h-0 pt-3">
          <div className="flex-1 h-full">
            <AllSongs />
          </div>
          <div className="flex-1 h-full">
            <SongQueue />
          </div>
        </div>
      </div>
      <div className="w-full z-50 bg-gray-900 bg-opacity-90 border-t border-slate-600">
        <CurrentSong />
      </div>
    </div>
  );
};
