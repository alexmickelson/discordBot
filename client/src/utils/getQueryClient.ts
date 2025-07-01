import { QueryCache, QueryClient } from "@tanstack/react-query";
import { toast } from "react-hot-toast";

export function getQueryClient(): QueryClient {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: 0,
      },
      mutations: {
        retry: 0,
        onError: handleQueryError,
      },
    },
    queryCache: new QueryCache({
      onError: handleQueryError,
    }),
  });
}

// Custom error handler for queries
export function handleQueryError(error: unknown) {
  console.log('in error handler', error);
  const message =
    (error &&
      typeof error === "object" &&
      "message" in error &&
      error.message) ||
    "An error occurred";
  toast.error(String(message));
}
