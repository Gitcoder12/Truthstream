import type { VerificationStatus } from '../types/api';

export function statusLabel(status: VerificationStatus): string {
  return status.replace(/_/g, ' ').replace(/^\w/, (match: string) => match.toUpperCase());
}

export function statusTone(status: VerificationStatus): string {
  switch (status) {
    case 'likely_true':
      return 'text-emerald-400 bg-emerald-500/10 ring-emerald-500/30';
    case 'likely_false':
      return 'text-rose-400 bg-rose-500/10 ring-rose-500/30';
    case 'mixed':
      return 'text-amber-300 bg-amber-500/10 ring-amber-500/30';
    default:
      return 'text-sky-300 bg-sky-500/10 ring-sky-500/30';
  }
}
