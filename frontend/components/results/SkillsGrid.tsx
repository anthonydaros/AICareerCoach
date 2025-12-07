"use client";

import { motion } from "framer-motion";
import { CheckCircle2, XCircle, Lightbulb, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";
import type { ATSResult, SkillGap } from "@/lib/types";

interface SkillsGridProps {
  atsResult: ATSResult;
  skillGaps?: SkillGap[];
}

export function SkillsGrid({ atsResult, skillGaps = [] }: SkillsGridProps) {
  return (
    <div className="space-y-6">
      {/* Matched Keywords */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="flex items-center gap-2 mb-4">
          <CheckCircle2 className="w-5 h-5 text-neon-green" />
          <h3 className="text-lg font-display font-bold uppercase tracking-wider text-white">
            Matched Keywords
          </h3>
          <span className="text-xs font-mono text-neon-green">
            ({atsResult.matched_keywords.length})
          </span>
        </div>

        <div className="bg-black/40 border border-neon-green/20 rounded-lg p-4">
          {atsResult.matched_keywords.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {atsResult.matched_keywords.map((keyword, index) => (
                <motion.span
                  key={keyword}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: index * 0.05 }}
                  className="px-3 py-1 text-sm bg-neon-green/10 text-neon-green border border-neon-green/30 rounded-full"
                >
                  {keyword}
                </motion.span>
              ))}
            </div>
          ) : (
            <p className="text-sm text-muted-foreground">No keywords matched</p>
          )}
        </div>
      </motion.div>

      {/* Missing Keywords */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <div className="flex items-center gap-2 mb-4">
          <XCircle className="w-5 h-5 text-red-400" />
          <h3 className="text-lg font-display font-bold uppercase tracking-wider text-white">
            Missing Keywords
          </h3>
          <span className="text-xs font-mono text-red-400">
            ({atsResult.missing_keywords.length})
          </span>
        </div>

        <div className="bg-black/40 border border-red-400/20 rounded-lg p-4">
          {atsResult.missing_keywords.length > 0 ? (
            <div className="flex flex-wrap gap-2">
              {atsResult.missing_keywords.map((keyword, index) => (
                <motion.span
                  key={keyword}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: index * 0.05 }}
                  className="px-3 py-1 text-sm bg-red-400/10 text-red-400 border border-red-400/30 rounded-full"
                >
                  {keyword}
                </motion.span>
              ))}
            </div>
          ) : (
            <p className="text-sm text-neon-green">All keywords matched!</p>
          )}
        </div>
      </motion.div>

      {/* Improvement Suggestions */}
      {atsResult.improvement_suggestions.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <div className="flex items-center gap-2 mb-4">
            <Lightbulb className="w-5 h-5 text-neon-yellow" />
            <h3 className="text-lg font-display font-bold uppercase tracking-wider text-white">
              Suggestions
            </h3>
          </div>

          <div className="bg-black/40 border border-neon-yellow/20 rounded-lg p-4 space-y-3">
            {atsResult.improvement_suggestions.map((suggestion, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 + index * 0.1 }}
                className="flex items-start gap-3"
              >
                <span className="text-neon-yellow font-mono text-sm">{String(index + 1).padStart(2, '0')}</span>
                <p className="text-sm text-muted-foreground">{suggestion}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Format Issues */}
      {atsResult.format_issues.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <div className="flex items-center gap-2 mb-4">
            <AlertCircle className="w-5 h-5 text-neon-pink" />
            <h3 className="text-lg font-display font-bold uppercase tracking-wider text-white">
              Format Issues
            </h3>
          </div>

          <div className="bg-black/40 border border-neon-pink/20 rounded-lg p-4 space-y-2">
            {atsResult.format_issues.map((issue, index) => (
              <div key={index} className="flex items-start gap-3">
                <span className="text-neon-pink">!</span>
                <p className="text-sm text-muted-foreground">{issue}</p>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Skill Gaps with Learning Resources */}
      {skillGaps.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <div className="flex items-center gap-2 mb-4">
            <Lightbulb className="w-5 h-5 text-neon-cyan" />
            <h3 className="text-lg font-display font-bold uppercase tracking-wider text-white">
              Skill Development
            </h3>
          </div>

          <div className="space-y-3">
            {skillGaps.slice(0, 5).map((gap, index) => (
              <motion.div
                key={gap.skill}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 + index * 0.1 }}
                className={cn(
                  "bg-black/40 border rounded-lg p-4",
                  gap.is_required ? "border-red-400/30" : "border-neon-cyan/30"
                )}
              >
                <div className="flex items-center gap-2 mb-2">
                  <span className={cn(
                    "text-sm font-medium",
                    gap.is_required ? "text-red-400" : "text-neon-cyan"
                  )}>
                    {gap.skill}
                  </span>
                  {gap.is_required && (
                    <span className="px-2 py-0.5 text-[10px] bg-red-400/20 text-red-400 rounded uppercase">
                      Required
                    </span>
                  )}
                </div>
                <p className="text-sm text-muted-foreground mb-2">{gap.suggestion}</p>
                {gap.learning_resources.length > 0 && (
                  <div className="flex flex-wrap gap-2">
                    {gap.learning_resources.slice(0, 3).map((resource, i) => (
                      <span key={i} className="text-xs text-neon-cyan/70">
                        {resource}
                      </span>
                    ))}
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}
