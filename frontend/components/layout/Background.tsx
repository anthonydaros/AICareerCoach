"use client";

import { motion } from "framer-motion";

export function Background() {
    return (
        <div className="fixed inset-0 -z-50 overflow-hidden bg-background">
            {/* 
        Aurora Effect: Large blurred orbs moving slowly in the background 
        colors: Indigo, Purple, Blue, Cyan
      */}
            <motion.div
                animate={{
                    scale: [1, 1.2, 1],
                    opacity: [0.3, 0.5, 0.3],
                    x: [0, 50, 0],
                    y: [0, -50, 0],
                }}
                transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
                className="absolute -top-[10%] -left-[10%] w-[50vw] h-[50vw] rounded-full bg-primary/20 blur-[100px]"
            />
            <motion.div
                animate={{
                    scale: [1, 1.1, 1],
                    opacity: [0.3, 0.6, 0.3],
                    x: [0, -30, 0],
                    y: [0, 50, 0],
                }}
                transition={{ duration: 15, repeat: Infinity, ease: "easeInOut", delay: 2 }}
                className="absolute top-[20%] -right-[10%] w-[40vw] h-[40vw] rounded-full bg-purple-500/20 blur-[100px]"
            />
            <motion.div
                animate={{
                    scale: [1, 1.3, 1],
                    opacity: [0.2, 0.4, 0.2],
                }}
                transition={{ duration: 20, repeat: Infinity, ease: "easeInOut", delay: 5 }}
                className="absolute bottom-0 left-[20%] w-[60vw] h-[40vw] rounded-full bg-cyan-500/10 blur-[120px]"
            />

            {/* Grid Overlay for technical feel */}
            <div className="absolute inset-0 bg-[url('/grid-pattern.svg')] opacity-[0.03] pointer-events-none" />
        </div>
    );
}
