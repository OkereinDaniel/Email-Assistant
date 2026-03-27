-- AI Email Assistant — Supabase Schema
-- Run this in the Supabase SQL editor to initialize the database.

-- ─────────────────────────────────────────
-- Users (extends Supabase auth.users)
-- ─────────────────────────────────────────
create table if not exists public.profiles (
  id            uuid primary key references auth.users (id) on delete cascade,
  email         text not null,
  full_name     text,
  avatar_url    text,
  -- Gmail OAuth token (encrypted at rest by Supabase Vault in production)
  gmail_token   jsonb,
  -- Automation preferences
  mode          text not null default 'suggest' check (mode in ('suggest', 'auto')),
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

-- ─────────────────────────────────────────
-- Emails (cached from Gmail)
-- ─────────────────────────────────────────
create table if not exists public.emails (
  id            text primary key,           -- Gmail message ID
  user_id       uuid not null references public.profiles (id) on delete cascade,
  subject       text,
  sender        text,
  recipient     text,
  snippet       text,
  body          text,
  received_at   timestamptz,
  is_read       boolean not null default false,
  label_ids     text[],
  -- AI enrichment
  intent        text,
  tone          text,
  priority      text check (priority in ('urgent', 'important', 'normal', 'low')),
  priority_reason text,
  summary       text,
  created_at    timestamptz not null default now()
);

create index if not exists emails_user_id_idx on public.emails (user_id);
create index if not exists emails_priority_idx on public.emails (user_id, priority);

-- ─────────────────────────────────────────
-- Tasks (extracted from emails)
-- ─────────────────────────────────────────
create table if not exists public.tasks (
  id            uuid primary key default gen_random_uuid(),
  user_id       uuid not null references public.profiles (id) on delete cascade,
  email_id      text references public.emails (id) on delete set null,
  title         text not null,
  description   text,
  owner         text,
  due_date      date,
  priority      text check (priority in ('high', 'medium', 'low')),
  status        text not null default 'pending' check (status in ('pending', 'done', 'dismissed')),
  -- Integration sync
  notion_page_id text,
  slack_message_ts text,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

create index if not exists tasks_user_id_idx on public.tasks (user_id);

-- ─────────────────────────────────────────
-- AI Action Log (for transparency/debugging)
-- ─────────────────────────────────────────
create table if not exists public.ai_action_logs (
  id            uuid primary key default gen_random_uuid(),
  user_id       uuid not null references public.profiles (id) on delete cascade,
  email_id      text,
  action_type   text not null,  -- e.g. 'reply_generated', 'task_extracted', 'priority_classified'
  model         text,
  input_tokens  int,
  output_tokens int,
  result        jsonb,
  created_at    timestamptz not null default now()
);

-- ─────────────────────────────────────────
-- Row Level Security
-- ─────────────────────────────────────────
alter table public.profiles enable row level security;
alter table public.emails enable row level security;
alter table public.tasks enable row level security;
alter table public.ai_action_logs enable row level security;

-- Users can only access their own data
create policy "profiles: own row" on public.profiles
  for all using (auth.uid() = id);

create policy "emails: own rows" on public.emails
  for all using (auth.uid() = user_id);

create policy "tasks: own rows" on public.tasks
  for all using (auth.uid() = user_id);

create policy "ai_action_logs: own rows" on public.ai_action_logs
  for all using (auth.uid() = user_id);

-- ─────────────────────────────────────────
-- Auto-update updated_at timestamps
-- ─────────────────────────────────────────
create or replace function public.set_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create trigger profiles_updated_at before update on public.profiles
  for each row execute function public.set_updated_at();

create trigger tasks_updated_at before update on public.tasks
  for each row execute function public.set_updated_at();
