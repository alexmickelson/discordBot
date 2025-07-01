import { useState } from "react";
import { useMusicWebSocket } from "../../contexts/useMusicWebSocketContexts";

export const AddUrlToQueue = () => {
  const { sendMessage } = useMusicWebSocket();
  const [url, setUrl] = useState("");

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        if (!url.trim()) return;
        sendMessage({ action: "add_to_queue", url });
        setUrl("");
      }}
      className="w-full mx-auto bg-gray-900 rounded-xl shadow-lg p-2 flex flex-col gap-1 mt-2 border border-gray-800"
    >
      <label htmlFor="url" className="text-gray-200 font-semibold text-lg">
        YouTube URL
      </label>
      <input
        id="url"
        type="url"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Paste a song URL..."
        className={[
          "",
        ].join(" ")}
        autoComplete="off"
        required
      />
      <button
        type="submit"
        className=""
      >
        Add to Queue
      </button>
    </form>
  );
};
