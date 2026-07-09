import type { Evidence } from '../types/api';

interface EvidenceCardProps {
  evidence: Evidence;
}

export function EvidenceCard({ evidence }: EvidenceCardProps) {
  const tone =
    evidence.stance === 'supports'
      ? 'border-emerald-500/40 bg-emerald-500/10'
      : evidence.stance === 'contradicts'
        ? 'border-rose-500/40 bg-rose-500/10'
        : 'border-sky-500/30 bg-sky-500/10';

  return (
    <article className={`rounded-2xl border p-4 ${tone}`}>
      <div className="mb-2 flex items-start justify-between gap-3">
        <h4 className="font-bold text-slate-950 dark:text-white">{evidence.title}</h4>
        <span className="rounded-full bg-white/60 px-2 py-1 text-xs font-semibold uppercase tracking-wide text-slate-700 dark:bg-white/10 dark:text-slate-200">
          {evidence.stance}
        </span>
      </div>
      <p className="text-sm leading-6 text-slate-700 dark:text-slate-300">{evidence.snippet}</p>
      <div className="mt-4 flex flex-wrap items-center justify-between gap-2 text-xs text-slate-500 dark:text-slate-400">
        <span>{evidence.source.name} · credibility {Math.round(evidence.source.credibility * 100)}%</span>
        {evidence.source.url ? (
          <a className="font-semibold text-sky-500 hover:text-sky-400" href={evidence.source.url} rel="noreferrer" target="_blank">
            Open source ↗
          </a>
        ) : null}
      </div>
    </article>
  );
}
