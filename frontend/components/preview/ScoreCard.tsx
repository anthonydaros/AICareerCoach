"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { CheckCircle2, Unlock, Target, TrendingUp } from "lucide-react";
import { cn } from "@/lib/utils";
import { useResults } from "@/contexts/ResultsContext";
import type { AnalyzeResponse } from "@/lib/types";

interface ScoreCardProps {
  result: AnalyzeResponse;
  resumeText?: string;
  jobs?: { id: string; text: string }[];
}

// Hook for count-up animation
function useCountUp(target: number, duration: number = 1500) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let startTime: number;
    let animationFrame: number;

    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);

      // Easing function (ease-out)
      const easeOut = 1 - Math.pow(1 - progress, 3);
      setCount(Math.round(easeOut * target));

      if (progress < 1) {
        animationFrame = requestAnimationFrame(animate);
      }
    };

    animationFrame = requestAnimationFrame(animate);

    return () => cancelAnimationFrame(animationFrame);
  }, [target, duration]);

  return count;
}

export function ScoreCard({ result, resumeText, jobs = [] }: ScoreCardProps) {
  const router = useRouter();
  const { setResults } = useResults();
  const score = useCountUp(result.ats_result.total_score, 1500);
  const [showGlow, setShowGlow] = useState(false);

  const handleViewDetails = () => {
    // Store results in context
    setResults(result, resumeText || "", jobs);
    // Navigate to results page
    router.push("/results");
  };

  // Trigger glow effect after count-up completes
  useEffect(() => {
    const timeout = setTimeout(() => setShowGlow(true), 1600);
    return () => clearTimeout(timeout);
  }, []);

  const getScoreColor = (score: number) => {
    if (score >= 80) return { text: "text-neon-green", bg: "bg-neon-green", glow: "rgba(0,255,136,0.4)" };
    if (score >= 60) return { text: "text-neon-cyan", bg: "bg-neon-cyan", glow: "rgba(0,243,255,0.4)" };
    if (score >= 40) return { text: "text-neon-yellow", bg: "bg-neon-yellow", glow: "rgba(204,255,0,0.4)" };
    return { text: "text-red-500", bg: "bg-red-500", glow: "rgba(255,0,0,0.4)" };
  };

  const scoreColors = getScoreColor(result.ats_result.total_score);
  const bestFit = result.best_fit;

  return (
    <div className="flex flex-col items-center justify-center h-full px-4 py-6">
      {/* Analysis Complete Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="flex items-center gap-2 mb-6"
      >
        <CheckCircle2 className="w-5 h-5 text-neon-green" />
        <span className="text-neon-green font-display font-bold tracking-widest uppercase text-sm">
          Analysis Complete
        </span>
      </motion.div>

      {/* Main Score Display */}
      <motion.div
        initial={{ scale: 0.5, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="relative mb-4"
      >
        {/* Glow effect behind score */}
        {showGlow && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: [0.3, 0.6, 0.3] }}
            transition={{ duration: 2, repeat: Infinity }}
            className={cn("absolute inset-0 rounded-full blur-2xl", scoreColors.bg)}
            style={{ transform: "scale(1.5)" }}
          />
        )}

        {/* Score circle */}
        <div
          className={cn(
            "relative w-32 h-32 rounded-full border-4 flex items-center justify-center",
            "bg-black/60 backdrop-blur-sm",
            showGlow && "shadow-[0_0_40px_var(--glow-color)]"
          )}
          style={{
            borderColor: `${scoreColors.glow}`,
            "--glow-color": scoreColors.glow
          } as React.CSSProperties}
        >
          <div className="text-center">
            <span className={cn("text-5xl font-display font-black", scoreColors.text)}>
              {score}
            </span>
            <div className="text-[10px] text-muted-foreground font-mono mt-1">/ 100</div>
          </div>
        </div>
      </motion.div>

      {/* Score Label */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
        className="text-center mb-6"
      >
        <div className="flex items-center justify-center gap-2 mb-1">
          <Target className="w-4 h-4 text-neon-pink" />
          <span className="text-xs font-display font-bold tracking-wider uppercase text-muted-foreground">
            ATS Compatibility Score
          </span>
        </div>
        <p className="text-[10px] text-muted-foreground/60 font-mono">
          Based on {result.job_matches.length} job{result.job_matches.length !== 1 ? "s" : ""} analyzed
        </p>
      </motion.div>

      {/* Best Fit Mini Info */}
      {bestFit && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1 }}
          className="w-full max-w-xs mb-6"
        >
          <div className="bg-neon-green/5 border border-neon-green/20 rounded-lg p-3">
            <div className="flex items-center gap-2 mb-1">
              <TrendingUp className="w-3 h-3 text-neon-green" />
              <span className="text-[10px] font-display font-bold uppercase tracking-wider text-neon-green">
                Best Match
              </span>
              <span className="ml-auto text-xs font-mono font-bold text-neon-green">
                {bestFit.match_percentage}%
              </span>
            </div>
            <p className="text-sm text-white font-medium truncate">{bestFit.job_title}</p>
          </div>
        </motion.div>
      )}

      {/* View Details Button */}
      <motion.button
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.2 }}
        onClick={handleViewDetails}
        className={cn(
          "group relative px-8 py-3 rounded-lg font-display font-bold tracking-wider uppercase",
          "bg-gradient-to-r from-neon-cyan/20 to-neon-pink/20",
          "border border-neon-cyan/40 hover:border-neon-cyan",
          "text-neon-cyan hover:text-white",
          "transition-all duration-300",
          "hover:shadow-[0_0_30px_rgba(0,243,255,0.3)]"
        )}
      >
        {/* Button glow effect */}
        <div className="absolute inset-0 rounded-lg bg-gradient-to-r from-neon-cyan/0 to-neon-pink/0 group-hover:from-neon-cyan/10 group-hover:to-neon-pink/10 transition-all duration-300" />

        <span className="relative flex items-center gap-2">
          <Unlock className="w-4 h-4" />
          Decrypt Report
        </span>
      </motion.button>

      {/* Quick Stats (optional mini preview) */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5 }}
        className="flex gap-4 mt-6 text-[10px] font-mono text-muted-foreground/60"
      >
        <div className="flex items-center gap-1">
          <span className="text-neon-cyan">+</span>
          <span>{result.ats_result.matched_keywords.length} keywords</span>
        </div>
        <div className="flex items-center gap-1">
          <span className="text-red-400">-</span>
          <span>{result.ats_result.missing_keywords.length} gaps</span>
        </div>
      </motion.div>
    </div>
  );
}
