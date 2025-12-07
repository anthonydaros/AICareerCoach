"use client";

import { useRef, useCallback, useState } from "react";
import { Header } from "@/components/layout/Header";
import { ResumeUploader } from "@/components/upload/ResumeUploader";
import { JobPostInput, JobPostInputRef } from "@/components/input/JobPostInput";
import { LivePreview } from "@/components/preview/LivePreview";
import { Button } from "@/components/ui/button";
import { Plus, Loader2 } from "lucide-react";
import { useAnalysis } from "@/hooks/useAnalysis";
import { DEMO_RESUME, DEMO_JOBS } from "@/lib/demo-data";
import type { Job } from "@/lib/types";

export default function Dashboard() {
  const jobInputRef = useRef<JobPostInputRef>(null);
  const [currentJobs, setCurrentJobs] = useState<Job[]>([]);
  const {
    status,
    result,
    error,
    resumeFilename,
    resumeText,
    hasResume,
    isLoading,
    handleFileUpload,
    loadDemoData,
    runAnalysis,
    reset,
  } = useAnalysis();

  const handleAddJob = () => {
    jobInputRef.current?.addJob();
  };

  const handleUpload = async (file: File) => {
    await handleFileUpload(file);
  };

  const handleClearResume = () => {
    reset();
  };

  const handleInitiate = async () => {
    const jobs = jobInputRef.current?.getJobs() || [];
    setCurrentJobs(jobs);
    await runAnalysis(jobs);
  };

  const handleLoadDemo = useCallback(async () => {
    // Load demo resume into state (for display purposes)
    loadDemoData(DEMO_RESUME, "john_doe_resume.txt");

    // Load demo jobs into the job input component
    jobInputRef.current?.setJobs(DEMO_JOBS);

    // Store jobs for passing to LivePreview
    setCurrentJobs(DEMO_JOBS);

    // Run analysis with demo data passed directly (avoids state timing issues)
    await runAnalysis(DEMO_JOBS, DEMO_RESUME);
  }, [loadDemoData, runAnalysis]);

  const canInitiate = hasResume && !isLoading;

  return (
    <div className="h-screen bg-deep-bg flex flex-col font-sans selection:bg-neon-pink/30 relative overflow-hidden">

      {/* HUD Borders / Overlay - Decorative */}
      <div className="fixed inset-0 pointer-events-none z-50" aria-hidden="true">
        <div className="absolute top-0 left-0 w-8 h-8 border-l-2 border-t-2 border-neon-cyan/50 rounded-tl-lg" />
        <div className="absolute top-0 right-0 w-8 h-8 border-r-2 border-t-2 border-neon-cyan/50 rounded-tr-lg" />
        <div className="absolute bottom-0 left-0 w-8 h-8 border-l-2 border-b-2 border-neon-cyan/50 rounded-bl-lg" />
        <div className="absolute bottom-0 right-0 w-8 h-8 border-r-2 border-b-2 border-neon-cyan/50 rounded-br-lg" />
        <div className="absolute bottom-4 left-1/2 -translate-x-1/2 text-[10px] text-neon-cyan/40 font-mono tracking-[0.2em] uppercase">
          System_Online :: Secure_Connection_Established
        </div>
      </div>

      <Header onLoadDemo={handleLoadDemo} />

      <main id="main-content" className="flex-1 flex flex-col lg:flex-row relative z-10 p-2 sm:p-3 lg:p-4 gap-3 lg:gap-4 max-w-[1600px] mx-auto w-full min-h-0" tabIndex={-1}>

        {/* LEFT PANEL: MISSIONS */}
        <section className="flex-1 flex flex-col gap-3 lg:gap-4 min-h-0" aria-label="Input section">

          {/* STEP 1: MISSION INTEL */}
          <div className="relative group flex-1 min-h-0 flex flex-col">
            <div className="absolute -inset-0.5 bg-gradient-to-r from-neon-cyan/20 to-transparent opacity-0 group-hover:opacity-100 transition duration-500 rounded-lg blur" />
            <div className="relative bg-background/40 border border-neon-cyan/30 p-1 rounded-lg backdrop-blur-md flex-1 flex flex-col min-h-0">
              <div className="bg-background/60 p-3 lg:p-4 rounded border border-white/5 flex-1 flex flex-col min-h-0">
                <div className="flex items-center justify-between border-b border-white/10 pb-2 shrink-0">
                  <h2 className="text-xl lg:text-2xl font-display font-bold text-neon-cyan tracking-wider flex items-center gap-2">
                    <span className="flex items-center justify-center w-6 h-6 lg:w-8 lg:h-8 bg-neon-cyan/10 border border-neon-cyan/50 rounded text-xs lg:text-sm">01</span>
                    MISSION INTEL
                  </h2>
                  <div className="flex items-center gap-2">
                    <span className="hidden sm:inline text-[10px] font-mono text-neon-cyan/60 uppercase tracking-widest">[Job_Description]</span>
                    <Button
                      size="sm"
                      onClick={handleAddJob}
                      className="bg-neon-cyan/10 text-neon-cyan border border-neon-cyan/50 hover:bg-neon-cyan hover:text-black uppercase font-mono tracking-wider transition-all shadow-[0_0_10px_rgba(0,243,255,0.2)] text-xs"
                    >
                      <Plus className="h-3 w-3 mr-1" />
                      NEW INTEL
                    </Button>
                  </div>
                </div>
                <div className="flex-1 min-h-0 mt-2">
                  <JobPostInput ref={jobInputRef} />
                </div>
              </div>
            </div>
          </div>

          {/* STEP 2: LOADOUT */}
          <div className="relative group shrink-0">
            <div className="absolute -inset-0.5 bg-gradient-to-r from-neon-pink/20 to-transparent opacity-0 group-hover:opacity-100 transition duration-500 rounded-lg blur" />
            <div className="relative bg-background/40 border border-neon-pink/30 p-1 rounded-lg backdrop-blur-md">
              <div className="bg-background/60 p-3 lg:p-4 rounded border border-white/5 space-y-2">
                <div className="flex items-center justify-between border-b border-white/10 pb-2">
                  <h2 className="text-xl lg:text-2xl font-display font-bold text-neon-pink tracking-wider flex items-center gap-2">
                    <span className="flex items-center justify-center w-6 h-6 lg:w-8 lg:h-8 bg-neon-pink/10 border border-neon-pink/50 rounded text-xs lg:text-sm">02</span>
                    LOADOUT
                  </h2>
                  <span className="text-[10px] font-mono text-neon-pink/60 uppercase tracking-widest">[Resume_Upload]</span>
                </div>
                <ResumeUploader
                  onUpload={handleUpload}
                  onClear={handleClearResume}
                  isUploading={status === "uploading"}
                  uploadedFilename={resumeFilename}
                  error={status === "error" ? error : null}
                />
              </div>
            </div>
          </div>

        </section>

        {/* RIGHT PANEL: EXECUTION & STATUS */}
        <section className="lg:w-[400px] flex flex-col gap-3 min-h-0" aria-label="Analysis and results">

          {/* EXECUTE BUTTON */}
          <div className="relative group cursor-pointer active:scale-95 transition-transform duration-100 shrink-0">
            <div className={`absolute inset-0 ${canInitiate ? 'bg-neon-cyan' : 'bg-gray-500'} blur-[20px] opacity-20 group-hover:opacity-40 ${!isLoading && 'animate-pulse'} transition-opacity`} aria-hidden="true" />
            <button
              onClick={handleInitiate}
              disabled={!canInitiate}
              aria-label={isLoading ? (status === "uploading" ? "Uploading resume" : "Analyzing data") : "Start analysis"}
              aria-busy={isLoading}
              className={`relative w-full overflow-hidden bg-background border-2 ${canInitiate
                  ? 'border-neon-cyan text-neon-cyan hover:bg-neon-cyan hover:text-black'
                  : 'border-gray-600 text-gray-500 cursor-not-allowed'
                } transition-all duration-300 p-4 lg:p-6 clip-path-polygon group focus:outline-none focus:ring-2 focus:ring-neon-cyan focus:ring-offset-2 focus:ring-offset-background`}
            >
              {/* Tech markings */}
              <div className="absolute top-0 right-0 p-1 text-[8px] font-mono opacity-50" aria-hidden="true">EXE_001</div>
              <div className="absolute bottom-0 left-0 p-1 text-[8px] font-mono opacity-50" aria-hidden="true">
                {hasResume ? 'READY' : 'AWAITING_DATA'}
              </div>

              <div className="flex flex-col items-center gap-1 relative z-10">
                {isLoading ? (
                  <>
                    <Loader2 className="h-6 w-6 animate-spin" aria-hidden="true" />
                    <span className="text-lg font-display font-black tracking-[0.2em] uppercase">
                      PROCESSING
                    </span>
                    <span className="text-xs font-mono tracking-widest opacity-80" aria-hidden="true">
                      {status === "uploading" ? "UPLOADING_RESUME" : "ANALYZING_DATA"}
                    </span>
                  </>
                ) : (
                  <>
                    <span className="text-2xl font-display font-black tracking-[0.2em] uppercase group-hover:drop-shadow-[0_0_10px_rgba(0,0,0,0.5)]">
                      INITIATE
                    </span>
                    <span className="text-xs font-mono tracking-widest opacity-80 group-hover:opacity-100" aria-hidden="true">RUN_ANALYSIS_PROTOCOL</span>
                  </>
                )}
              </div>
            </button>
          </div>

          {/* BATTLE LOG / PREVIEW */}
          <div className="flex-1 min-h-0 border border-white/10 rounded-lg bg-black/40 backdrop-blur overflow-hidden relative flex flex-col">
            <div className="bg-white/5 p-1.5 px-3 border-b border-white/10 flex items-center justify-between shrink-0">
              <span className="font-mono text-[10px] text-muted-foreground uppercase">System_Log</span>
              <div className="flex gap-1.5">
                <div className={`w-2 h-2 rounded-full ${status === 'error' ? 'bg-red-500' : 'bg-red-500/50'}`} />
                <div className={`w-2 h-2 rounded-full ${isLoading ? 'bg-yellow-500' : 'bg-yellow-500/50'}`} />
                <div className={`w-2 h-2 rounded-full ${status === 'done' ? 'bg-green-500' : 'bg-green-500/50'}`} />
              </div>
            </div>
            <div className="flex-1 relative">
              <LivePreview
                status={status}
                result={result}
                error={error}
                resumeText={resumeText || undefined}
                jobs={currentJobs}
              />
            </div>
          </div>

        </section>

      </main>

    </div>
  );
}
