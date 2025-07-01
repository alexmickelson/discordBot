import { Suspense } from "react";
import { useQueryErrorResetBoundary } from "@tanstack/react-query";
import { ErrorBoundary } from "react-error-boundary";
import { Spinner } from "./Spinner";

export const SuspenseAndError = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  const { reset } = useQueryErrorResetBoundary();
  return (
    <ErrorBoundary
      onReset={reset}
      fallbackRender={({ error, resetErrorBoundary }) => {
        return (
          <div>
            There was an error! {String(error)}
            <button className="btn" onClick={() => resetErrorBoundary()}>Try again</button>
          </div>
        );
      }}
    >
      <Suspense fallback={<Spinner />}>{children}</Suspense>
    </ErrorBoundary>
  );
};
