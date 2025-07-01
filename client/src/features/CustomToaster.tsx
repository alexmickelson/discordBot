import "@fortawesome/fontawesome-free/css/all.min.css";
import toast, { ToastBar, Toaster } from "react-hot-toast";

export function CustomToaster() {
  return (
    <Toaster
      position="top-right"
      gutter={8}
      toastOptions={{
        duration: 5000,
      }}
    >
      {(t) => (
        <ToastBar toast={t}>
          {({ icon, message }) => (
            <div className="flex items-center px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg shadow-lg text-gray-100 min-w-[220px] max-w-xs">
              {icon}
              <div className="ml-3 flex-1 text-sm font-medium">{message}</div>
              <button
                onClick={() => toast.dismiss(t.id)}
                className="ml-3 p-1 rounded hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-violet-500"
                aria-label="Close"
              >
                <i className="fas fa-times text-gray-400 text-lg"></i>
              </button>
            </div>
          )}
        </ToastBar>
      )}
    </Toaster>
  );
}
