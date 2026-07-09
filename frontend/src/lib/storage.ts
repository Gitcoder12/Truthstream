import type { HistoryItem, Settings } from '../types/api';

const SETTINGS_KEY = 'truthstream.settings';
const HISTORY_KEY = 'truthstream.history';

export const defaultSettings: Settings = {
  apiBaseUrl: '/api',
  darkMode: true,
  saveHistory: true,
};

export function loadSettings(): Settings {
  const raw = localStorage.getItem(SETTINGS_KEY);
  if (!raw) return defaultSettings;

  try {
    return { ...defaultSettings, ...JSON.parse(raw) };
  } catch {
    return defaultSettings;
  }
}

export function saveSettings(settings: Settings): void {
  localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
}

export function loadHistory(): HistoryItem[] {
  const raw = localStorage.getItem(HISTORY_KEY);
  if (!raw) return [];

  try {
    return JSON.parse(raw) as HistoryItem[];
  } catch {
    return [];
  }
}

export function saveHistory(history: HistoryItem[]): void {
  localStorage.setItem(HISTORY_KEY, JSON.stringify(history.slice(0, 25)));
}

export function clearHistory(): void {
  localStorage.removeItem(HISTORY_KEY);
}
