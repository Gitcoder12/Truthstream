import { ResultPanel } from '../components/ResultPanel';
import type { HistoryItem } from '../types/api';

interface HistoryProps {
  history: HistoryItem[];
  onClear: () => void;
}

export function History({ history, onClear }: HistoryProps) {
  return (
    <section className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400">History</p>
          <h1 className="mt-3 text-4xl font-black">Recent verifications</h1>
        </div>
        <button className="rounded-full border border-slate-300 px-5 py-3 font-bold text-slate-700 transition hover:bg-slate-100 disabled:opacity-50 dark:border-white/15 dark:text-white dark:hover:bg-white/10" disabled={!history.length} onClick={onClear} type="button">
          Clear history
        </button>
      </div>
      {history.length ? (
        <div className="space-y-8">
          {history.map((item) => (
            <article className="space-y-5 rounded-[2rem] border border-slate-200 bg-white p-5 dark:border-white/10 dark:bg-white/5" key={item.id}>
              <div>
                <p className="text-sm text-slate-500 dark:text-slate-400">{new Date(item.createdAt).toLocaleString()}</p>
                <h2 className="mt-1 text-2xl font-black">{item.claimText}</h2>
              </div>
              {item.results.map((result, index) => (
                <ResultPanel key={`${item.id}-${index}`} result={result} />
              ))}
            </article>
          ))}
        </div>
      ) : (
        <div className="rounded-[2rem] border border-dashed border-slate-300 p-12 text-center dark:border-white/10">
          <p className="text-5xl">🕓</p>
          <h2 className="mt-4 text-2xl font-black">No saved verifications yet.</h2>
          <p className="mt-2 text-slate-500 dark:text-slate-400">Run a claim from the Verify page to build your local history.</p>
        </div>
      )}
    </section>
  );
}
