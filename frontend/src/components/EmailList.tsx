"use client";

import { useState } from "react";
import { api } from "@/lib/api";

type Email = {
  id: string;
  subject: string;
  sender: string;
  preview: string;
  priority: "urgent" | "important" | "normal" | "low";
  received_at: string;
  is_read: boolean;
};

const priorityStyles: Record<Email["priority"], string> = {
  urgent: "bg-red-100 text-red-700",
  important: "bg-amber-100 text-amber-700",
  normal: "bg-blue-100 text-blue-700",
  low: "bg-slate-100 text-slate-500",
};

export default function EmailList({ emails }: { emails: Email[] }) {
  const [selected, setSelected] = useState<string | null>(null);
  const [reply, setReply] = useState<string | null>(null);
  const [summary, setSummary] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  if (!emails.length) {
    return <p className="text-slate-500 mt-4">No emails to display.</p>;
  }

  async function handleGenerateReply(emailId: string) {
    setLoading(true);
    setReply(null);
    const data = await api.generateReply(emailId);
    setReply(data.reply);
    setLoading(false);
  }

  async function handleSummarize(emailId: string) {
    setLoading(true);
    setSummary(null);
    const data = await api.summarizeEmail(emailId);
    setSummary(data.summary);
    setLoading(false);
  }

  return (
    <div className="space-y-3">
      {emails.map((email) => (
        <div
          key={email.id}
          className={`bg-white rounded-xl border p-4 cursor-pointer transition-shadow hover:shadow-md ${
            selected === email.id ? "border-brand-500 shadow-md" : "border-slate-200"
          } ${!email.is_read ? "font-semibold" : ""}`}
          onClick={() => setSelected(selected === email.id ? null : email.id)}
        >
          <div className="flex items-start justify-between gap-4">
            <div className="min-w-0">
              <p className="text-sm text-slate-500 truncate">{email.sender}</p>
              <p className="text-slate-800 truncate">{email.subject}</p>
              <p className="text-sm text-slate-400 truncate mt-1 font-normal">
                {email.preview}
              </p>
            </div>
            <div className="flex flex-col items-end gap-2 shrink-0">
              <span
                className={`text-xs px-2 py-0.5 rounded-full font-medium ${priorityStyles[email.priority]}`}
              >
                {email.priority}
              </span>
              <span className="text-xs text-slate-400">{email.received_at}</span>
            </div>
          </div>

          {selected === email.id && (
            <div className="mt-4 pt-4 border-t border-slate-100">
              <div className="flex gap-2 flex-wrap">
                <button
                  onClick={(e) => { e.stopPropagation(); handleGenerateReply(email.id); }}
                  className="text-sm bg-brand-600 hover:bg-brand-700 text-white px-3 py-1.5 rounded-lg transition-colors"
                >
                  Generate Reply
                </button>
                <button
                  onClick={(e) => { e.stopPropagation(); handleSummarize(email.id); }}
                  className="text-sm bg-slate-100 hover:bg-slate-200 text-slate-700 px-3 py-1.5 rounded-lg transition-colors"
                >
                  Summarize
                </button>
                <button
                  onClick={(e) => { e.stopPropagation(); api.extractTask(email.id); }}
                  className="text-sm bg-slate-100 hover:bg-slate-200 text-slate-700 px-3 py-1.5 rounded-lg transition-colors"
                >
                  Extract Task
                </button>
              </div>
              {loading && <p className="text-sm text-slate-400 mt-3">Working...</p>}
              {reply && (
                <div className="mt-3 bg-blue-50 border border-blue-100 rounded-lg p-3 text-sm text-slate-700">
                  <p className="font-medium text-blue-700 mb-1">Suggested Reply</p>
                  {reply}
                </div>
              )}
              {summary && (
                <div className="mt-3 bg-slate-50 border border-slate-200 rounded-lg p-3 text-sm text-slate-700">
                  <p className="font-medium text-slate-600 mb-1">Summary</p>
                  {summary}
                </div>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
