import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/discord_ws": {
        target: "http://api:8080",
        ws: true, // Enable WebSocket proxying
      },
      "/api": {
        target: "http://api:8080",
      },
    },
  },
});
