import "@fortawesome/fontawesome-free/css/all.min.css";
import toast, { ToastBar, Toaster } from "react-hot-toast";

export function CustomToaster() {
  return (
    <Toaster
      position="top-right"
      gutter={8}
      toastOptions={{
        duration: 50000,
      }}
    >
      {(t) => (
        <ToastBar
          toast={t}
          style={{
            padding: "0",
            margin: "0",
          }}
        >
          {({ icon, message }) => (
            <div
              className={`
                flex items-center px-4 py-3 
                bg-gray-900 
                border border-gray-700 rounded shadow-lg 
                text-gray-100 
                min-w-[220px] max-w-xs
              `}
            >
              {icon}
              <div className="ml-3 flex-1 text-sm font-medium">{message}</div>
              <button
                onClick={() => toast.dismiss(t.id)}
                className={`
                    ml-3 p-1 rounded
                    transition-transform duration-200 ease-in-out hover:scale-125
                    hover:text-gray-600 
                `}
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
