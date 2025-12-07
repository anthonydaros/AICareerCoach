"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { GraduationCap, ChevronDown, ChevronUp, AlertTriangle, Loader2, Rocket, Target, BookOpen, Users } from "lucide-react";
import { cn } from "@/lib/utils";
import type { CoachingTipsResponse, CoachingTip } from "@/lib/types";

interface CoachingSectionProps {
  coachingTips: CoachingTipsResponse | null;
  isLoading?: boolean;
}

const categoryIcons: Record<string, typeof Rocket> = {
  skills: Rocket,
  experience: Target,
  education: BookOpen,
  networking: Users,
  default: GraduationCap,
};

const priorityColors: Record<string, { text: string; bg: string; border: string }> = {
  high: { text: "text-red-400", bg: "bg-red-400/10", border: "border-red-400/30" },
  medium: { text: "text-neon-yellow", bg: "bg-neon-yellow/10", border: "border-neon-yellow/30" },
  low: { text: "text-neon-green", bg: "bg-neon-green/10", border: "border-neon-green/30" },
  default: { text: "text-neon-cyan", bg: "bg-neon-cyan/10", border: "border-neon-cyan/30" },
};

function TipCard({ tip, index }: { tip: CoachingTip; index: number }) {
  const [isExpanded, setIsExpanded] = useState(index === 0);
  const Icon = categoryIcons[tip.category.toLowerCase()] || categoryIcons.default;
  const colors = priorityColors[tip.priority.toLowerCase()] || priorityColors.default;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className={cn(
        "bg-black/40 border rounded-lg overflow-hidden transition-all duration-300",
        colors.border
      )}
    >
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full p-4 flex items-start gap-4 text-left hover:bg-white/5 transition-colors"
      >
        <div className={cn(
          "w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0",
          colors.bg
        )}>
          <Icon className={cn("w-5 h-5", colors.text)} />
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <span className={cn(
              "px-2 py-0.5 text-[10px] uppercase font-display font-bold rounded",
              colors.bg, colors.text
            )}>
              {tip.priority} Priority
            </span>
            <span className="text-[10px] text-muted-foreground uppercase font-mono">
              {tip.category}
            </span>
          </div>
          <h3 className="text-white font-medium">{tip.title}</h3>
        </div>

        {isExpanded ? (
          <ChevronUp className="w-5 h-5 text-muted-foreground flex-shrink-0" />
        ) : (
          <ChevronDown className="w-5 h-5 text-muted-foreground flex-shrink-0" />
        )}
      </button>

      {isExpanded && (
        <motion.div
          initial={{ height: 0, opacity: 0 }}
          animate={{ height: "auto", opacity: 1 }}
          className="border-t border-white/10 p-4 space-y-4"
        >
          {/* Description */}
          <p className="text-sm text-muted-foreground">{tip.description}</p>

          {/* Action Items */}
          {tip.action_items.length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-2">
                <Target className="w-4 h-4 text-neon-cyan" />
                <span className="text-xs font-display font-bold uppercase tracking-wider text-neon-cyan">
                  Action Items
                </span>
              </div>
              <ul className="space-y-2 pl-6">
                {tip.action_items.map((item, i) => (
                  <li
                    key={i}
                    className="text-sm text-muted-foreground flex items-start gap-3"
                  >
                    <span className="w-5 h-5 rounded bg-neon-cyan/10 text-neon-cyan flex items-center justify-center flex-shrink-0 text-xs font-mono">
                      {i + 1}
                    </span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </motion.div>
      )}
    </motion.div>
  );
}

export function CoachingSection({ coachingTips, isLoading }: CoachingSectionProps) {
  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <Loader2 className="w-8 h-8 text-neon-yellow animate-spin mb-4" />
        <p className="text-sm text-muted-foreground font-mono">Generating coaching tips...</p>
      </div>
    );
  }

  if (!coachingTips || coachingTips.tips.length === 0) {
    return (
      <div className="text-center py-12">
        <GraduationCap className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
        <p className="text-muted-foreground">No coaching tips available</p>
      </div>
    );
  }

  // Group tips by priority for summary
  const highPriority = coachingTips.tips.filter(t => t.priority.toLowerCase() === "high");
  const mediumPriority = coachingTips.tips.filter(t => t.priority.toLowerCase() === "medium");
  const lowPriority = coachingTips.tips.filter(t => t.priority.toLowerCase() === "low");

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center gap-2">
        <GraduationCap className="w-5 h-5 text-neon-yellow" />
        <h2 className="text-lg font-display font-bold uppercase tracking-wider text-white">
          Career Coaching
        </h2>
        <span className="text-xs font-mono text-muted-foreground">
          ({coachingTips.tips.length} recommendations)
        </span>
      </div>

      {/* Priority Summary */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-red-400/10 border border-red-400/30 rounded-lg p-3 text-center">
          <AlertTriangle className="w-5 h-5 mx-auto mb-1 text-red-400" />
          <div className="text-2xl font-display font-bold text-red-400">{highPriority.length}</div>
          <div className="text-[10px] font-mono text-red-400/70 uppercase">High Priority</div>
        </div>
        <div className="bg-neon-yellow/10 border border-neon-yellow/30 rounded-lg p-3 text-center">
          <Target className="w-5 h-5 mx-auto mb-1 text-neon-yellow" />
          <div className="text-2xl font-display font-bold text-neon-yellow">{mediumPriority.length}</div>
          <div className="text-[10px] font-mono text-neon-yellow/70 uppercase">Medium Priority</div>
        </div>
        <div className="bg-neon-green/10 border border-neon-green/30 rounded-lg p-3 text-center">
          <Rocket className="w-5 h-5 mx-auto mb-1 text-neon-green" />
          <div className="text-2xl font-display font-bold text-neon-green">{lowPriority.length}</div>
          <div className="text-[10px] font-mono text-neon-green/70 uppercase">Low Priority</div>
        </div>
      </div>

      {/* Tips List - sorted by priority */}
      <div className="space-y-3">
        {[...highPriority, ...mediumPriority, ...lowPriority].map((tip, index) => (
          <TipCard key={index} tip={tip} index={index} />
        ))}
      </div>
    </div>
  );
}
