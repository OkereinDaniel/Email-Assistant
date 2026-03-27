import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center px-4">
      <div className="text-center max-w-2xl">
        <h1 className="text-5xl font-bold text-white mb-4">
          AI Email Assistant
        </h1>
        <p className="text-slate-400 text-xl mb-10">
          Reduce inbox overload with AI-powered prioritization, replies,
          summaries, and task extraction — connected to Gmail.
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            href="/dashboard"
            className="bg-brand-600 hover:bg-brand-700 text-white font-semibold px-8 py-3 rounded-lg transition-colors"
          >
            Go to Dashboard
          </Link>
          <Link
            href="/auth/login"
            className="border border-slate-600 hover:border-slate-400 text-slate-300 hover:text-white font-semibold px-8 py-3 rounded-lg transition-colors"
          >
            Sign In
          </Link>
        </div>
      </div>
    </main>
  );
}
