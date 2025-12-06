"use client";

import { ScrollArea } from "@/components/ui/scroll-area";
import { Activity, Terminal } from "lucide-react";

export function LivePreview() {
    return (
        <div className="h-full flex flex-col font-mono text-sm bg-background/40 backdrop-blur border-l border-border/40">
            <div className="flex items-center justify-between border-b border-border/40 px-4 py-3 bg-muted/10">
                <div className="flex items-center gap-2">
                    <Activity className="h-4 w-4 text-neon-pink animate-pulse" />
                    <span className="font-display font-bold tracking-wide text-foreground">LIVE OUTPUT STREAM</span>
                </div>
                <div className="flex items-center gap-2 text-[10px] text-muted-foreground uppercase">
                    <div className="h-1.5 w-1.5 rounded-full bg-neon-green/80" />
                    <span>WebSocket Connected</span>
                </div>
            </div>

            <div className="flex-1 p-4 overflow-auto scrollbar-thin scrollbar-thumb-muted-foreground/20 scrollbar-track-transparent">
                <div className="space-y-4">
                    <div className="text-muted-foreground/50 pb-2 border-b border-dashed border-border/30 italic">
            // System awaiting input stream...
                        <br />
            // Ready to analyze resume vs job description
                    </div>

                    <div className="opacity-80 font-mono text-sm leading-relaxed">
                        <span className="text-neon-pink">const</span> <span className="text-neon-cyan">analysis_result</span> = <span className="text-foreground">{"{"}</span>
                        <div className="pl-6 border-l border-border/20 ml-1">
                            <div>
                                <span className="text-neon-yellow">match_score</span>: <span className="text-muted-foreground">null</span>,
                            </div>
                            <div>
                                <span className="text-neon-yellow">missing_skills</span>: <span className="text-foreground">[]</span>,
                            </div>
                            <div>
                                <span className="text-neon-yellow">recommendations</span>: <span className="text-foreground">[]</span>,
                            </div>
                            <div className="text-muted-foreground/40">
                                // ... awaiting data
                            </div>
                        </div>
                        <span className="text-foreground">{"}"}</span>
                    </div>
                </div>

                {/* Scanline Effect Overlay */}
                <div className="absolute inset-0 pointer-events-none bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.1)_50%),linear-gradient(90deg,rgba(255,0,0,0.03),rgba(0,255,0,0.01),rgba(0,0,255,0.03))] z-50 bg-[length:100%_2px,3px_100%] opacity-20 user-select-none" />
            </div>
        </div>
    );
}
