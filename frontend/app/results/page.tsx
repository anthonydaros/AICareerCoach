"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  ArrowLeft,
  Download,
  Share2,
  RefreshCw,
  Target,
  Briefcase,
  Zap,
  MessageSquare,
  GraduationCap,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { useResults } from "@/contexts/ResultsContext";
import { ScoreHero } from "@/components/results/ScoreHero";
import { JobMatchList } from "@/components/results/JobMatchList";
import { SkillsGrid } from "@/components/results/SkillsGrid";
import { InterviewPrepSection } from "@/components/results/InterviewPrepSection";
import { CoachingSection } from "@/components/results/CoachingSection";
import { Background } from "@/components/layout/Background";

type TabType = "overview" | "jobs" | "skills" | "interview" | "coaching";

const tabs: { id: TabType; label: string; icon: typeof Target }[] = [
  { id: "overview", label: "Overview", icon: Target },
  { id: "jobs", label: "Job Matches", icon: Briefcase },
  { id: "skills", label: "Skills", icon: Zap },
  { id: "interview", label: "Interview Prep", icon: MessageSquare },
  { id: "coaching", label: "Career Coach", icon: GraduationCap },
];

export default function ResultsPage() {
  const router = useRouter();
  const { result, interviewPrep, coachingTips, hasResults, clearResults } = useResults();
  const [activeTab, setActiveTab] = useState<TabType>("overview");
  const [isLoadingInterview, setIsLoadingInterview] = useState(false);
  const [isLoadingCoaching, setIsLoadingCoaching] = useState(false);

  // Redirect if no results
  useEffect(() => {
    if (!hasResults) {
      router.push("/");
    }
  }, [hasResults, router]);

  if (!result) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="w-8 h-8 animate-spin text-neon-cyan mx-auto mb-4" />
          <p className="text-muted-foreground font-mono">Loading results...</p>
        </div>
      </div>
    );
  }

  const handleNewAnalysis = () => {
    clearResults();
    router.push("/");
  };

  // Get all skill gaps from job matches for SkillsGrid
  const allSkillGaps = result.job_matches.flatMap(m => m.skill_gaps);

  return (
    <div className="min-h-screen bg-background relative">
      <Background />

      <div className="relative z-10">
        {/* Header */}
        <header className="sticky top-0 z-50 bg-black/80 backdrop-blur-xl border-b border-white/10">
          <div className="max-w-7xl mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <button
                  onClick={handleNewAnalysis}
                  className="flex items-center gap-2 text-muted-foreground hover:text-white transition-colors"
                >
                  <ArrowLeft className="w-4 h-4" />
                  <span className="text-sm font-mono">New Analysis</span>
                </button>
                <div className="h-6 w-px bg-white/20" />
                <h1 className="text-lg font-display font-bold tracking-wider uppercase text-white">
                  Analysis Results
                </h1>
              </div>

              <div className="flex items-center gap-2">
                <button
                  className="p-2 text-muted-foreground hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                  title="Download Report"
                >
                  <Download className="w-5 h-5" />
                </button>
                <button
                  className="p-2 text-muted-foreground hover:text-white hover:bg-white/10 rounded-lg transition-colors"
                  title="Share"
                >
                  <Share2 className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* Tabs */}
            <div className="flex gap-1 mt-4 overflow-x-auto pb-2 -mb-2 scrollbar-hide">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={cn(
                    "flex items-center gap-2 px-4 py-2 rounded-lg font-display font-bold text-sm uppercase tracking-wider transition-all whitespace-nowrap",
                    activeTab === tab.id
                      ? "bg-neon-cyan/20 text-neon-cyan border border-neon-cyan/40"
                      : "text-muted-foreground hover:text-white hover:bg-white/5"
                  )}
                >
                  <tab.icon className="w-4 h-4" />
                  {tab.label}
                </button>
              ))}
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 py-8">
          {activeTab === "overview" && (
            <motion.div
              key="overview"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <ScoreHero
                atsResult={result.ats_result}
                bestFit={result.best_fit}
                jobCount={result.job_matches.length}
              />

              {/* Quick Summary Cards */}
              <div className="mt-8 grid md:grid-cols-2 gap-6">
                {/* Top Job Match */}
                {result.best_fit && (
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                    className="bg-black/40 border border-neon-green/30 rounded-lg p-6"
                  >
                    <div className="flex items-center gap-2 mb-4">
                      <Briefcase className="w-5 h-5 text-neon-green" />
                      <h3 className="text-sm font-display font-bold uppercase tracking-wider text-neon-green">
                        Top Match
                      </h3>
                    </div>
                    <p className="text-lg text-white font-medium mb-2">
                      {result.best_fit.job_title}
                    </p>
                    <p className="text-sm text-muted-foreground line-clamp-2">
                      {result.best_fit.recommendation}
                    </p>
                    <button
                      onClick={() => setActiveTab("jobs")}
                      className="mt-4 text-sm text-neon-cyan hover:underline"
                    >
                      View all matches →
                    </button>
                  </motion.div>
                )}

                {/* Key Actions */}
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 }}
                  className="bg-black/40 border border-neon-pink/30 rounded-lg p-6"
                >
                  <div className="flex items-center gap-2 mb-4">
                    <Zap className="w-5 h-5 text-neon-pink" />
                    <h3 className="text-sm font-display font-bold uppercase tracking-wider text-neon-pink">
                      Quick Actions
                    </h3>
                  </div>
                  <div className="space-y-2">
                    <button
                      onClick={() => setActiveTab("skills")}
                      className="w-full text-left p-3 bg-white/5 hover:bg-white/10 rounded-lg transition-colors"
                    >
                      <span className="text-white text-sm">
                        Review {result.ats_result.missing_keywords.length} missing keywords
                      </span>
                    </button>
                    <button
                      onClick={() => setActiveTab("interview")}
                      className="w-full text-left p-3 bg-white/5 hover:bg-white/10 rounded-lg transition-colors"
                    >
                      <span className="text-white text-sm">
                        Prepare for interview questions
                      </span>
                    </button>
                    <button
                      onClick={() => setActiveTab("coaching")}
                      className="w-full text-left p-3 bg-white/5 hover:bg-white/10 rounded-lg transition-colors"
                    >
                      <span className="text-white text-sm">
                        Get career coaching tips
                      </span>
                    </button>
                  </div>
                </motion.div>
              </div>
            </motion.div>
          )}

          {activeTab === "jobs" && (
            <motion.div
              key="jobs"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <JobMatchList matches={result.job_matches} />
            </motion.div>
          )}

          {activeTab === "skills" && (
            <motion.div
              key="skills"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <SkillsGrid atsResult={result.ats_result} skillGaps={allSkillGaps} />
            </motion.div>
          )}

          {activeTab === "interview" && (
            <motion.div
              key="interview"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <InterviewPrepSection
                interviewPrep={interviewPrep}
                isLoading={isLoadingInterview}
              />
            </motion.div>
          )}

          {activeTab === "coaching" && (
            <motion.div
              key="coaching"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              <CoachingSection
                coachingTips={coachingTips}
                isLoading={isLoadingCoaching}
              />
            </motion.div>
          )}
        </main>

        {/* Footer */}
        <footer className="border-t border-white/10 py-8 mt-12">
          <div className="max-w-7xl mx-auto px-4 text-center">
            <p className="text-xs text-muted-foreground font-mono">
              AI Career Coach | Analysis powered by CareerAI
            </p>
          </div>
        </footer>
      </div>
    </div>
  );
}
