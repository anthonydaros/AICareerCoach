/**
 * API client for the AI Career Coach backend.
 */

import type {
  UploadResponse,
  AnalyzeRequest,
  AnalyzeResponse,
  ATSScoreRequest,
  ATSResult,
  InterviewPrepRequest,
  InterviewPrepResponse,
  CoachingTipsRequest,
  CoachingTipsResponse,
  JobMatch,
  ApiError,
} from "./types";

// API base URL from environment or default
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Custom error class for API errors.
 */
export class ApiClientError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public details?: string
  ) {
    super(message);
    this.name = "ApiClientError";
  }
}

/**
 * Make an API request with error handling.
 */
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
      },
    });

    if (!response.ok) {
      let errorMessage = `Request failed: ${response.statusText}`;
      try {
        const errorData: ApiError = await response.json();
        errorMessage = errorData.detail || errorMessage;
      } catch {
        // Use default error message
      }
      throw new ApiClientError(errorMessage, response.status);
    }

    return response.json();
  } catch (error) {
    if (error instanceof ApiClientError) {
      throw error;
    }
    throw new ApiClientError(
      error instanceof Error ? error.message : "Network error",
      0
    );
  }
}

/**
 * Check API health status.
 */
export async function checkHealth(): Promise<{ status: string }> {
  return apiRequest("/health");
}

/**
 * Upload a resume file and extract text.
 */
export async function uploadResume(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  return apiRequest("/upload", {
    method: "POST",
    body: formData,
  });
}

/**
 * Perform full career analysis.
 */
export async function analyzeCareer(
  request: AnalyzeRequest
): Promise<AnalyzeResponse> {
  return apiRequest("/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
}

/**
 * Calculate ATS score only.
 */
export async function calculateATSScore(
  request: ATSScoreRequest
): Promise<ATSResult> {
  return apiRequest("/ats-score", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
}

/**
 * Match resume against multiple jobs.
 */
export async function matchJobs(
  resumeText: string,
  jobPostings: { id: string; text: string }[]
): Promise<JobMatch[]> {
  return apiRequest("/match-jobs", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      resume_text: resumeText,
      job_postings: jobPostings,
    }),
  });
}

/**
 * Generate interview preparation questions.
 */
export async function generateInterviewPrep(
  request: InterviewPrepRequest
): Promise<InterviewPrepResponse> {
  return apiRequest("/interview-prep", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
}

/**
 * Generate career coaching tips.
 */
export async function generateCoachingTips(
  request: CoachingTipsRequest
): Promise<CoachingTipsResponse> {
  return apiRequest("/coaching-tips", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
}

// Export API base for reference
export { API_BASE };
