"use client";

import { motion } from "framer-motion";
import {
    FileText,
    Target,
    MessagesSquare,
    TrendingUp,
} from "lucide-react";

const features = [
    {
        icon: Target,
        title: "ATS Score Analysis",
        description: "Decodes resume compatibility with high-precision algorithms.",
        color: "from-neon-cyan/20 to-blue-600/20",
        border: "border-neon-cyan/40",
        text: "text-neon-cyan",
        shadow: "hover:shadow-[0_0_30px_rgba(0,243,255,0.2)]"
    },
    {
        icon: MessagesSquare,
        title: "Interview Prep",
        description: "AI simulation for technical and behavioral interrogation scenarios.",
        color: "from-neon-pink/20 to-purple-600/20",
        border: "border-neon-pink/40",
        text: "text-neon-pink",
        shadow: "hover:shadow-[0_0_30px_rgba(188,19,254,0.2)]"
    },
    {
        icon: TrendingUp,
        title: "Skill Gap Analysis",
        description: "Identify critical missing data points in your professional profile.",
        color: "from-neon-yellow/20 to-emerald-500/20",
        border: "border-neon-yellow/40",
        text: "text-neon-yellow",
        shadow: "hover:shadow-[0_0_30px_rgba(204,255,0,0.2)]"
    },
    {
        icon: FileText,
        title: "Multi-Job Match",
        description: "Parallel processing of your resume against multiple target nodes.",
        color: "from-orange-500/20 to-red-500/20",
        border: "border-orange-500/20",
        text: "text-orange-500",
        shadow: "hover:shadow-[0_0_30px_rgba(249,115,22,0.2)]"
    }
];

export function FeatureGrid() {
    return (
        <section className="py-24 relative overflow-hidden">
            {/* Scanlines */}
            <div className="absolute inset-0 pointer-events-none bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.1)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] z-0 bg-[length:100%_2px,3px_100%] opacity-10" />

            <div className="container relative z-10">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    className="text-center mb-16"
                >
                    <h2 className="text-4xl md:text-6xl font-display font-bold mb-4 uppercase tracking-tighter">
                        Upgrade Your <span className="text-neon-cyan drop-shadow-[0_0_10px_rgba(0,243,255,0.8)]">Career_OS</span>
                    </h2>
                    <p className="text-muted-foreground text-lg max-w-2xl mx-auto font-mono">
                        Deploying advanced heuristics to optimize your hiring probability.
                    </p>
                </motion.div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {features.map((feature, index) => (
                        <motion.div
                            key={index}
                            initial={{ opacity: 0, y: 20 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ delay: index * 0.1 }}
                            whileHover={{ y: -5 }}
                            className={`p-6 rounded-xl border ${feature.border} bg-gradient-to-br ${feature.color} backdrop-blur-sm ${feature.shadow} transition-all duration-300 group`}
                        >
                            <div className={`w-12 h-12 rounded-lg bg-black/40 border border-white/5 flex items-center justify-center mb-4 ${feature.text} group-hover:scale-110 transition-transform`}>
                                <feature.icon className="w-6 h-6" />
                            </div>
                            <h3 className="text-xl font-display font-bold mb-2 tracking-wide uppercase">{feature.title}</h3>
                            <p className="text-muted-foreground text-sm leading-relaxed font-sans">
                                {feature.description}
                            </p>
                        </motion.div>
                    ))}
                </div>
            </div>
        </section>
    );
}
