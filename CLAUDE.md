# CLAUDE.md — AI Email Assistant

This file provides project context for Claude Code. It is loaded automatically when working in this repository.

---

## Project Overview

AI Email Assistant is an AI-powered SaaS that helps professionals manage email overload. The system integrates with Gmail and uses AI agents to automate inbox management: prioritization, reply generation, summarization, task extraction, meeting scheduling, and follow-up tracking.

**Full product spec:** See [PRD.md](PRD.md)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js, React |
| Backend | Python, FastAPI |
| Automation | n8n workflows + custom AI agent orchestration |
| Database | Supabase (PostgreSQL) |
| Frontend Hosting | Vercel |
| AI / Background Jobs | Modal |

---

## Project Structure

```
project-root/
├── frontend/           # Next.js app (dashboard, inbox view, settings)
├── backend/            # FastAPI services, Gmail integration
│   └── agents/         # Individual AI agent modules
│       ├── email_analyzer.py
│       ├── priority_agent.py
│       ├── reply_agent.py
│       ├── task_agent.py
│       └── meeting_agent.py
├── automation/         # n8n workflow definitions
└── database/           # Supabase schema and migrations
```

---

## Core Integrations

| Service | Purpose |
|---|---|
| Gmail API | Read/send emails, OAuth authentication |
| Slack API | Push extracted tasks and notifications |
| Notion API | Create tasks from email content |
| Google Calendar API | Detect availability, schedule meetings |

---

## AI Agents

Six specialized agents form the core AI system:

| Agent | Role |
|---|---|
| **Email Analyzer** | Parses incoming email content; extracts sender, subject, intent |
| **Priority Agent** | Classifies emails as: `urgent`, `important`, `normal`, `low` |
| **Reply Generation Agent** | Generates reply suggestions using conversation context |
| **Task Extraction Agent** | Detects tasks, deadlines, and owners from email body |
| **Meeting Detection Agent** | Identifies meeting requests; suggests times from Google Calendar |
| **Follow-up Agent** | Detects emails without responses; generates reminders |

---

## AI Model Strategy

| Provider | Use For |
|---|---|
| **Anthropic Claude** | Summarization, classification, task extraction |
| **OpenAI GPT** | Conversational responses, reply generation |

The system selects the best model dynamically based on task type.

---

## API Endpoints

```
POST   /connect-gmail        Connect a Gmail account via OAuth
GET    /emails               Fetch and list processed emails
POST   /generate-reply       Generate a reply suggestion for an email
POST   /summarize-email      Return a summary of a single email
POST   /extract-task         Extract tasks from email content
POST   /schedule-meeting     Detect meeting request and propose times
```

---

## AI Prompt Guidelines

When writing or modifying AI prompts in this project:

1. Responses must be concise and professional
2. Email replies should match the sender's tone (formal vs. casual)
3. Never hallucinate or infer missing information — work only with what's provided
4. Extract structured data (JSON) whenever possible for downstream processing

---

## Development Guidelines

- **Modular agents** — each agent is an independent module with a single responsibility
- **Async processing** — all AI tasks run asynchronously; never block the request thread
- **Queues** — use job queues (e.g., via Modal) for long-running AI operations
- **Decision logging** — log all AI decisions with input/output for transparency and debugging
- **Environment variables** — store all API keys and secrets in `.env`; never hardcode credentials

---

## Security

- OAuth 2.0 for Gmail authentication; never store passwords
- Secure API token storage (encrypted at rest in Supabase)
- Encrypted user email data
- Role-based access control (RBAC) for SaaS multi-tenant version
