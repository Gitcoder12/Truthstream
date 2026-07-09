interface HomeProps {
  onVerify: () => void;
}

export function Home({ onVerify }: HomeProps) {
  return (
    <div className="grid items-center gap-10 py-12 lg:grid-cols-[1.05fr_0.95fr] lg:py-20">
      <section>
        <p className="mb-4 inline-flex rounded-full border border-sky-400/30 bg-sky-400/10 px-4 py-2 text-sm font-bold text-sky-500 dark:text-sky-300">
          Evidence-centered verification for fast-moving information
        </p>
        <h1 className="max-w-4xl text-5xl font-black tracking-tight sm:text-6xl lg:text-7xl">
          Verify claims with sources, confidence, and context.
        </h1>
        <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-600 dark:text-slate-300">
          TruthStream turns a claim into a transparent evidence report. It shows what supports the claim, what contradicts it, and how confident the system is.
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          <button className="rounded-full bg-sky-400 px-6 py-3 font-black text-ink shadow-glow transition hover:-translate-y-0.5" onClick={onVerify} type="button">
            Verify a claim
          </button>
          <button className="rounded-full border border-slate-300 px-6 py-3 font-bold text-slate-700 transition hover:bg-slate-100 dark:border-white/15 dark:text-white dark:hover:bg-white/10" onClick={() => window.dispatchEvent(new CustomEvent('truthstream:navigate', { detail: 'about' }))} type="button">
            Learn how it works
          </button>
        </div>
      </section>
      <section className="rounded-[2rem] border border-white/10 bg-slate-950 p-6 text-white shadow-2xl shadow-sky-950/20">
        <div className="rounded-3xl bg-white/5 p-5">
          <p className="text-sm text-slate-400">Try typing</p>
          <p className="mt-2 rounded-2xl bg-white/10 p-4 font-mono text-lg">“India banned AI”</p>
        </div>
        <div className="mt-6 grid gap-4 sm:grid-cols-3">
          {[
            ['Evidence', '3 sources'],
            ['Confidence', '72%'],
            ['Status', 'Mixed'],
          ].map(([label, value]) => (
            <div className="rounded-2xl bg-white/10 p-4" key={label}>
              <p className="text-xs uppercase tracking-[0.2em] text-slate-400">{label}</p>
              <p className="mt-2 text-2xl font-black">{value}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
