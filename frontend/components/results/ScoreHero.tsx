"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Target, Zap, Award, TrendingUp } from "lucide-react";
import { cn } from "@/lib/utils";
import type { ATSResult, BestFit } from "@/lib/types";

interface ScoreHeroProps {
  atsResult: ATSResult;
  bestFit: BestFit | null;
  jobCount: number;
}

function useCountUp(target: number, duration: number = 2000) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let startTime: number;
    let animationFrame: number;

    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
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

export function ScoreHero({ atsResult, bestFit, jobCount }: ScoreHeroProps) {
  const score = useCountUp(atsResult.total_score, 2000);
  const [showGlow, setShowGlow] = useState(false);

  useEffect(() => {
    const timeout = setTimeout(() => setShowGlow(true), 2100);
    return () => clearTimeout(timeout);
  }, []);

  const getScoreColor = (score: number) => {
    if (score >= 80) return { text: "text-neon-green", bg: "bg-neon-green", glow: "rgba(0,255,136,0.5)" };
    if (score >= 60) return { text: "text-neon-cyan", bg: "bg-neon-cyan", glow: "rgba(0,243,255,0.5)" };
    if (score >= 40) return { text: "text-neon-yellow", bg: "bg-neon-yellow", glow: "rgba(204,255,0,0.5)" };
    return { text: "text-red-500", bg: "bg-red-500", glow: "rgba(255,0,0,0.5)" };
  };

  const scoreColors = getScoreColor(atsResult.total_score);

  const stats = [
    { label: "Jobs Analyzed", value: jobCount, icon: Target },
    { label: "Keywords Matched", value: atsResult.matched_keywords.length, icon: Zap },
    { label: "Skill Gaps", value: atsResult.missing_keywords.length, icon: Award },
  ];

  return (
    <div className="relative overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-neon-cyan/5 via-transparent to-neon-pink/5" />

      <div className="relative px-6 py-10 lg:py-16">
        <div className="max-w-6xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-8 items-center">
            {/* Score Display */}
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6 }}
              className="flex flex-col items-center"
            >
              {/* Main Score Circle */}
              <div className="relative">
                {showGlow && (
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: [0.4, 0.7, 0.4] }}
                    transition={{ duration: 3, repeat: Infinity }}
                    className={cn("absolute inset-0 rounded-full blur-3xl", scoreColors.bg)}
                    style={{ transform: "scale(1.8)" }}
                  />
                )}

                <div
                  className={cn(
                    "relative w-48 h-48 lg:w-56 lg:h-56 rounded-full border-4 flex items-center justify-center",
                    "bg-black/80 backdrop-blur-xl",
                    showGlow && "shadow-[0_0_60px_var(--glow-color)]"
                  )}
                  style={{
                    borderColor: scoreColors.glow,
                    "--glow-color": scoreColors.glow
                  } as React.CSSProperties}
                >
                  <div className="text-center">
                    <span className={cn("text-7xl lg:text-8xl font-display font-black", scoreColors.text)}>
                      {score}
                    </span>
                    <div className="text-sm text-muted-foreground font-mono mt-2">/ 100</div>
                  </div>
                </div>
              </div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                className="mt-6 text-center"
              >
                <h2 className="text-xl font-display font-bold tracking-wider uppercase text-white mb-1">
                  ATS Compatibility Score
                </h2>
                <p className="text-sm text-muted-foreground font-mono">
                  Based on comprehensive analysis
                </p>
              </motion.div>
            </motion.div>

            {/* Stats Grid */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3, duration: 0.5 }}
              className="space-y-6"
            >
              {/* Quick Stats */}
              <div className="grid grid-cols-3 gap-4">
                {stats.map((stat, index) => (
                  <motion.div
                    key={stat.label}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.4 + index * 0.1 }}
                    className="bg-black/40 border border-white/10 rounded-lg p-4 text-center"
                  >
                    <stat.icon className="w-5 h-5 mx-auto mb-2 text-neon-cyan" />
                    <div className="text-2xl font-display font-bold text-white">{stat.value}</div>
                    <div className="text-[10px] font-mono text-muted-foreground uppercase tracking-wider">
                      {stat.label}
                    </div>
                  </motion.div>
                ))}
              </div>

              {/* Best Fit Card */}
              {bestFit && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.7 }}
                  className="bg-neon-green/10 border border-neon-green/30 rounded-lg p-4"
                >
                  <div className="flex items-center gap-2 mb-2">
                    <TrendingUp className="w-4 h-4 text-neon-green" />
                    <span className="text-xs font-display font-bold uppercase tracking-wider text-neon-green">
                      Best Match
                    </span>
                    <span className="ml-auto text-lg font-mono font-bold text-neon-green">
                      {bestFit.match_percentage}%
                    </span>
                  </div>
                  <p className="text-lg text-white font-medium">{bestFit.job_title}</p>
                  <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
                    {bestFit.recommendation}
                  </p>
                </motion.div>
              )}

              {/* Score Breakdown Mini */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.8 }}
                className="space-y-3"
              >
                {[
                  { label: "Skills", score: atsResult.skill_score, max: 40 },
                  { label: "Experience", score: atsResult.experience_score, max: 30 },
                  { label: "Education", score: atsResult.education_score, max: 15 },
                  { label: "Certifications", score: atsResult.certification_score, max: 10 },
                  { label: "Keywords", score: atsResult.keyword_score, max: 5 },
                ].map((item) => (
                  <div key={item.label} className="flex items-center gap-3">
                    <span className="text-xs font-mono text-muted-foreground w-24">{item.label}</span>
                    <div className="flex-1 h-2 bg-white/10 rounded-full overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${(item.score / item.max) * 100}%` }}
                        transition={{ duration: 1, delay: 1 }}
                        className="h-full bg-gradient-to-r from-neon-cyan to-neon-pink"
                      />
                    </div>
                    <span className="text-xs font-mono text-white w-16 text-right">
                      {item.score.toFixed(1)}/{item.max}
                    </span>
                  </div>
                ))}
              </motion.div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}
