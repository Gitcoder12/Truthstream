import type { VerificationResult } from '../types/api';

export async function verifyClaim(apiBaseUrl: string, text: string): Promise<VerificationResult[]> {
  const response = await fetch(`${apiBaseUrl}/verify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    const details = await safeError(response);
    throw new Error(details || `Verification failed with status ${response.status}`);
  }

  return (await response.json()) as VerificationResult[];
}

async function safeError(response: Response): Promise<string | null> {
  try {
    const body = await response.json();
    return typeof body.detail === 'string' ? body.detail : null;
  } catch {
    return null;
  }
}
