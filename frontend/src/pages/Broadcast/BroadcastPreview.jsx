import React from "react";
import PropTypes from "prop-types";

export default function BroadcastPreview({ title, message }) {
  return (
    <div className="bg-white p-6 rounded-2xl border border-gray-200 shadow-sm max-w-sm mx-auto">
      <div className="flex items-start gap-3">
        <div className="bg-blue-100 p-2 rounded-lg text-blue-600">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            className="lucide lucide-bell"
          >
            <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9" />
            <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0" />
          </svg>
        </div>
        <div>
          <h3 className="font-bold text-gray-900">
            {title || "Broadcast Title"}
          </h3>
          <p className="text-sm text-gray-600 mt-1">
            {message || "This is a preview of the broadcast message."}
          </p>
          <span className="text-xs text-gray-400 mt-2 block">Just now</span>
        </div>
      </div>
    </div>
  );
}

BroadcastPreview.propTypes = {
  title: PropTypes.string,
  message: PropTypes.string,
};
