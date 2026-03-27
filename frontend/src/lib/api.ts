import axios from "axios";

const client = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

export const api = {
  connectGmail: () => client.post("/connect-gmail").then((r) => r.data),

  getEmails: () => client.get("/emails").then((r) => r.data),

  generateReply: (emailId: string, context?: string) =>
    client.post("/generate-reply", { email_id: emailId, context }).then((r) => r.data),

  summarizeEmail: (emailId: string) =>
    client.post("/summarize-email", { email_id: emailId }).then((r) => r.data),

  extractTask: (emailId: string) =>
    client.post("/extract-task", { email_id: emailId }).then((r) => r.data),

  scheduleMeeting: (emailId: string) =>
    client.post("/schedule-meeting", { email_id: emailId }).then((r) => r.data),
};
