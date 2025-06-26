import { AllSongs } from "./components/AllSongs";
import { CurrentSong } from "./components/CurrentSong";
import { PlaybackInfo } from "./components/PlaybackInfo";
import { SongQueue } from "./components/SongQueue";

export const App = () => {
  return (
    <div className="max-w-4xl mx-auto mt-12">
      <h1 className="text-center text-3xl font-bold mb-8">Discord Music</h1>
      <CurrentSong />
      <SongQueue />
      <PlaybackInfo />
      <hr />
      <AllSongs />
    </div>
  );
};
