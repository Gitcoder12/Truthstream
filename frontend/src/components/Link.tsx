import type { ReactNode } from 'react';

interface LinkProps {
  active: boolean;
  children: ReactNode;
  page: string;
}

export function Link({ active, children, page }: LinkProps) {
  return (
    <button
      className={`rounded-full px-4 py-2 text-sm font-semibold transition ${
        active
          ? 'bg-slate-950 text-white shadow-lg dark:bg-white dark:text-ink'
          : 'text-slate-600 hover:bg-slate-200 dark:text-slate-300 dark:hover:bg-white/10'
      }`}
      onClick={() => window.dispatchEvent(new CustomEvent('truthstream:navigate', { detail: page }))}
      type="button"
    >
      {children}
    </button>
  );
}
