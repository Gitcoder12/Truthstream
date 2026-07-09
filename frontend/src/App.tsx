import { useEffect, useMemo, useState } from 'react';
import { Layout } from './components/Layout';
import { About } from './pages/About';
import { History } from './pages/History';
import { Home } from './pages/Home';
import { Settings } from './pages/Settings';
import { Verify } from './pages/Verify';
import { clearHistory, loadHistory, loadSettings, saveHistory, saveSettings } from './lib/storage';
import type { HistoryItem, Settings as SettingsType } from './types/api';

type Page = 'home' | 'verify' | 'history' | 'about' | 'settings';

export function App() {
  const [page, setPage] = useState<Page>('home');
  const [settings, setSettings] = useState<SettingsType>(() => loadSettings());
  const [history, setHistory] = useState<HistoryItem[]>(() => loadHistory());

  useEffect(() => {
    const handler = (event: Event) => {
      const nextPage = (event as CustomEvent<Page>).detail;
      setPage(nextPage);
    };
    window.addEventListener('truthstream:navigate', handler);
    return () => window.removeEventListener('truthstream:navigate', handler);
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', settings.darkMode);
    saveSettings(settings);
  }, [settings]);

  useEffect(() => {
    saveHistory(history);
  }, [history]);

  const content = useMemo(() => {
    switch (page) {
      case 'verify':
        return (
          <Verify
            onHistoryItem={(item) => setHistory((items) => [item, ...items].slice(0, 25))}
            settings={settings}
          />
        );
      case 'history':
        return <History history={history} onClear={() => { clearHistory(); setHistory([]); }} />;
      case 'about':
        return <About />;
      case 'settings':
        return <Settings onSettings={setSettings} settings={settings} />;
      default:
        return <Home onVerify={() => setPage('verify')} />;
    }
  }, [history, page, settings]);

  return <Layout activePage={page}>{content}</Layout>;
}
