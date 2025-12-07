"use client";

import { motion } from "framer-motion";
import { Briefcase, CheckCircle2, XCircle, ChevronDown, ChevronUp, Star, AlertTriangle } from "lucide-react";
import { cn } from "@/lib/utils";
import type { JobMatch } from "@/lib/types";
import { useState } from "react";

interface JobMatchListProps {
  matches: JobMatch[];
}

function MatchCard({ match, index }: { match: JobMatch; index: number }) {
  const [isExpanded, setIsExpanded] = useState(false);

  const getMatchColor = (level: string) => {
    switch (level) {
      case "excellent":
        return { text: "text-neon-green", bg: "bg-neon-green/20", border: "border-neon-green/40" };
      case "good":
        return { text: "text-neon-cyan", bg: "bg-neon-cyan/20", border: "border-neon-cyan/40" };
      case "fair":
        return { text: "text-neon-yellow", bg: "bg-neon-yellow/20", border: "border-neon-yellow/40" };
      default:
        return { text: "text-red-400", bg: "bg-red-400/20", border: "border-red-400/40" };
    }
  };

  const colors = getMatchColor(match.match_level);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className={cn(
        "bg-black/40 border rounded-lg overflow-hidden transition-all duration-300",
        colors.border,
        isExpanded && "shadow-lg"
      )}
    >
      {/* Header */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full p-4 flex items-center gap-4 text-left hover:bg-white/5 transition-colors"
      >
        {/* Rank Badge */}
        <div className={cn(
          "w-10 h-10 rounded-lg flex items-center justify-center font-display font-bold text-lg",
          colors.bg, colors.text
        )}>
          {match.is_best_fit ? <Star className="w-5 h-5" /> : `#${index + 1}`}
        </div>

        {/* Job Info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <h3 className="text-white font-medium truncate">{match.job_title}</h3>
            {match.is_best_fit && (
              <span className="px-2 py-0.5 text-[10px] font-display font-bold uppercase bg-neon-green/20 text-neon-green rounded">
                Best Fit
              </span>
            )}
          </div>
          {match.company && (
            <p className="text-sm text-muted-foreground truncate">{match.company}</p>
          )}
        </div>

        {/* Match Percentage */}
        <div className="text-right">
          <span className={cn("text-2xl font-display font-bold", colors.text)}>
            {match.match_percentage}%
          </span>
          <p className={cn("text-xs uppercase font-mono", colors.text)}>{match.match_level}</p>
        </div>

        {/* Expand Icon */}
        {isExpanded ? (
          <ChevronUp className="w-5 h-5 text-muted-foreground" />
        ) : (
          <ChevronDown className="w-5 h-5 text-muted-foreground" />
        )}
      </button>

      {/* Expanded Content */}
      {isExpanded && (
        <motion.div
          initial={{ height: 0, opacity: 0 }}
          animate={{ height: "auto", opacity: 1 }}
          exit={{ height: 0, opacity: 0 }}
          className="border-t border-white/10 p-4 space-y-4"
        >
          {/* Skills Row */}
          <div className="grid md:grid-cols-2 gap-4">
            {/* Matched Skills */}
            <div>
              <div className="flex items-center gap-2 mb-2">
                <CheckCircle2 className="w-4 h-4 text-neon-green" />
                <span className="text-xs font-display font-bold uppercase tracking-wider text-neon-green">
                  Matched Skills ({match.matched_skills.length})
                </span>
              </div>
              <div className="flex flex-wrap gap-1">
                {match.matched_skills.slice(0, 8).map((skill) => (
                  <span
                    key={skill}
                    className="px-2 py-0.5 text-xs bg-neon-green/10 text-neon-green border border-neon-green/30 rounded"
                  >
                    {skill}
                  </span>
                ))}
                {match.matched_skills.length > 8 && (
                  <span className="px-2 py-0.5 text-xs text-muted-foreground">
                    +{match.matched_skills.length - 8} more
                  </span>
                )}
              </div>
            </div>

            {/* Missing Skills */}
            <div>
              <div className="flex items-center gap-2 mb-2">
                <XCircle className="w-4 h-4 text-red-400" />
                <span className="text-xs font-display font-bold uppercase tracking-wider text-red-400">
                  Missing Skills ({match.missing_skills.length})
                </span>
              </div>
              <div className="flex flex-wrap gap-1">
                {match.missing_skills.slice(0, 8).map((skill) => (
                  <span
                    key={skill}
                    className="px-2 py-0.5 text-xs bg-red-400/10 text-red-400 border border-red-400/30 rounded"
                  >
                    {skill}
                  </span>
                ))}
                {match.missing_skills.length > 8 && (
                  <span className="px-2 py-0.5 text-xs text-muted-foreground">
                    +{match.missing_skills.length - 8} more
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* Strengths & Concerns */}
          <div className="grid md:grid-cols-2 gap-4">
            {match.strengths.length > 0 && (
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <CheckCircle2 className="w-4 h-4 text-neon-cyan" />
                  <span className="text-xs font-display font-bold uppercase tracking-wider text-neon-cyan">
                    Strengths
                  </span>
                </div>
                <ul className="space-y-1">
                  {match.strengths.slice(0, 3).map((strength, i) => (
                    <li key={i} className="text-sm text-muted-foreground flex items-start gap-2">
                      <span className="text-neon-cyan">+</span>
                      {strength}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {match.concerns.length > 0 && (
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <AlertTriangle className="w-4 h-4 text-neon-yellow" />
                  <span className="text-xs font-display font-bold uppercase tracking-wider text-neon-yellow">
                    Concerns
                  </span>
                </div>
                <ul className="space-y-1">
                  {match.concerns.slice(0, 3).map((concern, i) => (
                    <li key={i} className="text-sm text-muted-foreground flex items-start gap-2">
                      <span className="text-neon-yellow">!</span>
                      {concern}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </motion.div>
      )}
    </motion.div>
  );
}

export function JobMatchList({ matches }: JobMatchListProps) {
  const sortedMatches = [...matches].sort((a, b) => b.match_percentage - a.match_percentage);

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 mb-4">
        <Briefcase className="w-5 h-5 text-neon-cyan" />
        <h2 className="text-lg font-display font-bold uppercase tracking-wider text-white">
          Job Matches
        </h2>
        <span className="text-xs font-mono text-muted-foreground">
          ({matches.length} jobs analyzed)
        </span>
      </div>

      <div className="space-y-3">
        {sortedMatches.map((match, index) => (
          <MatchCard key={match.job_id} match={match} index={index} />
        ))}
      </div>
    </div>
  );
}
