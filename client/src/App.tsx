import { AllSongs } from "./features/allSongs/AllSongs";
import { PlaybackInfo } from "./features/currentlyPlaying/PlaybackInfo";
import { AddUrlToQueue } from "./features/songQueue/AddUrlToQueue";
import { CurrentSong } from "./features/currentlyPlaying/CurrentSong";
import { SongQueue } from "./features/songQueue/SongQueue";

export const App = () => {
  return (
    <div className="max-w-4xl mx-auto mt-12">
      <h1 className="text-center text-3xl font-bold mb-8">Discord Music</h1>
      <CurrentSong />
      <SongQueue />
      <PlaybackInfo />
      <hr />
      <AllSongs />
      <hr />
      <AddUrlToQueue />
    </div>
  );
};
