# TruthStream Frontend

React + TypeScript + Tailwind website for the TruthStream verification API.

## Local development

From the repository root, start the backend:

```bash
uvicorn truthstream.api:app --reload
```

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open http://127.0.0.1:5173.

The frontend defaults to the Vite `/api` proxy, which forwards requests to `http://127.0.0.1:8000`.
You can change the API base URL in the Settings page.

## Pages

- Home: product landing page.
- Verify: claim input, loading state, confidence meter, evidence cards, and errors.
- History: locally saved verification results.
- About: explanation of the verification flow.
- Settings: API base URL, dark mode, and local history preferences.
