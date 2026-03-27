"use client";

import { api } from "@/lib/api";

export default function ConnectGmailBanner() {
  return (
    <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 mb-6 flex items-center justify-between">
      <div>
        <p className="font-semibold text-amber-800">Connect your Gmail account</p>
        <p className="text-sm text-amber-600 mt-0.5">
          Grant access so the AI can read and manage your inbox.
        </p>
      </div>
      <button
        onClick={() => api.connectGmail()}
        className="bg-amber-500 hover:bg-amber-600 text-white font-semibold px-4 py-2 rounded-lg text-sm transition-colors shrink-0"
      >
        Connect Gmail
      </button>
    </div>
  );
}
