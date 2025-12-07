/**
 * TypeScript types matching backend API schemas.
 */

// ============================================
// Request Types
// ============================================

export interface JobPostingInput {
  id: string;
  text: string;
}

export interface AnalyzeRequest {
  resume_text: string;
  job_postings: JobPostingInput[];
}

export interface ATSScoreRequest {
  resume_text: string;
  job_text: string;
}

export interface InterviewPrepRequest {
  resume_text: string;
  job_text: string;
  skill_gaps?: string[];
}

export interface CoachingTipsRequest {
  resume_text: string;
  job_postings: JobPostingInput[];
  match_results?: Record<string, unknown>[];
}

// ============================================
// Response Types
// ============================================

export interface UploadResponse {
  filename: string;
  content_type: string;
  text_content: string;
  char_count: number;
}

export type MatchLevel = "excellent" | "good" | "fair" | "poor";

export interface ATSResult {
  total_score: number;
  skill_score: number;
  experience_score: number;
  education_score: number;
  certification_score: number;
  keyword_score: number;
  matched_keywords: string[];
  missing_keywords: string[];
  format_issues: string[];
  improvement_suggestions: string[];
}

export interface SkillGap {
  skill: string;
  is_required: boolean;
  suggestion: string;
  learning_resources: string[];
}

export interface JobMatch {
  job_id: string;
  job_title: string;
  company: string | null;
  match_percentage: number;
  match_level: MatchLevel;
  matched_skills: string[];
  missing_skills: string[];
  skill_gaps: SkillGap[];
  strengths: string[];
  concerns: string[];
  is_best_fit: boolean;
}

export interface BestFit {
  job_id: string;
  job_title: string;
  match_percentage: number;
  recommendation: string;
}

export interface AnalyzeResponse {
  ats_result: ATSResult;
  job_matches: JobMatch[];
  best_fit: BestFit | null;
  interview_prep?: InterviewPrepResponse | null;
  coaching_tips?: CoachingTipsResponse | null;
}

export interface InterviewQuestion {
  question: string;
  category: string;
  why_asked: string;
  what_to_say: string[];
  what_to_avoid: string[];
}

export interface InterviewPrepResponse {
  job_title: string;
  questions: InterviewQuestion[];
}

export interface CoachingTip {
  category: string;
  title: string;
  description: string;
  action_items: string[];
  priority: string;
}

export interface CoachingTipsResponse {
  tips: CoachingTip[];
}

export interface ApiError {
  detail: string;
  error_type?: string;
}

// ============================================
// Application State Types
// ============================================

export type AnalysisStatus = "idle" | "uploading" | "analyzing" | "done" | "error";

export interface AnalysisState {
  status: AnalysisStatus;
  resumeText: string | null;
  resumeFilename: string | null;
  result: AnalyzeResponse | null;
  interviewPrep: InterviewPrepResponse | null;
  coachingTips: CoachingTipsResponse | null;
  error: string | null;
}

export interface Job {
  id: string;
  text: string;
  title?: string;
}
