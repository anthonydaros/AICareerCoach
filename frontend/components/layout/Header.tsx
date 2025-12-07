"use client";

import { Terminal, GitBranch, Play, Menu } from "lucide-react";
import { Sheet, SheetContent, SheetTrigger, SheetTitle, SheetDescription } from "@/components/ui/sheet";


interface HeaderProps {
    onLoadDemo?: () => void;
}

export function Header({ onLoadDemo }: HeaderProps) {
    return (
        <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/80 backdrop-blur-md supports-[backdrop-filter]:bg-background/60">
            <div className="flex h-16 items-center justify-between px-6 font-sans text-sm">
                <div className="flex items-center gap-3 group cursor-pointer">
                    <div className="relative flex items-center justify-center">
                        <Terminal className="h-5 w-5 text-neon-cyan transition-all group-hover:drop-shadow-[0_0_8px_rgba(0,243,255,0.8)]" />
                    </div>
                    <span className="font-display font-bold text-xl tracking-wider uppercase text-foreground group-hover:text-neon-cyan transition-colors duration-300">
                        Career<span className="text-neon-pink">.AI</span>
                    </span>
                </div>

                {/* DESKTOP MENU */}
                <div className="hidden sm:flex items-center gap-4 sm:gap-6 ml-auto">
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
                    <div className="flex items-center gap-2 text-xs text-muted-foreground/60 font-mono">
                        <GitBranch className="h-3 w-3" aria-hidden="true" />
                        <span>v.0.2.1-alpha</span>
                    </div>
                    <div className="h-4 w-[1px] bg-border/50" aria-hidden="true" />
                    <div className="flex items-center gap-2 text-xs text-neon-yellow" role="status" aria-live="polite">
                        <div className="relative" aria-hidden="true">
                            <div className="h-2 w-2 rounded-full bg-neon-yellow" />
                            <div className="absolute top-0 left-0 h-2 w-2 rounded-full bg-neon-yellow animate-ping opacity-75" />
                        </div>
                        <span className="font-medium tracking-wide uppercase">System Online</span>
                    </div>
                </div>

                {/* MOBILE MENU */}
                <div className="sm:hidden ml-auto">
                    <Sheet>
                        <SheetTrigger asChild>
                            <button className="p-2 text-neon-cyan hover:bg-neon-cyan/10 rounded-md transition-colors" aria-label="Open Menu">
                                <Menu className="h-6 w-6" />
                            </button>
                        </SheetTrigger>
                        <SheetContent side="right" className="bg-background/95 backdrop-blur-xl border-l border-border/50 w-[300px]">
                            <SheetTitle className="sr-only">Mobile Menu</SheetTitle>
                            <SheetDescription className="sr-only">Navigation and Actions</SheetDescription>
                            <div className="flex flex-col gap-8 mt-10">
                                <div className="flex flex-col gap-4">
                                    <div className="text-xs font-mono text-muted-foreground uppercase tracking-widest mb-2">Actions</div>
                                    {onLoadDemo && (
                                        <button
                                            onClick={onLoadDemo}
                                            className="flex items-center justify-between px-4 py-3 text-sm font-mono uppercase tracking-wider
                                                       bg-neon-pink/10 text-neon-pink border border-neon-pink/50 rounded
                                                       hover:bg-neon-pink hover:text-black transition-all duration-300"
                                        >
                                            <span className="flex items-center gap-3">
                                                <Play className="h-4 w-4" />
                                                Demo
                                            </span>
                                        </button>
                                    )}
                                </div>

                                <div className="flex flex-col gap-4">
                                    <div className="text-xs font-mono text-muted-foreground uppercase tracking-widest mb-2">Status</div>
                                    <div className="flex items-center justify-between px-4 py-3 rounded bg-white/5 border border-white/10">
                                        <span className="text-sm font-medium text-neon-yellow uppercase">System</span>
                                        <div className="flex items-center gap-2">
                                            <div className="relative flex h-2 w-2">
                                                <div className="animate-ping absolute inline-flex h-full w-full rounded-full bg-neon-yellow opacity-75"></div>
                                                <div className="relative inline-flex rounded-full h-2 w-2 bg-neon-yellow"></div>
                                            </div>
                                            <span className="text-xs text-neon-yellow font-mono">ONLINE</span>
                                        </div>
                                    </div>
                                    <div className="flex items-center justify-between px-4 py-3 rounded bg-white/5 border border-white/10">
                                        <span className="text-sm font-medium text-muted-foreground uppercase">Version</span>
                                        <span className="text-xs font-mono text-muted-foreground">v.0.2.1-alpha</span>
                                    </div>
                                </div>
                            </div>
                        </SheetContent>
                    </Sheet>
                </div>
            </div>
        </header>
    );
}
