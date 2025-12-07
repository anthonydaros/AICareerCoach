"use client";

import { Activity, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";
import type { AnalyzeResponse, AnalysisStatus, Job } from "@/lib/types";
import { TerminalTypewriter } from "./TerminalTypewriter";
import { ScoreCard } from "./ScoreCard";

interface LivePreviewProps {
  status: AnalysisStatus;
  result: AnalyzeResponse | null;
  error: string | null;
  resumeText?: string;
  jobs?: Job[];
}

export function LivePreview({ status, result, error, resumeText, jobs }: LivePreviewProps) {
  const renderIdleState = () => (
    <div className="space-y-4">
      <div className="text-muted-foreground/50 pb-2 border-b border-dashed border-border/30 italic">
        // System awaiting input stream...
        <br />
        // Ready to analyze resume vs job description
      </div>

      <div className="opacity-80 font-mono text-sm leading-relaxed">
        <span className="text-neon-pink">const</span>{" "}
        <span className="text-neon-cyan">analysis_result</span> ={" "}
        <span className="text-foreground">{"{"}</span>
        <div className="pl-6 border-l border-border/20 ml-1">
          <div>
            <span className="text-neon-yellow">match_score</span>:{" "}
            <span className="text-muted-foreground">null</span>,
          </div>
          <div>
            <span className="text-neon-yellow">missing_skills</span>:{" "}
            <span className="text-foreground">[]</span>,
          </div>
          <div>
            <span className="text-neon-yellow">recommendations</span>:{" "}
            <span className="text-foreground">[]</span>,
          </div>
          <div className="text-muted-foreground/40">// ... awaiting data</div>
        </div>
        <span className="text-foreground">{"}"}</span>
      </div>
    </div>
  );

  const renderLoadingState = () => (
    <TerminalTypewriter status={status as "uploading" | "analyzing"} />
  );

  const renderErrorState = () => (
    <div
      className="flex flex-col items-center justify-center h-full gap-4"
      role="alert"
      aria-live="assertive"
    >
      <AlertCircle className="h-12 w-12 text-red-500" aria-hidden="true" />
      <div className="text-center">
        <p className="text-red-500 font-display font-bold tracking-widest uppercase">
          ERROR DETECTED
        </p>
        <p className="text-sm text-muted-foreground font-mono mt-2 max-w-[300px]">
          {error}
        </p>
      </div>
    </div>
  );

  const renderResultState = () => {
    if (!result) return null;

    return (
      <ScoreCard
        result={result}
        resumeText={resumeText}
        jobs={jobs?.map(j => ({ id: j.id, text: j.text }))}
      />
    );
  };

  const renderContent = () => {
    if (status === "error") return renderErrorState();
    if (status === "uploading" || status === "analyzing") return renderLoadingState();
    if (status === "done" && result) return renderResultState();
    return renderIdleState();
  };

  const isLoading = status === "uploading" || status === "analyzing";

  const getStatusMessage = () => {
    if (status === "error") return "Analysis error occurred";
    if (status === "uploading") return "Uploading resume";
    if (status === "analyzing") return "Analyzing data";
    if (status === "done") return "Analysis complete";
    return "Awaiting input";
  };

  return (
    <div
      className="h-full flex flex-col font-mono text-sm bg-background/40 backdrop-blur border-l border-border/40"
      role="region"
      aria-label="Analysis results"
      aria-busy={isLoading}
    >
      {/* Screen reader status announcements */}
      <div className="sr-only" aria-live="polite" aria-atomic="true">
        {getStatusMessage()}
      </div>

      <div className="flex items-center justify-between border-b border-border/40 px-4 py-3 bg-muted/10">
        <div className="flex items-center gap-2">
          <Activity
            className={cn(
              "h-4 w-4",
              isLoading
                ? "text-neon-cyan animate-pulse"
                : status === "done"
                  ? "text-neon-green"
                  : "text-neon-pink animate-pulse"
            )}
            aria-hidden="true"
          />
          <span className="font-display font-bold tracking-wide text-foreground">
            LIVE OUTPUT STREAM
          </span>
        </div>
        <div
          className="flex items-center gap-2 text-[10px] text-muted-foreground uppercase"
          role="status"
          aria-live="polite"
        >
          <div
            className={cn(
              "h-1.5 w-1.5 rounded-full",
              status === "error" ? "bg-red-500" : "bg-neon-green/80"
            )}
            aria-hidden="true"
          />
          <span>{status === "error" ? "Error" : "Connected"}</span>
        </div>
      </div>

      <div className="flex-1 p-4 overflow-auto scrollbar-thin scrollbar-thumb-muted-foreground/20 scrollbar-track-transparent relative">
        {renderContent()}

        {/* Scanline Effect Overlay */}
        <div
          className="absolute inset-0 pointer-events-none bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.1)_50%),linear-gradient(90deg,rgba(255,0,0,0.03),rgba(0,255,0,0.01),rgba(0,0,255,0.03))] z-50 bg-[length:100%_2px,3px_100%] opacity-20 user-select-none"
          aria-hidden="true"
        />
      </div>
    </div>
  );
}
