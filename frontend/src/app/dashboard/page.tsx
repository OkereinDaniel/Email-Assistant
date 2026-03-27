"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import EmailList from "@/components/EmailList";
import Sidebar from "@/components/Sidebar";
import ConnectGmailBanner from "@/components/ConnectGmailBanner";

export default function DashboardPage() {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(true);
  const [gmailConnected, setGmailConnected] = useState(false);

  useEffect(() => {
    async function fetchEmails() {
      try {
        const data = await api.getEmails();
        setEmails(data.emails);
        setGmailConnected(true);
      } catch {
        setGmailConnected(false);
      } finally {
        setLoading(false);
      }
    }
    fetchEmails();
  }, []);

  return (
    <div className="flex h-screen bg-slate-100">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-6">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-2xl font-bold text-slate-800 mb-6">Inbox</h1>
          {!gmailConnected && <ConnectGmailBanner />}
          {loading ? (
            <p className="text-slate-500">Loading emails...</p>
          ) : (
            <EmailList emails={emails} />
          )}
        </div>
      </main>
    </div>
  );
}
