import { useState } from "react";
import { useMusicWebSocket } from "../contexts/useMusicWebSocketContexts";

export const AddUrlToQueue = () => {
  const { sendMessage, error, message } = useMusicWebSocket();
  const [url, setUrl] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;
    sendMessage({ action: "add_to_queue", url });
    setSubmitted(true);
    setUrl("");
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="w-full max-w-lg mx-auto bg-gray-900 rounded-xl shadow-lg p-6 flex flex-col gap-4 mt-8 border border-gray-800"
    >
      <label htmlFor="url" className="text-gray-200 font-semibold text-lg">
        Add Song by URL
      </label>
      <input
        id="url"
        type="url"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Paste a song URL..."
        className="px-4 py-2 rounded bg-gray-800 text-gray-100 focus:outline-none focus:ring-2 focus:ring-violet-500 placeholder-gray-400"
        autoComplete="off"
        required
      />
      <button
        type="submit"
        className="bg-violet-700 hover:bg-violet-800 text-white font-bold py-2 px-4 rounded transition-colors duration-150 shadow"
      >
        Add to Queue
      </button>
      {submitted && message && (
        <div className="text-green-400 text-sm mt-2">{message}</div>
      )}
      {error && <div className="text-red-400 text-sm mt-2">{error}</div>}
    </form>
  );
};
