
"use client";

import { useState, useEffect, forwardRef, useImperativeHandle } from "react";
import { ClipboardPaste, Trash2, Code2, Plus, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { motion, AnimatePresence } from "framer-motion";

interface Job {
    id: string;
    text: string;
}

export interface JobPostInputRef {
    addJob: () => void;
    getJobs: () => Job[];
    setJobs: (jobs: Job[]) => void;
}

export const JobPostInput = forwardRef<JobPostInputRef>((props, ref) => {
    const [jobs, setJobs] = useState<Job[]>([{ id: '1', text: '' }]);
    const [activeId, setActiveId] = useState<string>('1');

    useImperativeHandle(ref, () => ({
        addJob: () => {
            const newId = Date.now().toString();
            setJobs(prev => [...prev, { id: newId, text: '' }]);
            setActiveId(newId);
        },
        getJobs: () => jobs.filter(j => j.text.trim().length > 0),
        setJobs: (newJobs: Job[]) => {
            if (newJobs.length > 0) {
                setJobs(newJobs);
                setActiveId(newJobs[0].id);
            }
        },
    }));

    const activeJob = jobs.find(j => j.id === activeId) || jobs[0];

    const removeJob = (e: React.MouseEvent, id: string) => {
        e.stopPropagation();
        if (jobs.length === 1) {
            updateJob(id, '');
            return;
        }
        const newJobs = jobs.filter(j => j.id !== id);
        setJobs(newJobs);
        if (id === activeId) {
            setActiveId(newJobs[newJobs.length - 1].id);
        }
    };

    const updateJob = (id: string, newText: string) => {
        setJobs(jobs.map(j => j.id === id ? { ...j, text: newText } : j));
    };

    const handlePaste = async () => {
        try {
            const text = await navigator.clipboard.readText();
            updateJob(activeId, text);
        } catch (err) {
            console.error('Failed to read clipboard');
        }
    };

    // Calculate visual order: Active is index 0 (front), others follow
    const renderStack = () => {
        const active = jobs.find(j => j.id === activeId);
        const others = jobs.filter(j => j.id !== activeId);
        return [active, ...others].filter(Boolean) as Job[];
    }

    const displayJobs = renderStack();
    const CARD_OFFSET = 18;
    const SCALE_FACTOR = 0.06;

    return (
        <div className="h-full flex flex-col relative group" role="region" aria-label="Job postings input area">
            {/* Screen reader announcements */}
            <div className="sr-only" aria-live="polite" aria-atomic="true" id="job-announcements">
                {jobs.length} job posting{jobs.length !== 1 ? 's' : ''} in stack
            </div>

            {/* STACK STATUS - Button moved to parent */}
            <div className="flex items-center justify-end mb-2 px-1 z-50 relative h-6">
                {/* Only showing count if multiple, largely decorative now */}
                {jobs.length > 1 && (
                    <span className="text-[10px] font-mono text-neon-cyan/60 uppercase tracking-widest bg-black/50 px-2 py-1 rounded border border-white/10" aria-hidden="true">
                        Stack_Depth: {jobs.length}
                    </span>
                )}
            </div>

            {/* STACK CONTAINER */}
            <div className="flex-1 relative pt-12 md:pt-14">
                <AnimatePresence>
                    {displayJobs.map((job, index) => {
                        if (index > 2) return null;

                        return (
                            <motion.div
                                key={job.id}
                                layoutId={job.id}
                                onClick={() => setActiveId(job.id)}
                                initial={{ opacity: 0, scale: 0.9, y: 0 }}
                                animate={{
                                    top: index * -CARD_OFFSET,
                                    scale: 1 - index * SCALE_FACTOR,
                                    zIndex: displayJobs.length - index,
                                    opacity: 1,
                                }}
                                exit={{ opacity: 0, scale: 0.8, transition: { duration: 0.2 } }}
                                transition={{ type: "spring", stiffness: 200, damping: 20 }}
                                className={cn(
                                    "absolute inset-0 border rounded-xl overflow-hidden shadow-2xl origin-top transition-colors duration-200",
                                    index === 0
                                        ? "border-neon-cyan/50 bg-black/90 shadow-[0_-10px_40px_rgba(0,243,255,0.15)]"
                                        : "border-white/10 bg-black/80 cursor-pointer hover:bg-black/70 hover:border-white/20"
                                )}
                                style={{
                                    transformOrigin: "top center"
                                }}
                            >
                                {/* Card Header */}
                                <div className={cn(
                                    "h-9 flex items-center justify-between px-3 border-b transition-colors select-none",
                                    index === 0 ? "bg-neon-cyan/5 border-neon-cyan/20" : "bg-white/5 border-white/5"
                                )}>
                                    <div className="flex items-center gap-2 text-[10px] font-mono tracking-widest uppercase">
                                        <Code2 className={cn("h-3 w-3", index === 0 ? "text-neon-cyan" : "text-muted-foreground")} />
                                        <span className={index === 0 ? "text-neon-cyan" : "text-muted-foreground"}>
                                            Mission_Data_{jobs.findIndex(j => j.id === job.id) + 1}
                                        </span>
                                    </div>
                                    {index === 0 && (
                                        <button
                                            onClick={(e) => removeJob(e, job.id)}
                                            aria-label={`Remove job posting ${jobs.findIndex(j => j.id === job.id) + 1}`}
                                            className="hover:text-red-500 text-muted-foreground transition-colors p-1 focus:outline-none focus:ring-2 focus:ring-red-500 rounded"
                                        >
                                            <X className="h-3 w-3" aria-hidden="true" />
                                        </button>
                                    )}
                                </div>

                                {/* Editor Area - Only interactive if index 0 */}
                                <div className="absolute inset-0 top-9 p-4 bg-transparent">
                                    <textarea
                                        id={`job-textarea-${job.id}`}
                                        value={job.text}
                                        onChange={(e) => updateJob(job.id, e.target.value)}
                                        disabled={index !== 0}
                                        aria-label={`Job posting ${jobs.findIndex(j => j.id === job.id) + 1} description`}
                                        aria-describedby={index === 0 ? "job-input-instructions" : undefined}
                                        className={cn(
                                            "w-full h-full bg-transparent resize-none outline-none font-mono text-sm leading-relaxed",
                                            "placeholder:text-muted-foreground/30 selection:bg-neon-cyan/30",
                                            "focus:ring-2 focus:ring-neon-cyan/50 focus:ring-inset rounded",
                                            index !== 0 ? "pointer-events-none text-muted-foreground/50" : "text-white"
                                        )}
                                        placeholder={index === 0 ? "> PASTE JOB MISSION DATA..." : ""}
                                        spellCheck={false}
                                    />
                                    {index === 0 && (
                                        <p id="job-input-instructions" className="sr-only">
                                            Paste or type the job posting description here. You can add multiple job postings using the New Intel button.
                                        </p>
                                    )}
                                </div>

                                {/* Active Card Controls */}
                                {index === 0 && (
                                    <motion.div
                                        initial={{ opacity: 0 }}
                                        animate={{ opacity: 1 }}
                                        className="absolute bottom-4 right-4 flex gap-2"
                                    >
                                        <Button
                                            variant="outline"
                                            size="sm"
                                            onClick={() => updateJob(job.id, '')}
                                            aria-label="Clear job posting text"
                                            className="h-7 border-red-500/30 text-red-400 hover:bg-red-500/10 hover:border-red-500 hover:text-red-500 text-[10px] font-mono uppercase tracking-wider"
                                        >
                                            <Trash2 className="h-3 w-3 mr-1" aria-hidden="true" />
                                            Clear
                                        </Button>
                                        <Button
                                            variant="default"
                                            size="sm"
                                            onClick={handlePaste}
                                            aria-label="Paste job posting from clipboard"
                                            className="h-7 bg-neon-cyan/10 text-neon-cyan border border-neon-cyan/50 hover:bg-neon-cyan hover:text-black text-[10px] font-mono uppercase tracking-wider shadow-[0_0_10px_rgba(0,243,255,0.2)]"
                                        >
                                            <ClipboardPaste className="h-3 w-3 mr-1" aria-hidden="true" />
                                            Paste
                                        </Button>
                                    </motion.div>
                                )}
                            </motion.div>
                        );
                    })}
                </AnimatePresence>

                {/* Empty State */}
                {jobs.length === 0 && (
                    <div className="absolute inset-0 flex items-center justify-center border border-white/10 rounded-lg border-dashed">
                        {/* This placeholder button will also call the exposed method via parent if clicked? 
                           No, we need to pass a prop or just rely on parent button. 
                           Actually, having a button here too is fine as a fallback. */}
                        <div className="text-center">
                            <p className="text-muted-foreground text-sm mb-2">No active missions.</p>
                            <p className="text-[10px] text-muted-foreground/50">Click "NEW INTEL" to start.</p>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
});

JobPostInput.displayName = "JobPostInput";

