export function About() {
  return (
    <section className="grid gap-8 lg:grid-cols-[0.8fr_1.2fr]">
      <div>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400">About</p>
        <h1 className="mt-3 text-4xl font-black">TruthStream explains evidence instead of pretending to know absolute truth.</h1>
        <p className="mt-5 text-lg leading-8 text-slate-600 dark:text-slate-300">
          The goal is to help journalists, researchers, and curious readers rapidly inspect what sources say about a claim.
        </p>
      </div>
      <div className="grid gap-4">
        {[
          ['1', 'Extract claims', 'The backend identifies factual claims from submitted text.'],
          ['2', 'Retrieve evidence', 'Evidence providers collect supporting, contradicting, or neutral source material.'],
          ['3', 'Score confidence', 'The verification engine weighs source credibility, recency, and stance.'],
          ['4', 'Show the work', 'The UI displays confidence, evidence cards, source links, and explanations.'],
        ].map(([step, title, body]) => (
          <article className="rounded-3xl border border-slate-200 bg-white p-6 dark:border-white/10 dark:bg-white/5" key={step}>
            <div className="flex gap-4">
              <span className="grid h-10 w-10 shrink-0 place-items-center rounded-2xl bg-sky-400 font-black text-ink">{step}</span>
              <div>
                <h2 className="text-xl font-black">{title}</h2>
                <p className="mt-2 text-slate-600 dark:text-slate-300">{body}</p>
              </div>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}
