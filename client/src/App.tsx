import { AllSongs } from "./features/allSongs/AllSongs";
import { PlaybackInfo } from "./features/currentlyPlaying/PlaybackInfo";
import { AddUrlToQueue } from "./features/songQueue/AddUrlToQueue";
import { CurrentSong } from "./features/currentlyPlaying/CurrentSong";
import { SongQueue } from "./features/songQueue/SongQueue";

export const App = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <div className="flex-1 max-w-4xl mx-auto w-full mt-12 mb-32">
        <h1 className="text-center text-3xl font-bold mb-8">Discord Music</h1>
        <SongQueue />
        <PlaybackInfo />
        <hr />
        <AllSongs />
        <hr />
        <AddUrlToQueue />
      </div>
      <div className="fixed bottom-0 left-0 w-full z-50 bg-gray-900 bg-opacity-90 border-t border-slate-600">
        <div className="max-w-4xl mx-auto w-full">
          <CurrentSong />
        </div>
      </div>
    </div>
  );
};
