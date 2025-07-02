import { useState } from "react";
import { useAddToQueueMutation } from "../playbackHooks";
import { Spinner } from "../../utils/Spinner";

export const AddUrlToQueue = () => {
  const [url, setUrl] = useState("");
  const addToQueueMutation = useAddToQueueMutation();

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        if (!url.trim()) return;
        addToQueueMutation.mutate(url);
        setUrl("");
      }}
      className="w-full mx-auto bg-gray-900 rounded-xl shadow-lg p-2 flex flex-col gap-1 mt-2 border border-gray-800"
    >
      <label htmlFor="url" className="text-gray-200 font-semibold text-lg">
        YouTube URL
      </label>
      <div className="flex gap-3">
        <div className="flex-1">
          <input
            id="url"
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Paste a song URL..."
            autoComplete="off"
            className="w-full"
            required
          />
        </div>
        <div>
          {addToQueueMutation.isPending ? (
            <div className="flex justify-center items-center h-10">
              <Spinner />
            </div>
          ) : (
            <button type="submit" className="btn">
              Add to Queue
            </button>
          )}
        </div>
      </div>
    </form>
  );
};
