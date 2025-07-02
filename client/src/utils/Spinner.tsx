import React from "react";

export const Spinner: React.FC<{ size?: number; className?: string }> = ({ size = 32, className = "" }) => (
  <div
    className={`flex items-center justify-center ${className}`}
    style={{ width: size, height: size }}
  >
    <svg
      className="animate-spin text-gray-500"
      style={{ width: size, height: size }}
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      />
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
      />
    </svg>
  </div>
);
