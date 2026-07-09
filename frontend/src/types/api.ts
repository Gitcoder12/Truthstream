export type EvidenceStance = 'supports' | 'contradicts' | 'neutral';
export type VerificationStatus =
  | 'likely_true'
  | 'mixed'
  | 'insufficient_evidence'
  | 'likely_false';

export interface Source {
  name: string;
  url: string | null;
  credibility: number;
}

export interface Evidence {
  source: Source;
  title: string;
  snippet: string;
  stance: EvidenceStance;
  recency_score: number;
}

export interface Claim {
  text: string;
  entities: string[];
}

export interface EvidenceSummary {
  supporting_count: number;
  contradicting_count: number;
  neutral_count: number;
  supporting_weight: number;
  contradicting_weight: number;
}

export interface VerificationResult {
  claim: Claim;
  confidence_score: number;
  status: VerificationStatus;
  supporting_evidence: Evidence[];
  contradicting_evidence: Evidence[];
  neutral_evidence: Evidence[];
  explanation: string;
  evidence_summary: EvidenceSummary;
}

export interface HistoryItem {
  id: string;
  claimText: string;
  createdAt: string;
  results: VerificationResult[];
}

export interface Settings {
  apiBaseUrl: string;
  darkMode: boolean;
  saveHistory: boolean;
}
