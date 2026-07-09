import { ConfidenceMeter } from './ConfidenceMeter';
import { EvidenceCard } from './EvidenceCard';
import type { VerificationResult } from '../types/api';

interface ResultPanelProps {
  result: VerificationResult;
}

export function ResultPanel({ result }: ResultPanelProps) {
  const groups = [
    { title: 'Supporting evidence', items: result.supporting_evidence },
    { title: 'Contradicting evidence', items: result.contradicting_evidence },
    { title: 'Neutral evidence', items: result.neutral_evidence },
  ];

  return (
    <section className="space-y-6">
      <ConfidenceMeter confidence={result.confidence_score} status={result.status} />
      <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm dark:border-white/10 dark:bg-white/5">
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400">Claim</p>
        <h2 className="mt-2 text-2xl font-black">{result.claim.text}</h2>
        <p className="mt-4 leading-7 text-slate-700 dark:text-slate-300">{result.explanation}</p>
        <div className="mt-4 grid gap-3 sm:grid-cols-3">
          <Metric label="Supports" value={result.evidence_summary.supporting_count} />
          <Metric label="Contradicts" value={result.evidence_summary.contradicting_count} />
          <Metric label="Neutral" value={result.evidence_summary.neutral_count} />
        </div>
      </div>
      {groups.map((group) => (
        <div key={group.title} className="space-y-3">
          <h3 className="text-lg font-black">{group.title}</h3>
          {group.items.length ? (
            <div className="grid gap-4 lg:grid-cols-2">
              {group.items.map((item, index) => (
                <EvidenceCard evidence={item} key={`${item.title}-${index}`} />
              ))}
            </div>
          ) : (
            <p className="rounded-2xl border border-dashed border-slate-300 p-4 text-sm text-slate-500 dark:border-white/10 dark:text-slate-400">
              No {group.title.toLowerCase()} found for this claim.
            </p>
          )}
        </div>
      ))}
    </section>
  );
}

function Metric({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-2xl bg-slate-100 p-4 dark:bg-white/10">
      <p className="text-xs uppercase tracking-[0.2em] text-slate-500 dark:text-slate-400">{label}</p>
      <p className="text-2xl font-black">{value}</p>
    </div>
  );
}
