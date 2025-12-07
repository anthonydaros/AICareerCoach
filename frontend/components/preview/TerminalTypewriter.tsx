"use client";

import { useState, useEffect, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";

// Hacker content for upload phase (~60 lines)
const HACKER_LINES_UPLOAD = [
  "// boot: resume_parser_v3.7.2",
  "sys.init({ mode: 'binary_decode' });",
  "console.log('[SYS] Initializing parser...');",
  "",
  "const parser = new DocumentParser();",
  "parser.setEncoding('utf-8');",
  "parser.enableOCR(true);",
  "parser.setMaxFileSize(10 * 1024 * 1024);",
  "",
  "// Loading file into memory buffer...",
  "const fileBuffer = await fs.readFile(path);",
  "const checksum = crypto.hash('sha256', fileBuffer);",
  "console.log(`[OK] Checksum: ${checksum.slice(0,8)}`);",
  "console.log(`[OK] File size: ${fileBuffer.length} bytes`);",
  "",
  "// Detecting document format...",
  "const format = parser.detectFormat(fileBuffer);",
  "const mimeType = parser.getMimeType(fileBuffer);",
  "console.log(`[OK] Format: ${format} (${mimeType})`);",
  "",
  "if (format === 'PDF') {",
  "  await parser.loadPDFEngine();",
  "  const pdfMeta = parser.extractPDFMetadata();",
  "  console.log(`[OK] PDF pages: ${pdfMeta.pages}`);",
  "} else if (format === 'DOCX') {",
  "  await parser.loadXMLExtractor();",
  "  const docMeta = parser.extractDocMetadata();",
  "  console.log(`[OK] Word count: ${docMeta.words}`);",
  "}",
  "",
  "// Extracting raw text content...",
  "const rawText = await parser.extract();",
  "const wordCount = rawText.split(/\\s+/).length;",
  "console.log(`[OK] Extracted ${wordCount} words`);",
  "",
  "// Splitting into sections...",
  "const sections = parser.splitSections(rawText);",
  "console.log(`[OK] Found ${sections.length} sections`);",
  "",
  "// Identifying section types...",
  "for (const section of sections) {",
  "  section.type = parser.classifySection(section);",
  "  section.confidence = parser.getConfidence();",
  "}",
  "",
  "// Validating document structure...",
  "const isValid = parser.validateSchema(sections);",
  "if (!isValid) throw new Error('MALFORMED_DOC');",
  "",
  "// Running quality checks...",
  "const quality = parser.assessQuality(rawText);",
  "console.log(`[OK] Quality score: ${quality.score}/100`);",
  "",
  "// Normalizing text encoding...",
  "const normalized = parser.normalizeText(rawText);",
  "console.log('[OK] Text normalized successfully');",
  "",
  "// Document parsed successfully",
  "return { text: rawText, sections, metadata };",
];

// Expanded hacker content for analyze phase (~120 lines)
const HACKER_LINES_ANALYZE = [
  "// boot: career_ai_engine_v4.2.0",
  "import { NeuralMatcher } from '@ai/career';",
  "import { SkillGraph } from '@ai/taxonomy';",
  "const ai = new NeuralMatcher({ gpu: true });",
  "console.log('[SYS] AI Engine initialized');",
  "",
  "// Loading skill taxonomy database...",
  "const taxonomy = await ai.loadGraph('skills_v3');",
  "console.log('[OK] 127,000 skills indexed');",
  "const embeddings = await ai.loadEmbeddings();",
  "console.log('[OK] Embeddings loaded (768-dim)');",
  "",
  "// Parsing candidate resume...",
  "console.log('[SYS] Parsing resume content...');",
  "const profile = ai.parseResume(resumeText);",
  "profile.contact = ai.extractContact(profile);",
  "profile.titles = ai.detectJobTitles(profile);",
  "console.log(`[OK] Found ${profile.titles.length} job titles`);",
  "",
  "// Extracting technical stack...",
  "const techStack = ai.extractTechStack(profile);",
  "console.log(`[OK] Detected ${techStack.length} technologies`);",
  "for (const tech of techStack) {",
  "  tech.yearsUsed = ai.estimateYears(tech, profile);",
  "  tech.proficiency = ai.scoreProficiency(tech);",
  "  tech.category = taxonomy.classify(tech.name);",
  "}",
  "",
  "// Extracting soft skills...",
  "const softSkills = ai.extractSoftSkills(profile);",
  "console.log(`[OK] Found ${softSkills.length} soft skills`);",
  "",
  "// Analyzing experience timeline...",
  "console.log('[SYS] Building career timeline...');",
  "const timeline = ai.buildTimeline(profile);",
  "const gaps = ai.detectEmploymentGaps(timeline);",
  "const avgTenure = ai.calculateAvgTenure(timeline);",
  "console.log(`[OK] Avg tenure: ${avgTenure} months`);",
  "console.log(`[OK] Total experience: ${timeline.totalYears}y`);",
  "",
  "// Analyzing career progression...",
  "const progression = ai.analyzeProgression(timeline);",
  "console.log(`[OK] Career trajectory: ${progression.trend}`);",
  "",
  "// Detecting seniority indicators...",
  "const seniority = ai.classifySeniority({",
  "  titles: profile.titles,",
  "  yearsExp: timeline.totalYears,",
  "  responsibilities: profile.responsibilities",
  "});",
  "console.log(`[OK] Seniority level: ${seniority.level}`);",
  "",
  "// Extracting education & certifications...",
  "const education = ai.extractEducation(profile);",
  "const certs = ai.extractCertifications(profile);",
  "console.log(`[OK] ${education.length} degrees found`);",
  "console.log(`[OK] ${certs.length} certifications found`);",
  "",
  "// Ingesting job descriptions...",
  "console.log('[SYS] Processing job postings...');",
  "for (const job of jobPostings) {",
  "  job.requiredSkills = ai.extractRequired(job);",
  "  job.preferredSkills = ai.extractPreferred(job);",
  "  job.roleLevel = ai.classifyRole(job);",
  "  job.industry = ai.detectIndustry(job);",
  "  console.log(`[OK] Processed: ${job.title || 'Job'}`);",
  "}",
  "",
  "// Computing semantic embeddings...",
  "console.log('[SYS] Generating embeddings...');",
  "const resumeEmbed = ai.embed(profile.summary);",
  "for (const job of jobPostings) {",
  "  job.embedding = ai.embed(job.description);",
  "}",
  "",
  "// Computing skill match scores...",
  "console.log('[SYS] Calculating match scores...');",
  "const results = [];",
  "for (const job of jobPostings) {",
  "  const match = ai.semanticMatch(profile, job);",
  "  const gaps = ai.identifyGaps(profile, job);",
  "  const fitScore = ai.calculateFit(match, gaps);",
  "  const similarity = ai.cosineSimilarity(resumeEmbed, job.embedding);",
  "  results.push({ job, match, gaps, fitScore, similarity });",
  "  console.log(`[OK] Match: ${Math.round(fitScore)}%`);",
  "}",
  "",
  "// Ranking job matches...",
  "results.sort((a, b) => b.fitScore - a.fitScore);",
  "console.log('[OK] Jobs ranked by fit score');",
  "",
  "// Calculating ATS compatibility...",
  "console.log('[SYS] Analyzing ATS compatibility...');",
  "const atsScore = ai.computeATS({",
  "  keywords: ai.extractKeywords(jobPostings),",
  "  resume: profile,",
  "  format: ai.analyzeFormatting(resumeText)",
  "});",
  "console.log(`[OK] ATS Score: ${atsScore.total}/100`);",
  "",
  "// Analyzing keyword density...",
  "const keywordAnalysis = ai.analyzeKeywords(profile, jobPostings);",
  "console.log(`[OK] Matched: ${keywordAnalysis.matched.length} keywords`);",
  "console.log(`[OK] Missing: ${keywordAnalysis.missing.length} keywords`);",
  "",
  "// Generating improvement suggestions...",
  "console.log('[SYS] Generating recommendations...');",
  "const suggestions = ai.generateSuggestions({",
  "  profile, atsScore, gaps: results[0]?.gaps",
  "});",
  "",
  "// Generating career insights...",
  "const insights = ai.generateInsights({",
  "  profile, results, atsScore, seniority",
  "});",
  "console.log('[OK] Career insights generated');",
  "",
  "// Running final validation...",
  "const validation = ai.validateResults(results);",
  "console.log('[OK] Results validated');",
  "",
  "// Compiling final report...",
  "console.log('[SYS] Compiling report...');",
  "return {",
  "  ats_result: atsScore,",
  "  job_matches: results,",
  "  insights, seniority,",
  "  suggestions",
  "};",
];

// Constants for scrolling
const VISIBLE_LINES = 12;
const LINE_HEIGHT = 20;

interface TerminalTypewriterProps {
  status: "uploading" | "analyzing";
}

export function TerminalTypewriter({ status }: TerminalTypewriterProps) {
  const [lines, setLines] = useState<string[]>([]);
  const [currentLineIndex, setCurrentLineIndex] = useState(0);
  const [currentCharIndex, setCurrentCharIndex] = useState(0);
  const [isComplete, setIsComplete] = useState(false);

  const HACKER_LINES = status === "uploading" ? HACKER_LINES_UPLOAD : HACKER_LINES_ANALYZE;

  // Calculate offset to scroll lines up (start at top)
  const offset = useMemo(() => {
    if (currentLineIndex < VISIBLE_LINES) return 0;
    return -((currentLineIndex - VISIBLE_LINES + 1) * LINE_HEIGHT);
  }, [currentLineIndex]);

  // Progress percentage
  const progress = useMemo(() => {
    return Math.min(Math.round((currentLineIndex / HACKER_LINES.length) * 100), 95);
  }, [currentLineIndex, HACKER_LINES.length]);

  // Reset when status changes
  useEffect(() => {
    setLines([]);
    setCurrentLineIndex(0);
    setCurrentCharIndex(0);
    setIsComplete(false);
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

  const getLineColor = (line: string) => {
    if (line.startsWith("//")) return "text-muted-foreground/60";
    if (line.includes("console.log")) return "text-neon-green";
    if (line.includes("const ") || line.includes("let ") || line.includes("for ") || line.includes("import ")) return "text-neon-pink";
    if (line.includes("await ") || line.includes("return ") || line.includes("throw ")) return "text-neon-yellow";
    if (line.includes("{") || line.includes("}") || line.includes("if ")) return "text-foreground";
    return "text-neon-cyan";
  };

  return (
    <div className="h-full flex flex-col relative overflow-hidden">
      {/* Terminal content - Top-aligned scrolling area */}
      <div className="flex-1 relative overflow-hidden">
        <div className="absolute inset-0 flex flex-col justify-start px-4 pt-4">
          {/* Visible lines window */}
          <div
            className="relative overflow-hidden"
            style={{ height: `${VISIBLE_LINES * LINE_HEIGHT}px` }}
          >
            <motion.div
              className="absolute w-full font-mono text-xs"
              animate={{ y: offset }}
              transition={{ duration: 0.3, ease: "easeOut" }}
            >
              {lines.map((line, i) => (
                <div
                  key={i}
                  className="flex items-center"
                  style={{ height: `${LINE_HEIGHT}px`, minHeight: `${LINE_HEIGHT}px`, maxHeight: `${LINE_HEIGHT}px` }}
                >
                  <span className="text-neon-cyan/40 w-6 text-right pr-2 select-none text-[10px] shrink-0">
                    {String(i + 1).padStart(2, "0")}
                  </span>
                  <span className={`${getLineColor(line)} truncate text-[11px] leading-tight`}>
                    {line}
                    {i === currentLineIndex && !isComplete && (
                      <motion.span
                        animate={{ opacity: [1, 0] }}
                        transition={{ duration: 0.4, repeat: Infinity }}
                        className="inline-block w-1.5 h-3 bg-neon-cyan ml-0.5 align-middle shadow-[0_0_5px_rgba(0,243,255,0.8)]"
                      />
                    )}
                  </span>
                </div>
              ))}
            </motion.div>
          </div>
        </div>
      </div>

      {/* Footer - Fixed at bottom with progress bar */}
      <AnimatePresence>
        {!isComplete && (
          <motion.div
            className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black via-black/80 to-transparent z-10"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <div className="flex items-center gap-3">
              <span className="text-[10px] text-muted-foreground uppercase tracking-wider">Processing</span>
              <div className="flex-1 h-2 bg-black/60 rounded-full overflow-hidden border border-neon-cyan/20">
                <motion.div
                  className="h-full bg-gradient-to-r from-neon-cyan via-neon-pink to-neon-cyan bg-[length:200%_100%]"
                  initial={{ width: "0%" }}
                  animate={{
                    width: `${progress}%`,
                    backgroundPosition: ["0% 0%", "100% 0%"],
                  }}
                  transition={{
                    width: { duration: 0.3 },
                    backgroundPosition: { duration: 2, repeat: Infinity, ease: "linear" }
                  }}
                />
              </div>
              <span className="text-[10px] font-mono text-neon-cyan w-10 text-right">
                {progress}%
              </span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Completion state */}
      <AnimatePresence>
        {isComplete && (
          <motion.div
            className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black via-black/80 to-transparent z-10"
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
  );
}
