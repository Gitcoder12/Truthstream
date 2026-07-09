import type { VerificationStatus } from '../types/api';
import { statusLabel, statusTone } from '../lib/format';

interface ConfidenceMeterProps {
  confidence: number;
  status: VerificationStatus;
}

export function ConfidenceMeter({ confidence, status }: ConfidenceMeterProps) {
  const percent = Math.round(confidence * 100);

  return (
    <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm dark:border-white/10 dark:bg-white/5">
      <div className="mb-4 flex items-center justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400">Confidence</p>
          <p className="text-5xl font-black tracking-tight">{percent}%</p>
        </div>
        <span className={`rounded-full px-3 py-1 text-sm font-bold ring-1 ${statusTone(status)}`}>
          {statusLabel(status)}
        </span>
      </div>
      <div className="h-4 overflow-hidden rounded-full bg-slate-200 dark:bg-white/10">
        <div
          className="h-full rounded-full bg-gradient-to-r from-rose-500 via-amber-400 to-emerald-400 transition-all duration-700"
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
}
