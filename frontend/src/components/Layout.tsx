import type { ReactNode } from 'react';
import { Link } from './Link';

interface LayoutProps {
  activePage: string;
  children: ReactNode;
}

const navItems = [
  { id: 'home', label: 'Home' },
  { id: 'verify', label: 'Verify' },
  { id: 'history', label: 'History' },
  { id: 'about', label: 'About' },
  { id: 'settings', label: 'Settings' },
];

export function Layout({ activePage, children }: LayoutProps) {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-950 transition dark:bg-ink dark:text-white">
      <div className="fixed inset-0 -z-10 bg-[radial-gradient(circle_at_top_left,rgba(56,189,248,0.18),transparent_35%),radial-gradient(circle_at_bottom_right,rgba(34,197,94,0.12),transparent_35%)]" />
      <header className="sticky top-0 z-20 border-b border-slate-200/80 bg-white/80 backdrop-blur dark:border-white/10 dark:bg-ink/80">
        <nav className="mx-auto flex max-w-7xl flex-col gap-4 px-4 py-4 sm:flex-row sm:items-center sm:justify-between lg:px-8">
          <button
            className="flex items-center gap-3 text-left"
            onClick={() => window.dispatchEvent(new CustomEvent('truthstream:navigate', { detail: 'home' }))}
            type="button"
          >
            <span className="grid h-10 w-10 place-items-center rounded-2xl bg-sky-400 text-lg font-black text-ink shadow-glow">
              T
            </span>
            <span>
              <span className="block text-lg font-black tracking-tight">TruthStream</span>
              <span className="block text-xs text-slate-500 dark:text-slate-400">Evidence, not vibes.</span>
            </span>
          </button>
          <div className="flex flex-wrap gap-2">
            {navItems.map((item) => (
              <Link key={item.id} active={activePage === item.id} page={item.id}>
                {item.label}
              </Link>
            ))}
          </div>
        </nav>
      </header>
      <main className="mx-auto max-w-7xl px-4 py-8 lg:px-8">{children}</main>
    </div>
  );
}
