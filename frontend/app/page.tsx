"use client";

import { useRef } from "react";
import { Header } from "@/components/layout/Header";
import { ResumeUploader } from "@/components/upload/ResumeUploader";
import { JobPostInput, JobPostInputRef } from "@/components/input/JobPostInput";
import { LivePreview } from "@/components/preview/LivePreview";
import { Button } from "@/components/ui/button";
import { Plus, Loader2 } from "lucide-react";
import { useAnalysis } from "@/hooks/useAnalysis";

export default function Dashboard() {
  const jobInputRef = useRef<JobPostInputRef>(null);
  const {
    status,
    result,
    error,
    resumeFilename,
    hasResume,
    isLoading,
    handleFileUpload,
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
    await runAnalysis(jobs);
  };

  const canInitiate = hasResume && !isLoading;

  return (
    <div className="min-h-screen bg-deep-bg flex flex-col font-sans selection:bg-neon-pink/30 relative overflow-x-hidden">

      {/* HUD Borders / Overlay */}
      <div className="fixed inset-0 pointer-events-none z-50">
        <div className="absolute top-0 left-0 w-8 h-8 border-l-2 border-t-2 border-neon-cyan/50 rounded-tl-lg" />
        <div className="absolute top-0 right-0 w-8 h-8 border-r-2 border-t-2 border-neon-cyan/50 rounded-tr-lg" />
        <div className="absolute bottom-0 left-0 w-8 h-8 border-l-2 border-b-2 border-neon-cyan/50 rounded-bl-lg" />
        <div className="absolute bottom-0 right-0 w-8 h-8 border-r-2 border-b-2 border-neon-cyan/50 rounded-br-lg" />
        <div className="absolute bottom-4 left-1/2 -translate-x-1/2 text-[10px] text-neon-cyan/40 font-mono tracking-[0.2em] uppercase">
          System_Online :: Secure_Connection_Established
        </div>
      </div>

      <Header />

      <main className="flex-1 flex flex-col lg:flex-row relative z-10 p-4 lg:p-8 gap-8 max-w-[1600px] mx-auto w-full">

        {/* LEFT PANEL: MISSIONS */}
        <section className="flex-1 flex flex-col gap-6 lg:gap-8">

          {/* STEP 1: MISSION INTEL */}
          <div className="relative group">
            <div className="absolute -inset-0.5 bg-gradient-to-r from-neon-cyan/20 to-transparent opacity-0 group-hover:opacity-100 transition duration-500 rounded-lg blur" />
            <div className="relative bg-background/40 border border-neon-cyan/30 p-1 rounded-lg backdrop-blur-md">
              <div className="bg-background/60 p-4 lg:p-6 rounded border border-white/5 space-y-4">
                <div className="flex items-center justify-between border-b border-white/10 pb-3">
                  <h2 className="text-2xl font-display font-bold text-neon-cyan tracking-wider flex items-center gap-3">
                    <span className="flex items-center justify-center w-8 h-8 bg-neon-cyan/10 border border-neon-cyan/50 rounded text-sm">01</span>
                    MISSION INTEL
                  </h2>
                  <div className="flex items-center gap-3">
                    <span className="hidden sm:inline text-xs font-mono text-neon-cyan/60 uppercase tracking-widest">[Job_Description]</span>
                    <Button
                      size="sm"
                      onClick={handleAddJob}
                      className="bg-neon-cyan/10 text-neon-cyan border border-neon-cyan/50 hover:bg-neon-cyan hover:text-black uppercase font-mono tracking-wider transition-all shadow-[0_0_10px_rgba(0,243,255,0.2)]"
                    >
                      <Plus className="h-4 w-4 mr-1.5" />
                      NEW INTEL
                    </Button>
                  </div>
                </div>
                <div className="h-[300px] lg:h-[400px]">
                  <JobPostInput ref={jobInputRef} />
                </div>
              </div>
            </div>
          </div>

          {/* STEP 2: LOADOUT */}
          <div className="relative group">
            <div className="absolute -inset-0.5 bg-gradient-to-r from-neon-pink/20 to-transparent opacity-0 group-hover:opacity-100 transition duration-500 rounded-lg blur" />
            <div className="relative bg-background/40 border border-neon-pink/30 p-1 rounded-lg backdrop-blur-md">
              <div className="bg-background/60 p-4 lg:p-6 rounded border border-white/5 space-y-4">
                <div className="flex items-center justify-between border-b border-white/10 pb-3">
                  <h2 className="text-2xl font-display font-bold text-neon-pink tracking-wider flex items-center gap-3">
                    <span className="flex items-center justify-center w-8 h-8 bg-neon-pink/10 border border-neon-pink/50 rounded text-sm">02</span>
                    LOADOUT
                  </h2>
                  <span className="text-xs font-mono text-neon-pink/60 uppercase tracking-widest">[Resume_Upload]</span>
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
        <section className="lg:w-[450px] flex flex-col gap-6">

          {/* EXECUTE BUTTON */}
          <div className="relative group cursor-pointer active:scale-95 transition-transform duration-100">
            <div className={`absolute inset-0 ${canInitiate ? 'bg-neon-cyan' : 'bg-gray-500'} blur-[20px] opacity-20 group-hover:opacity-40 ${!isLoading && 'animate-pulse'} transition-opacity`} />
            <button
              onClick={handleInitiate}
              disabled={!canInitiate}
              className={`relative w-full overflow-hidden bg-background border-2 ${
                canInitiate
                  ? 'border-neon-cyan text-neon-cyan hover:bg-neon-cyan hover:text-black'
                  : 'border-gray-600 text-gray-500 cursor-not-allowed'
              } transition-all duration-300 p-8 clip-path-polygon group`}
            >
              {/* Tech markings */}
              <div className="absolute top-0 right-0 p-2 text-[10px] font-mono opacity-50">EXE_001</div>
              <div className="absolute bottom-0 left-0 p-2 text-[10px] font-mono opacity-50">
                {hasResume ? 'READY' : 'AWAITING_DATA'}
              </div>

              <div className="flex flex-col items-center gap-2 relative z-10">
                {isLoading ? (
                  <>
                    <Loader2 className="h-8 w-8 animate-spin" />
                    <span className="text-xl font-display font-black tracking-[0.2em] uppercase">
                      PROCESSING
                    </span>
                    <span className="text-sm font-mono tracking-widest opacity-80">
                      {status === "uploading" ? "UPLOADING_RESUME" : "ANALYZING_DATA"}
                    </span>
                  </>
                ) : (
                  <>
                    <span className="text-3xl font-display font-black tracking-[0.2em] uppercase group-hover:drop-shadow-[0_0_10px_rgba(0,0,0,0.5)]">
                      INITIATE
                    </span>
                    <span className="text-sm font-mono tracking-widest opacity-80 group-hover:opacity-100">RUN_ANALYSIS_PROTOCOL</span>
                  </>
                )}
              </div>
            </button>
          </div>

          {/* BATTLE LOG / PREVIEW */}
          <div className="flex-1 min-h-[400px] border border-white/10 rounded-lg bg-black/40 backdrop-blur overflow-hidden relative flex flex-col">
            <div className="bg-white/5 p-2 px-4 border-b border-white/10 flex items-center justify-between">
              <span className="font-mono text-xs text-muted-foreground uppercase">System_Log</span>
              <div className="flex gap-1.5">
                <div className={`w-2 h-2 rounded-full ${status === 'error' ? 'bg-red-500' : 'bg-red-500/50'}`} />
                <div className={`w-2 h-2 rounded-full ${isLoading ? 'bg-yellow-500' : 'bg-yellow-500/50'}`} />
                <div className={`w-2 h-2 rounded-full ${status === 'done' ? 'bg-green-500' : 'bg-green-500/50'}`} />
              </div>
            </div>
            <div className="flex-1 relative">
              <LivePreview status={status} result={result} error={error} />
            </div>
          </div>

        </section>

      </main>

    </div>
  );
}
