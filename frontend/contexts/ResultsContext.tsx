"use client";

import { createContext, useContext, useState, useCallback, ReactNode } from "react";
import type {
  AnalyzeResponse,
  InterviewPrepResponse,
  CoachingTipsResponse,
  Job,
} from "@/lib/types";

interface ResultsState {
  result: AnalyzeResponse | null;
  interviewPrep: InterviewPrepResponse | null;
  coachingTips: CoachingTipsResponse | null;
  resumeText: string | null;
  jobs: Job[];
}

interface ResultsContextType extends ResultsState {
  setResults: (
    result: AnalyzeResponse,
    resumeText: string,
    jobs: Job[]
  ) => void;
  setInterviewPrep: (interviewPrep: InterviewPrepResponse) => void;
  setCoachingTips: (coachingTips: CoachingTipsResponse) => void;
  clearResults: () => void;
  hasResults: boolean;
}

const initialState: ResultsState = {
  result: null,
  interviewPrep: null,
  coachingTips: null,
  resumeText: null,
  jobs: [],
};

const ResultsContext = createContext<ResultsContextType | undefined>(undefined);

export function ResultsProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<ResultsState>(initialState);

  const setResults = useCallback(
    (result: AnalyzeResponse, resumeText: string, jobs: Job[]) => {
      setState((prev) => ({
        ...prev,
        result,
        resumeText,
        jobs,
      }));
    },
    []
  );

  const setInterviewPrep = useCallback((interviewPrep: InterviewPrepResponse) => {
    setState((prev) => ({
      ...prev,
      interviewPrep,
    }));
  }, []);

  const setCoachingTips = useCallback((coachingTips: CoachingTipsResponse) => {
    setState((prev) => ({
      ...prev,
      coachingTips,
    }));
  }, []);

  const clearResults = useCallback(() => {
    setState(initialState);
  }, []);

  const value: ResultsContextType = {
    ...state,
    setResults,
    setInterviewPrep,
    setCoachingTips,
    clearResults,
    hasResults: !!state.result,
  };

  return (
    <ResultsContext.Provider value={value}>{children}</ResultsContext.Provider>
  );
}

export function useResults(): ResultsContextType {
  const context = useContext(ResultsContext);
  if (context === undefined) {
    throw new Error("useResults must be used within a ResultsProvider");
  }
  return context;
}
