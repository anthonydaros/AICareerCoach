"use client";

/**
 * React hook for managing career analysis state.
 */

import { useState, useCallback } from "react";
import {
  uploadResume,
  analyzeCareer,
  generateInterviewPrep,
  generateCoachingTips,
  ApiClientError,
} from "@/lib/api";
import type {
  AnalysisState,
  AnalysisStatus,
  UploadResponse,
  AnalyzeResponse,
  InterviewPrepResponse,
  CoachingTipsResponse,
  Job,
} from "@/lib/types";

const initialState: AnalysisState = {
  status: "idle",
  resumeText: null,
  resumeFilename: null,
  result: null,
  interviewPrep: null,
  coachingTips: null,
  error: null,
};

export function useAnalysis() {
  const [state, setState] = useState<AnalysisState>(initialState);

  /**
   * Set the analysis status.
   */
  const setStatus = useCallback((status: AnalysisStatus) => {
    setState((prev) => ({ ...prev, status, error: null }));
  }, []);

  /**
   * Set an error message.
   */
  const setError = useCallback((error: string) => {
    setState((prev) => ({ ...prev, status: "error", error }));
  }, []);

  /**
   * Handle file upload.
   */
  const handleFileUpload = useCallback(
    async (file: File): Promise<UploadResponse | null> => {
      setState((prev) => ({ ...prev, status: "uploading", error: null }));

      try {
        const response = await uploadResume(file);

        setState((prev) => ({
          ...prev,
          status: "idle",
          resumeText: response.text_content,
          resumeFilename: response.filename,
        }));

        return response;
      } catch (error) {
        const message =
          error instanceof ApiClientError
            ? error.message
            : "Failed to upload file";

        setState((prev) => ({
          ...prev,
          status: "error",
          error: message,
        }));

        return null;
      }
    },
    []
  );

  /**
   * Set resume text directly (for pasted text).
   */
  const setResumeText = useCallback((text: string) => {
    setState((prev) => ({
      ...prev,
      resumeText: text,
      resumeFilename: null,
    }));
  }, []);

  /**
   * Run the full analysis.
   */
  const runAnalysis = useCallback(
    async (jobs: Job[]): Promise<AnalyzeResponse | null> => {
      if (!state.resumeText) {
        setError("Please upload a resume first");
        return null;
      }

      if (jobs.length === 0) {
        setError("Please add at least one job posting");
        return null;
      }

      setState((prev) => ({ ...prev, status: "analyzing", error: null }));

      try {
        const result = await analyzeCareer({
          resume_text: state.resumeText,
          job_postings: jobs.map((j) => ({ id: j.id, text: j.text })),
        });

        setState((prev) => ({
          ...prev,
          status: "done",
          result,
        }));

        return result;
      } catch (error) {
        const message =
          error instanceof ApiClientError
            ? error.message
            : "Analysis failed";

        setState((prev) => ({
          ...prev,
          status: "error",
          error: message,
        }));

        return null;
      }
    },
    [state.resumeText, setError]
  );

  /**
   * Generate interview prep for a specific job.
   */
  const getInterviewPrep = useCallback(
    async (
      jobText: string,
      skillGaps?: string[]
    ): Promise<InterviewPrepResponse | null> => {
      if (!state.resumeText) {
        setError("Please upload a resume first");
        return null;
      }

      try {
        const response = await generateInterviewPrep({
          resume_text: state.resumeText,
          job_text: jobText,
          skill_gaps: skillGaps,
        });

        setState((prev) => ({
          ...prev,
          interviewPrep: response,
        }));

        return response;
      } catch (error) {
        const message =
          error instanceof ApiClientError
            ? error.message
            : "Failed to generate interview prep";

        setError(message);
        return null;
      }
    },
    [state.resumeText, setError]
  );

  /**
   * Generate coaching tips.
   */
  const getCoachingTips = useCallback(
    async (jobs: Job[]): Promise<CoachingTipsResponse | null> => {
      if (!state.resumeText) {
        setError("Please upload a resume first");
        return null;
      }

      try {
        const response = await generateCoachingTips({
          resume_text: state.resumeText,
          job_postings: jobs.map((j) => ({ id: j.id, text: j.text })),
        });

        setState((prev) => ({
          ...prev,
          coachingTips: response,
        }));

        return response;
      } catch (error) {
        const message =
          error instanceof ApiClientError
            ? error.message
            : "Failed to generate coaching tips";

        setError(message);
        return null;
      }
    },
    [state.resumeText, setError]
  );

  /**
   * Reset all state.
   */
  const reset = useCallback(() => {
    setState(initialState);
  }, []);

  /**
   * Clear just the error.
   */
  const clearError = useCallback(() => {
    setState((prev) => ({ ...prev, error: null }));
  }, []);

  return {
    // State
    ...state,

    // Computed
    hasResume: !!state.resumeText,
    hasResult: !!state.result,
    isLoading: state.status === "uploading" || state.status === "analyzing",

    // Actions
    handleFileUpload,
    setResumeText,
    runAnalysis,
    getInterviewPrep,
    getCoachingTips,
    reset,
    clearError,
    setStatus,
    setError,
  };
}
