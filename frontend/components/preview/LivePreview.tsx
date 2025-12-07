"use client";

import { Activity, AlertCircle, CheckCircle2, Target, TrendingUp, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";
import type { AnalyzeResponse, AnalysisStatus } from "@/lib/types";

interface LivePreviewProps {
    status: AnalysisStatus;
    result: AnalyzeResponse | null;
    error: string | null;
}

export function LivePreview({ status, result, error }: LivePreviewProps) {
    const renderIdleState = () => (
        <div className="space-y-4">
            <div className="text-muted-foreground/50 pb-2 border-b border-dashed border-border/30 italic">
                // System awaiting input stream...
                <br />
                // Ready to analyze resume vs job description
            </div>

            <div className="opacity-80 font-mono text-sm leading-relaxed">
                <span className="text-neon-pink">const</span> <span className="text-neon-cyan">analysis_result</span> = <span className="text-foreground">{"{"}</span>
                <div className="pl-6 border-l border-border/20 ml-1">
                    <div>
                        <span className="text-neon-yellow">match_score</span>: <span className="text-muted-foreground">null</span>,
                    </div>
                    <div>
                        <span className="text-neon-yellow">missing_skills</span>: <span className="text-foreground">[]</span>,
                    </div>
                    <div>
                        <span className="text-neon-yellow">recommendations</span>: <span className="text-foreground">[]</span>,
                    </div>
                    <div className="text-muted-foreground/40">
                        // ... awaiting data
                    </div>
                </div>
                <span className="text-foreground">{"}"}</span>
            </div>
        </div>
    );

    const renderLoadingState = () => (
        <div className="flex flex-col items-center justify-center h-full gap-4">
            <Loader2 className="h-12 w-12 text-neon-cyan animate-spin" />
            <div className="text-center">
                <p className="text-neon-cyan font-display font-bold tracking-widest uppercase">
                    {status === "uploading" ? "UPLOADING RESUME..." : "ANALYZING DATA..."}
                </p>
                <p className="text-[10px] text-muted-foreground font-mono mt-2">
                    {status === "uploading"
                        ? "// Extracting text content"
                        : "// Processing with AI engine"}
                </p>
            </div>
        </div>
    );

    const renderErrorState = () => (
        <div className="flex flex-col items-center justify-center h-full gap-4">
            <AlertCircle className="h-12 w-12 text-red-500" />
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

    const getScoreColor = (score: number) => {
        if (score >= 80) return "text-neon-green";
        if (score >= 60) return "text-neon-cyan";
        if (score >= 40) return "text-neon-yellow";
        return "text-red-500";
    };

    const getMatchLevelColor = (level: string) => {
        switch (level) {
            case "excellent": return "text-neon-green";
            case "good": return "text-neon-cyan";
            case "fair": return "text-neon-yellow";
            default: return "text-red-500";
        }
    };

    const renderResultState = () => {
        if (!result) return null;

        const { ats_result, job_matches, best_fit } = result;

        return (
            <div className="space-y-6">
                {/* ATS Score Section */}
                <div className="space-y-2">
                    <div className="flex items-center gap-2 text-neon-pink">
                        <Target className="h-4 w-4" />
                        <span className="font-display font-bold tracking-wider uppercase text-xs">ATS COMPATIBILITY</span>
                    </div>
                    <div className="bg-black/40 rounded-lg p-4 border border-neon-pink/20">
                        <div className="flex items-baseline gap-2 mb-3">
                            <span className={cn("text-4xl font-display font-black", getScoreColor(ats_result.total_score))}>
                                {ats_result.total_score}
                            </span>
                            <span className="text-muted-foreground text-sm">/100</span>
                        </div>
                        <div className="grid grid-cols-2 gap-2 text-[10px] font-mono">
                            <div className="flex justify-between">
                                <span className="text-muted-foreground">Skills:</span>
                                <span className="text-neon-cyan">{ats_result.skill_score}/40</span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-muted-foreground">Experience:</span>
                                <span className="text-neon-cyan">{ats_result.experience_score}/30</span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-muted-foreground">Education:</span>
                                <span className="text-neon-cyan">{ats_result.education_score}/15</span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-muted-foreground">Keywords:</span>
                                <span className="text-neon-cyan">{ats_result.keyword_score}/5</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Best Fit Banner */}
                {best_fit && (
                    <div className="bg-neon-green/10 border border-neon-green/30 rounded-lg p-3">
                        <div className="flex items-center gap-2 mb-2">
                            <CheckCircle2 className="h-4 w-4 text-neon-green" />
                            <span className="text-neon-green font-display font-bold text-xs uppercase tracking-wider">Best Match Found</span>
                        </div>
                        <p className="text-white font-bold">{best_fit.job_title}</p>
                        <p className="text-[10px] font-mono text-muted-foreground mt-1">{best_fit.recommendation}</p>
                    </div>
                )}

                {/* Job Matches */}
                <div className="space-y-2">
                    <div className="flex items-center gap-2 text-neon-cyan">
                        <TrendingUp className="h-4 w-4" />
                        <span className="font-display font-bold tracking-wider uppercase text-xs">JOB MATCHES</span>
                    </div>
                    <div className="space-y-2">
                        {job_matches.map((match) => (
                            <div
                                key={match.job_id}
                                className={cn(
                                    "bg-black/40 rounded-lg p-3 border",
                                    match.is_best_fit ? "border-neon-green/30" : "border-white/10"
                                )}
                            >
                                <div className="flex items-center justify-between mb-2">
                                    <span className="text-white font-bold text-sm truncate max-w-[200px]">
                                        {match.job_title}
                                    </span>
                                    <span className={cn("font-mono font-bold", getMatchLevelColor(match.match_level))}>
                                        {match.match_percentage}%
                                    </span>
                                </div>
                                {match.company && (
                                    <p className="text-[10px] text-muted-foreground font-mono mb-2">{match.company}</p>
                                )}
                                {match.matched_skills.length > 0 && (
                                    <div className="flex flex-wrap gap-1 mb-2">
                                        {match.matched_skills.slice(0, 5).map((skill) => (
                                            <span
                                                key={skill}
                                                className="text-[9px] bg-neon-cyan/10 text-neon-cyan px-1.5 py-0.5 rounded border border-neon-cyan/20"
                                            >
                                                {skill}
                                            </span>
                                        ))}
                                        {match.matched_skills.length > 5 && (
                                            <span className="text-[9px] text-muted-foreground">
                                                +{match.matched_skills.length - 5} more
                                            </span>
                                        )}
                                    </div>
                                )}
                                {match.missing_skills.length > 0 && (
                                    <div className="flex flex-wrap gap-1">
                                        {match.missing_skills.slice(0, 3).map((skill) => (
                                            <span
                                                key={skill}
                                                className="text-[9px] bg-red-500/10 text-red-400 px-1.5 py-0.5 rounded border border-red-500/20"
                                            >
                                                -{skill}
                                            </span>
                                        ))}
                                        {match.missing_skills.length > 3 && (
                                            <span className="text-[9px] text-muted-foreground">
                                                +{match.missing_skills.length - 3} gaps
                                            </span>
                                        )}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>

                {/* Improvement Suggestions */}
                {ats_result.improvement_suggestions.length > 0 && (
                    <div className="space-y-2">
                        <span className="text-neon-yellow font-display font-bold tracking-wider uppercase text-xs">RECOMMENDATIONS</span>
                        <ul className="space-y-1 text-[11px] font-mono text-muted-foreground">
                            {ats_result.improvement_suggestions.slice(0, 5).map((suggestion, idx) => (
                                <li key={idx} className="flex items-start gap-2">
                                    <span className="text-neon-yellow">{">"}</span>
                                    <span>{suggestion}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
        );
    };

    const renderContent = () => {
        if (status === "error") return renderErrorState();
        if (status === "uploading" || status === "analyzing") return renderLoadingState();
        if (status === "done" && result) return renderResultState();
        return renderIdleState();
    };

    return (
        <div className="h-full flex flex-col font-mono text-sm bg-background/40 backdrop-blur border-l border-border/40">
            <div className="flex items-center justify-between border-b border-border/40 px-4 py-3 bg-muted/10">
                <div className="flex items-center gap-2">
                    <Activity className={cn(
                        "h-4 w-4",
                        status === "analyzing" || status === "uploading"
                            ? "text-neon-cyan animate-pulse"
                            : status === "done"
                                ? "text-neon-green"
                                : "text-neon-pink animate-pulse"
                    )} />
                    <span className="font-display font-bold tracking-wide text-foreground">LIVE OUTPUT STREAM</span>
                </div>
                <div className="flex items-center gap-2 text-[10px] text-muted-foreground uppercase">
                    <div className={cn(
                        "h-1.5 w-1.5 rounded-full",
                        status === "error" ? "bg-red-500" : "bg-neon-green/80"
                    )} />
                    <span>{status === "error" ? "Error" : "Connected"}</span>
                </div>
            </div>

            <div className="flex-1 p-4 overflow-auto scrollbar-thin scrollbar-thumb-muted-foreground/20 scrollbar-track-transparent">
                {renderContent()}

                {/* Scanline Effect Overlay */}
                <div className="absolute inset-0 pointer-events-none bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.1)_50%),linear-gradient(90deg,rgba(255,0,0,0.03),rgba(0,255,0,0.01),rgba(0,0,255,0.03))] z-50 bg-[length:100%_2px,3px_100%] opacity-20 user-select-none" />
            </div>
        </div>
    );
}
