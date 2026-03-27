import Link from "next/link";

const navItems = [
  { label: "Inbox", href: "/dashboard", icon: "📥" },
  { label: "Tasks", href: "/dashboard/tasks", icon: "✅" },
  { label: "Meetings", href: "/dashboard/meetings", icon: "📅" },
  { label: "Settings", href: "/dashboard/settings", icon: "⚙️" },
];

export default function Sidebar() {
  return (
    <aside className="w-56 bg-white border-r border-slate-200 flex flex-col py-6 px-3">
      <div className="px-3 mb-8">
        <span className="text-brand-600 font-bold text-lg">MailAI</span>
      </div>
      <nav className="flex flex-col gap-1">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="flex items-center gap-3 px-3 py-2 rounded-lg text-slate-600 hover:bg-slate-100 hover:text-slate-900 text-sm font-medium transition-colors"
          >
            <span>{item.icon}</span>
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
