"use client";

import { useState, useEffect, useRef, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";

const HACKER_LINES_UPLOAD = [
  "// Initializing document parser...",
  "const parser = new ResumeDecoder();",
  "await parser.loadBinaryStream(file);",
  "",
  "// Extracting raw text data...",
  "const buffer = parser.decodeBuffer();",
  "const text = buffer.toString('utf-8');",
  "",
  "// Validating document structure...",
  "if (!parser.validateFormat()) {",
  "  throw new ParseError('INVALID_FORMAT');",
  "}",
  "",
  "// Document parsed successfully",
  "return { text, metadata };",
];

const HACKER_LINES_ANALYZE = [
  "// Initializing CareerAI neural engine...",
  "import { CareerAI } from '@anthropic/career';",
  "const ai = new CareerAI({ model: 'careerai' });",
  "",
  "// Loading skill taxonomy database...",
  "const taxonomy = await ai.loadSkillGraph();",
  "console.log('[OK] 50,000+ skills indexed');",
  "",
  "// Extracting candidate profile...",
  "const profile = ai.extractProfile(resume);",
  "const skills = profile.skills.map(s => ({",
  "  name: s.name,",
  "  level: s.proficiency,",
  "  years: s.experience",
  "}));",
  "",
  "// Cross-referencing job requirements...",
  "for (const job of jobPostings) {",
  "  const match = ai.calculateMatch(profile, job);",
  "  const gaps = ai.identifyGaps(profile, job);",
  "  results.push({ job, match, gaps });",
  "}",
  "",
  "// Computing ATS compatibility score...",
  "const ats = ai.computeATSScore({",
  "  skills: profile.skills,",
  "  experience: profile.experience,",
  "  keywords: extractKeywords(jobs)",
  "});",
  "",
  "// Generating career insights...",
  "const seniority = ai.detectSeniority(profile);",
  "const stability = ai.analyzeCareerPath(profile);",
  "const bestFit = ai.findBestMatch(results);",
  "",
  "// Compiling comprehensive report...",
  "return {",
  "  ats_result: ats,",
  "  job_matches: results,",
  "  seniority, stability, bestFit",
  "};",
];

// Matrix rain characters
const MATRIX_CHARS = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789";

interface MatrixColumnProps {
  delay: number;
  duration: number;
  left: string;
}

function MatrixColumn({ delay, duration, left }: MatrixColumnProps) {
  const chars = useMemo(() => {
    return Array.from({ length: 20 }, () =>
      MATRIX_CHARS[Math.floor(Math.random() * MATRIX_CHARS.length)]
    ).join("\n");
  }, []);

  return (
    <motion.div
      className="absolute top-0 text-neon-green/30 text-[8px] leading-none font-mono whitespace-pre pointer-events-none select-none"
      style={{ left }}
      initial={{ y: -200, opacity: 0 }}
      animate={{ y: 400, opacity: [0, 0.5, 0.5, 0] }}
      transition={{
        duration,
        delay,
        repeat: Infinity,
        repeatDelay: Math.random() * 3,
        ease: "linear",
      }}
    >
      {chars}
    </motion.div>
  );
}

interface TerminalTypewriterProps {
  status: "uploading" | "analyzing";
}

export function TerminalTypewriter({ status }: TerminalTypewriterProps) {
  const [lines, setLines] = useState<string[]>([]);
  const [currentLineIndex, setCurrentLineIndex] = useState(0);
  const [currentCharIndex, setCurrentCharIndex] = useState(0);
  const [isComplete, setIsComplete] = useState(false);
  const [glitchText, setGlitchText] = useState("");
  const containerRef = useRef<HTMLDivElement>(null);

  const HACKER_LINES = status === "uploading" ? HACKER_LINES_UPLOAD : HACKER_LINES_ANALYZE;

  // Matrix rain columns
  const matrixColumns = useMemo(() => {
    return Array.from({ length: 15 }, (_, i) => ({
      delay: Math.random() * 5,
      duration: 3 + Math.random() * 4,
      left: `${(i / 15) * 100}%`,
    }));
  }, []);

  // Reset when status changes
  useEffect(() => {
    setLines([]);
    setCurrentLineIndex(0);
    setCurrentCharIndex(0);
    setIsComplete(false);
  }, [status]);

  // Glitch effect on status text
  useEffect(() => {
    const glitchChars = "!@#$%^&*()_+-=[]{}|;':\",./<>?";
    const originalText = status === "uploading"
      ? "PARSING RESUME DATA"
      : "NEURAL ANALYSIS IN PROGRESS";

    const interval = setInterval(() => {
      if (Math.random() > 0.7) {
        const glitched = originalText.split("").map((char, i) =>
          Math.random() > 0.9 ? glitchChars[Math.floor(Math.random() * glitchChars.length)] : char
        ).join("");
        setGlitchText(glitched);
        setTimeout(() => setGlitchText(""), 100);
      }
    }, 500);

    return () => clearInterval(interval);
  }, [status]);

  // Typing effect
  useEffect(() => {
    if (isComplete) return;
    if (currentLineIndex >= HACKER_LINES.length) {
      setIsComplete(true);
      return;
    }

    const currentLine = HACKER_LINES[currentLineIndex];

    // Handle empty lines quickly
    if (currentLine === "") {
      const timeout = setTimeout(() => {
        setLines(prev => [...prev, ""]);
        setCurrentLineIndex(i => i + 1);
        setCurrentCharIndex(0);
      }, 100);
      return () => clearTimeout(timeout);
    }

    if (currentCharIndex < currentLine.length) {
      // Type next character
      const timeout = setTimeout(() => {
        setLines(prev => {
          const updated = [...prev];
          if (updated.length <= currentLineIndex) {
            updated.push("");
          }
          updated[currentLineIndex] = currentLine.slice(0, currentCharIndex + 1);
          return updated;
        });
        setCurrentCharIndex(c => c + 1);
      }, 15 + Math.random() * 25);
      return () => clearTimeout(timeout);
    } else {
      // Move to next line
      const timeout = setTimeout(() => {
        setCurrentLineIndex(i => i + 1);
        setCurrentCharIndex(0);
      }, 100);
      return () => clearTimeout(timeout);
    }
  }, [currentLineIndex, currentCharIndex, isComplete, HACKER_LINES]);

  // Auto-scroll to bottom
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [lines]);

  const getLineColor = (line: string) => {
    if (line.startsWith("//")) return "text-muted-foreground/60";
    if (line.includes("console.log")) return "text-neon-green";
    if (line.includes("const ") || line.includes("let ") || line.includes("for ") || line.includes("import ")) return "text-neon-pink";
    if (line.includes("await ") || line.includes("return ") || line.includes("throw ")) return "text-neon-yellow";
    if (line.includes("{") || line.includes("}") || line.includes("if ")) return "text-foreground";
    return "text-neon-cyan";
  };

  const statusText = glitchText || (status === "uploading" ? "PARSING RESUME DATA" : "NEURAL ANALYSIS IN PROGRESS");

  return (
    <div className="flex flex-col h-full relative overflow-hidden">
      {/* Matrix rain background */}
      <div className="absolute inset-0 overflow-hidden opacity-30 pointer-events-none">
        {matrixColumns.map((col, i) => (
          <MatrixColumn key={i} {...col} />
        ))}
      </div>

      {/* Status header */}
      <div className="flex items-center gap-3 mb-4 pb-3 border-b border-neon-cyan/20 relative z-10">
        <div className="flex gap-1">
          <motion.div
            className="w-2 h-2 rounded-full bg-red-500"
            animate={{ opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 1, repeat: Infinity }}
          />
          <motion.div
            className="w-2 h-2 rounded-full bg-yellow-500"
            animate={{ opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 1, repeat: Infinity, delay: 0.3 }}
          />
          <motion.div
            className="w-2 h-2 rounded-full bg-green-500"
            animate={{ opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 1, repeat: Infinity, delay: 0.6 }}
          />
        </div>
        <span className="text-[10px] font-mono text-muted-foreground uppercase tracking-widest">
          {statusText}...
        </span>
        <motion.div
          animate={{ opacity: [0.3, 1, 0.3] }}
          transition={{ duration: 1, repeat: Infinity }}
          className="ml-auto w-2 h-2 rounded-full bg-neon-cyan shadow-[0_0_10px_rgba(0,243,255,0.8)]"
        />
      </div>

      {/* Terminal content */}
      <div
        ref={containerRef}
        className="flex-1 overflow-auto font-mono text-xs leading-relaxed scrollbar-thin scrollbar-thumb-muted-foreground/20 scrollbar-track-transparent relative z-10"
      >
        {lines.map((line, i) => (
          <motion.div
            key={i}
            className="flex"
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.1 }}
          >
            <span className="text-neon-cyan/40 w-8 text-right pr-3 select-none">
              {String(i + 1).padStart(2, "0")}
            </span>
            <span className={getLineColor(line)}>
              {line}
              {i === currentLineIndex && !isComplete && (
                <motion.span
                  animate={{ opacity: [1, 0] }}
                  transition={{ duration: 0.4, repeat: Infinity }}
                  className="inline-block w-2 h-3.5 bg-neon-cyan ml-0.5 align-middle shadow-[0_0_5px_rgba(0,243,255,0.8)]"
                />
              )}
            </span>
          </motion.div>
        ))}

        {/* Progress section */}
        <AnimatePresence>
          {!isComplete && (
            <motion.div
              className="mt-6 pt-4 border-t border-border/30"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <div className="flex items-center gap-3 mb-3">
                <span className="text-[10px] text-muted-foreground uppercase">Processing</span>
                <div className="flex-1 h-2 bg-black/60 rounded-full overflow-hidden border border-neon-cyan/20">
                  <motion.div
                    className="h-full bg-gradient-to-r from-neon-cyan via-neon-pink to-neon-cyan bg-[length:200%_100%]"
                    initial={{ width: "0%" }}
                    animate={{
                      width: `${Math.min((currentLineIndex / HACKER_LINES.length) * 100, 95)}%`,
                      backgroundPosition: ["0% 0%", "100% 0%"],
                    }}
                    transition={{
                      width: { duration: 0.3 },
                      backgroundPosition: { duration: 2, repeat: Infinity, ease: "linear" }
                    }}
                  />
                </div>
                <span className="text-[10px] font-mono text-neon-cyan w-12 text-right">
                  {Math.min(Math.round((currentLineIndex / HACKER_LINES.length) * 100), 95)}%
                </span>
              </div>

              {/* Additional stats */}
              <div className="grid grid-cols-3 gap-2 text-[9px] font-mono">
                <div className="bg-black/40 rounded px-2 py-1 border border-neon-cyan/10">
                  <span className="text-muted-foreground">Lines:</span>
                  <span className="text-neon-cyan ml-1">{currentLineIndex}</span>
                </div>
                <div className="bg-black/40 rounded px-2 py-1 border border-neon-pink/10">
                  <span className="text-muted-foreground">Ops:</span>
                  <span className="text-neon-pink ml-1">{currentLineIndex * 47}</span>
                </div>
                <div className="bg-black/40 rounded px-2 py-1 border border-neon-yellow/10">
                  <span className="text-muted-foreground">Time:</span>
                  <span className="text-neon-yellow ml-1">{(currentLineIndex * 0.8).toFixed(1)}s</span>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Completion state */}
        <AnimatePresence>
          {isComplete && (
            <motion.div
              className="mt-4 pt-4 border-t border-neon-green/30"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="flex items-center gap-2 text-neon-green text-[10px]">
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
                >
                  <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
                  </svg>
                </motion.div>
                <span className="uppercase tracking-wider font-bold">Analysis Complete</span>
                <motion.span
                  animate={{ opacity: [0, 1, 0] }}
                  transition={{ duration: 1, repeat: Infinity }}
                  className="text-neon-green"
                >
                  _
                </motion.span>
              </div>
              <p className="text-[9px] text-muted-foreground mt-2">
                Rendering results... Please wait
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
