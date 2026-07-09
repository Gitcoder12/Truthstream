import type { Settings as SettingsType } from '../types/api';

interface SettingsProps {
  settings: SettingsType;
  onSettings: (settings: SettingsType) => void;
}

export function Settings({ settings, onSettings }: SettingsProps) {
  return (
    <section className="mx-auto max-w-3xl space-y-6">
      <div>
        <p className="text-sm uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400">Settings</p>
        <h1 className="mt-3 text-4xl font-black">Configure your TruthStream workspace.</h1>
      </div>
      <div className="rounded-[2rem] border border-slate-200 bg-white p-6 dark:border-white/10 dark:bg-white/5">
        <label className="block text-sm font-bold text-slate-700 dark:text-slate-200" htmlFor="apiBaseUrl">API base URL</label>
        <input
          className="mt-2 w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3 outline-none ring-sky-400/40 focus:ring-4 dark:border-white/10 dark:bg-ink/60"
          id="apiBaseUrl"
          onChange={(event) => onSettings({ ...settings, apiBaseUrl: event.target.value })}
          value={settings.apiBaseUrl}
        />
        <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">Use <code>/api</code> with the Vite proxy, or point directly to your FastAPI server.</p>
      </div>
      <Toggle
        checked={settings.darkMode}
        description="Switch between a light workspace and the default dark TruthStream interface."
        label="Dark mode"
        onChange={(checked) => onSettings({ ...settings, darkMode: checked })}
      />
      <Toggle
        checked={settings.saveHistory}
        description="Store verification history in this browser using localStorage."
        label="Save local history"
        onChange={(checked) => onSettings({ ...settings, saveHistory: checked })}
      />
    </section>
  );
}

function Toggle({ checked, description, label, onChange }: { checked: boolean; description: string; label: string; onChange: (checked: boolean) => void }) {
  return (
    <div className="flex items-center justify-between gap-4 rounded-[2rem] border border-slate-200 bg-white p-6 dark:border-white/10 dark:bg-white/5">
      <div>
        <h2 className="font-black">{label}</h2>
        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">{description}</p>
      </div>
      <button className={`h-8 w-14 rounded-full p-1 transition ${checked ? 'bg-sky-400' : 'bg-slate-300 dark:bg-white/20'}`} onClick={() => onChange(!checked)} type="button">
        <span className={`block h-6 w-6 rounded-full bg-white transition ${checked ? 'translate-x-6' : ''}`} />
      </button>
    </div>
  );
}
