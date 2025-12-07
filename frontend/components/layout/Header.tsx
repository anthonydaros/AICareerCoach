"use client";

import { Terminal, GitBranch, Play } from "lucide-react";

interface HeaderProps {
    onLoadDemo?: () => void;
}

export function Header({ onLoadDemo }: HeaderProps) {
    return (
        <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/80 backdrop-blur-md supports-[backdrop-filter]:bg-background/60">
            <div className="flex h-16 items-center px-6 font-sans text-sm">
                <div className="flex items-center gap-3 mr-10 group cursor-pointer">
                    <div className="relative flex items-center justify-center">
                        <Terminal className="h-5 w-5 text-neon-cyan transition-all group-hover:drop-shadow-[0_0_8px_rgba(0,243,255,0.8)]" />
                    </div>
                    <span className="font-display font-bold text-xl tracking-wider uppercase text-foreground group-hover:text-neon-cyan transition-colors duration-300">
                        Career<span className="text-neon-pink">.AI</span>
                    </span>
                </div>


                <div className="ml-auto flex items-center gap-4 sm:gap-6">
                    {onLoadDemo && (
                        <button
                            onClick={onLoadDemo}
                            aria-label="Load demo data to see how the app works"
                            className="flex items-center gap-2 px-3 py-1.5 text-xs font-mono uppercase tracking-wider
                                       bg-neon-pink/10 text-neon-pink border border-neon-pink/50 rounded
                                       hover:bg-neon-pink hover:text-black transition-all duration-300
                                       shadow-[0_0_10px_rgba(188,19,254,0.2)] hover:shadow-[0_0_20px_rgba(188,19,254,0.4)]
                                       focus:outline-none focus:ring-2 focus:ring-neon-pink focus:ring-offset-2 focus:ring-offset-background"
                        >
                            <Play className="h-3 w-3" aria-hidden="true" />
                            <span>Demo</span>
                        </button>
                    )}
                    <div className="flex items-center gap-2 text-xs text-muted-foreground/60 font-mono hidden sm:flex">
                        <GitBranch className="h-3 w-3" aria-hidden="true" />
                        <span>v.0.2.1-alpha</span>
                    </div>
                    <div className="h-4 w-[1px] bg-border/50 hidden sm:block" aria-hidden="true" />
                    <div className="flex items-center gap-2 text-xs text-neon-yellow" role="status" aria-live="polite">
                        <div className="relative" aria-hidden="true">
                            <div className="h-2 w-2 rounded-full bg-neon-yellow" />
                            <div className="absolute top-0 left-0 h-2 w-2 rounded-full bg-neon-yellow animate-ping opacity-75" />
                        </div>
                        <span className="font-medium tracking-wide uppercase">System Online</span>
                    </div>
                </div>
            </div>
        </header>
    );
}
