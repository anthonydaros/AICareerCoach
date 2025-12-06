"use client";

import Link from "next/link";
import { Terminal, GitBranch, Settings } from "lucide-react";

export function Header() {
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

                <nav className="flex items-center gap-8 hidden md:flex">
                    <Link href="/" className="flex items-center gap-2 text-muted-foreground hover:text-neon-cyan transition-colors duration-300 group">
                        <span className="text-neon-cyan text-xs font-mono opacity-60 group-hover:opacity-100">[01]</span>
                        <span className="tracking-wide">Dashboard</span>
                    </Link>
                    <Link href="/history" className="flex items-center gap-2 text-muted-foreground hover:text-neon-pink transition-colors duration-300 group">
                        <span className="text-neon-pink text-xs font-mono opacity-60 group-hover:opacity-100">[02]</span>
                        <span className="tracking-wide">History</span>
                    </Link>
                </nav>

                <div className="ml-auto flex items-center gap-6">
                    <div className="flex items-center gap-2 text-xs text-muted-foreground/60 font-mono hidden sm:flex">
                        <GitBranch className="h-3 w-3" />
                        <span>v.0.2.1-alpha</span>
                    </div>
                    <div className="h-4 w-[1px] bg-border/50 hidden sm:block" />
                    <div className="flex items-center gap-2 text-xs text-neon-yellow">
                        <div className="relative">
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
