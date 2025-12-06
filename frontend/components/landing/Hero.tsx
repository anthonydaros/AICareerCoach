"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { ArrowRight, Upload, BrainCircuit, Terminal } from "lucide-react";

export function Hero() {
    return (
        <section className="relative pt-32 pb-20 md:pt-48 md:pb-32 overflow-hidden selection:bg-neon-pink/30">
            {/* Background Effects */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[500px] bg-neon-cyan/20 blur-[120px] rounded-full pointer-events-none opacity-20" />
            <div className="absolute bottom-0 right-0 w-[800px] h-[600px] bg-neon-pink/10 blur-[100px] rounded-full pointer-events-none opacity-20" />

            <div className="container relative z-10">
                <div className="mx-auto max-w-5xl text-center">
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6, ease: "easeOut" }}
                    >
                        <div className="inline-flex items-center gap-2 rounded-full border border-neon-cyan/30 bg-neon-cyan/5 px-4 py-1.5 text-xs font-mono tracking-wider text-neon-cyan mb-8 shadow-[0_0_15px_-3px_rgba(0,243,255,0.3)]">
                            <span className="relative flex h-2 w-2">
                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-neon-cyan opacity-75"></span>
                                <span className="relative inline-flex rounded-full h-2 w-2 bg-neon-cyan"></span>
                            </span>
                            SYSTEM_READY :: V.2.0
                        </div>

                        <h1 className="text-5xl md:text-7xl lg:text-8xl font-display font-bold tracking-tight mb-8 leading-tight">
                            HACK THE <br />
                            <span className="text-transparent bg-clip-text bg-gradient-to-r from-neon-cyan via-white to-neon-pink drop-shadow-[0_0_10px_rgba(0,243,255,0.5)]">
                                JOB MARKET
                            </span>
                        </h1>

                        <p className="text-lg md:text-xl text-muted-foreground mb-12 max-w-2xl mx-auto leading-relaxed font-sans font-light">
                            Advanced AI protocols to bypass ATS firewalls. <br />
                            <span className="text-foreground">Analyze. Optimize. Dominate.</span>
                        </p>

                        <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
                            <Button size="lg" className="h-14 px-10 text-lg bg-neon-cyan text-black hover:bg-neon-cyan/90 shadow-[0_0_20px_rgba(0,243,255,0.4)] hover:shadow-[0_0_30px_rgba(0,243,255,0.6)] transition-all hover:scale-105 font-bold tracking-wide">
                                <Upload className="mr-2 h-5 w-5" />
                                INITIATE SCAN
                            </Button>
                            <Button size="lg" variant="outline" className="h-14 px-10 text-lg border-neon-pink/50 text-neon-pink hover:bg-neon-pink/10 hover:border-neon-pink hover:shadow-[0_0_20px_rgba(188,19,254,0.3)] transition-all backdrop-blur-sm font-mono">
                                <Terminal className="mr-2 h-5 w-5" />
                                RUN DEMO_MODE
                            </Button>
                        </div>
                    </motion.div>
                </div>
            </div>
        </section>
    );
}
