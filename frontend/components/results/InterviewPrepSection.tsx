"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MessageSquare, ChevronDown, ChevronUp, CheckCircle2, XCircle, Lightbulb, HelpCircle, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";
import type { InterviewPrepResponse, InterviewQuestion } from "@/lib/types";

interface InterviewPrepSectionProps {
  interviewPrep: InterviewPrepResponse | null;
  isLoading?: boolean;
}

const categoryColors: Record<string, { text: string; bg: string; border: string }> = {
  technical: { text: "text-neon-cyan", bg: "bg-neon-cyan/10", border: "border-neon-cyan/30" },
  behavioral: { text: "text-neon-pink", bg: "bg-neon-pink/10", border: "border-neon-pink/30" },
  situational: { text: "text-neon-yellow", bg: "bg-neon-yellow/10", border: "border-neon-yellow/30" },
  experience: { text: "text-neon-green", bg: "bg-neon-green/10", border: "border-neon-green/30" },
  default: { text: "text-white", bg: "bg-white/10", border: "border-white/30" },
};

function QuestionCard({ question, index }: { question: InterviewQuestion; index: number }) {
  const [isExpanded, setIsExpanded] = useState(false);
  const colors = categoryColors[question.category.toLowerCase()] || categoryColors.default;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
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
          "w-8 h-8 rounded flex items-center justify-center flex-shrink-0",
          colors.bg
        )}>
          <span className={cn("text-sm font-mono font-bold", colors.text)}>
            {String(index + 1).padStart(2, '0')}
          </span>
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <span className={cn(
              "px-2 py-0.5 text-[10px] uppercase font-display font-bold rounded",
              colors.bg, colors.text
            )}>
              {question.category}
            </span>
          </div>
          <p className="text-white font-medium">{question.question}</p>
        </div>

        {isExpanded ? (
          <ChevronUp className="w-5 h-5 text-muted-foreground flex-shrink-0" />
        ) : (
          <ChevronDown className="w-5 h-5 text-muted-foreground flex-shrink-0" />
        )}
      </button>

      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="border-t border-white/10"
          >
            <div className="p-4 space-y-4">
              {/* Why Asked */}
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <HelpCircle className="w-4 h-4 text-neon-cyan" />
                  <span className="text-xs font-display font-bold uppercase tracking-wider text-neon-cyan">
                    Why This Question?
                  </span>
                </div>
                <p className="text-sm text-muted-foreground pl-6">{question.why_asked}</p>
              </div>

              {/* What to Say */}
              {question.what_to_say.length > 0 && (
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <CheckCircle2 className="w-4 h-4 text-neon-green" />
                    <span className="text-xs font-display font-bold uppercase tracking-wider text-neon-green">
                      What to Highlight
                    </span>
                  </div>
                  <ul className="space-y-1 pl-6">
                    {question.what_to_say.map((point, i) => (
                      <li key={i} className="text-sm text-muted-foreground flex items-start gap-2">
                        <span className="text-neon-green">+</span>
                        {point}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* What to Avoid */}
              {question.what_to_avoid.length > 0 && (
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <XCircle className="w-4 h-4 text-red-400" />
                    <span className="text-xs font-display font-bold uppercase tracking-wider text-red-400">
                      What to Avoid
                    </span>
                  </div>
                  <ul className="space-y-1 pl-6">
                    {question.what_to_avoid.map((point, i) => (
                      <li key={i} className="text-sm text-muted-foreground flex items-start gap-2">
                        <span className="text-red-400">-</span>
                        {point}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* STAR Tip for Behavioral */}
              {question.category.toLowerCase() === "behavioral" && (
                <div className="bg-neon-pink/10 border border-neon-pink/30 rounded-lg p-3">
                  <div className="flex items-center gap-2 mb-2">
                    <Lightbulb className="w-4 h-4 text-neon-pink" />
                    <span className="text-xs font-display font-bold uppercase tracking-wider text-neon-pink">
                      STAR Method Tip
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground">
                    Structure your answer using <strong className="text-neon-pink">S</strong>ituation,{" "}
                    <strong className="text-neon-pink">T</strong>ask,{" "}
                    <strong className="text-neon-pink">A</strong>ction,{" "}
                    <strong className="text-neon-pink">R</strong>esult
                  </p>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

export function InterviewPrepSection({ interviewPrep, isLoading }: InterviewPrepSectionProps) {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <Loader2 className="w-8 h-8 text-neon-cyan animate-spin mb-4" />
        <p className="text-sm text-muted-foreground font-mono">Generating interview questions...</p>
      </div>
    );
  }

  if (!interviewPrep || interviewPrep.questions.length === 0) {
    return (
      <div className="text-center py-12">
        <MessageSquare className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
        <p className="text-muted-foreground">No interview questions available</p>
      </div>
    );
  }

  // Group questions by category
  const categories = Array.from(new Set(interviewPrep.questions.map(q => q.category)));
  const filteredQuestions = selectedCategory
    ? interviewPrep.questions.filter(q => q.category === selectedCategory)
    : interviewPrep.questions;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div className="flex items-center gap-2">
          <MessageSquare className="w-5 h-5 text-neon-pink" />
          <h2 className="text-lg font-display font-bold uppercase tracking-wider text-white">
            Interview Prep
          </h2>
          <span className="text-xs font-mono text-muted-foreground">
            ({interviewPrep.questions.length} questions)
          </span>
        </div>

        {interviewPrep.job_title && (
          <span className="text-sm text-muted-foreground font-mono">
            For: {interviewPrep.job_title}
          </span>
        )}
      </div>

      {/* Category Filter */}
      <div className="flex flex-wrap gap-2">
        <button
          onClick={() => setSelectedCategory(null)}
          className={cn(
            "px-3 py-1 text-xs font-display font-bold uppercase rounded-full transition-all",
            !selectedCategory
              ? "bg-white text-black"
              : "bg-white/10 text-white hover:bg-white/20"
          )}
        >
          All
        </button>
        {categories.map((category) => {
          const colors = categoryColors[category.toLowerCase()] || categoryColors.default;
          return (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={cn(
                "px-3 py-1 text-xs font-display font-bold uppercase rounded-full transition-all",
                selectedCategory === category
                  ? cn(colors.bg, colors.text, colors.border, "border")
                  : "bg-white/10 text-white hover:bg-white/20"
              )}
            >
              {category}
            </button>
          );
        })}
      </div>

      {/* Questions List */}
      <div className="space-y-3">
        {filteredQuestions.map((question, index) => (
          <QuestionCard key={index} question={question} index={index} />
        ))}
      </div>
    </div>
  );
}
