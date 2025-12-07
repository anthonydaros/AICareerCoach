"use client";

import { useState } from "react";
import { Upload, FileText, Check, Loader2, ScanLine, X } from "lucide-react";
import { cn } from "@/lib/utils";

interface ResumeUploaderProps {
    onUpload?: (file: File) => Promise<void>;
    onClear?: () => void;
    isUploading?: boolean;
    uploadedFilename?: string | null;
    error?: string | null;
}

export function ResumeUploader({
    onUpload,
    onClear,
    isUploading = false,
    uploadedFilename,
    error,
}: ResumeUploaderProps) {
    const [isDragActive, setIsDragActive] = useState(false);
    const [file, setFile] = useState<File | null>(null);

    const status = isUploading ? "uploading" : uploadedFilename ? "done" : "idle";

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragActive(false);
        if (e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    };

    const handleFile = async (f: File) => {
        setFile(f);
        if (onUpload) {
            await onUpload(f);
        }
    };

    const clearFile = (e: React.MouseEvent) => {
        e.stopPropagation();
        setFile(null);
        if (onClear) {
            onClear();
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            document.getElementById('resume-upload-input')?.click();
        }
    };

    return (
        <div className="font-sans h-full">
            {/* Hidden instructions for screen readers */}
            <p id="resume-upload-instructions" className="sr-only">
                Upload your resume in PDF, DOCX, or TXT format. You can drag and drop a file or click to browse.
            </p>

            <div
                role="button"
                tabIndex={0}
                aria-label={file ? `Resume uploaded: ${file.name}` : "Upload resume"}
                aria-describedby="resume-upload-instructions"
                aria-busy={isUploading}
                className={cn(
                    "relative h-full min-h-[120px] border-2 border-dashed transition-all duration-300 rounded-lg flex flex-col items-center justify-center p-6 cursor-pointer group overflow-hidden",
                    "focus:outline-none focus:ring-2 focus:ring-neon-pink focus:ring-offset-2 focus:ring-offset-background",
                    isDragActive
                        ? "border-neon-pink bg-neon-pink/10 shadow-[inset_0_0_30px_rgba(188,19,254,0.3)]"
                        : "border-white/10 hover:border-neon-pink/50 hover:bg-white/5",
                    file ? "border-solid border-neon-pink bg-neon-pink/5" : ""
                )}
                onDragOver={(e) => { e.preventDefault(); setIsDragActive(true); }}
                onDragLeave={() => setIsDragActive(false)}
                onDrop={handleDrop}
                onClick={() => document.getElementById('resume-upload-input')?.click()}
                onKeyDown={handleKeyDown}
            >
                <input
                    id="resume-upload-input"
                    type="file"
                    accept=".pdf,.docx,.doc,.txt"
                    aria-label="Choose resume file"
                    className="hidden"
                    onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
                />

                {/* Animated Corners */}
                {!file && (
                    <>
                        <div className="absolute top-0 left-0 w-3 h-3 border-t-2 border-l-2 border-neon-pink/30 group-hover:border-neon-pink transition-colors" />
                        <div className="absolute top-0 right-0 w-3 h-3 border-t-2 border-r-2 border-neon-pink/30 group-hover:border-neon-pink transition-colors" />
                        <div className="absolute bottom-0 left-0 w-3 h-3 border-b-2 border-l-2 border-neon-pink/30 group-hover:border-neon-pink transition-colors" />
                        <div className="absolute bottom-0 right-0 w-3 h-3 border-b-2 border-r-2 border-neon-pink/30 group-hover:border-neon-pink transition-colors" />
                    </>
                )}

                {!file ? (
                    <div className="text-center space-y-3 pointer-events-none z-10">
                        <div className="w-16 h-16 rounded-full bg-black/50 border border-neon-pink/30 flex items-center justify-center mx-auto mb-2 group-hover:scale-110 group-hover:border-neon-pink transition-all shadow-[0_0_15px_rgba(188,19,254,0.1)]">
                            <Upload className="h-8 w-8 text-neon-pink opacity-70 group-hover:opacity-100" />
                        </div>
                        <div>
                            <p className="text-neon-pink font-bold font-display tracking-widest uppercase text-sm">DROP DATA CORE</p>
                            <p className="text-[10px] text-muted-foreground font-mono mt-1">OR CLICK TO UPLOAD</p>
                        </div>
                    </div>
                ) : (
                    <div className="w-full space-y-4 relative z-10">
                        <div className="flex items-center justify-between bg-black/40 p-3 rounded border border-neon-pink/30">
                            <div className="flex items-center gap-3">
                                <FileText className="h-6 w-6 text-neon-pink" />
                                <div className="text-left">
                                    <p className="text-sm font-bold text-white truncate max-w-[200px]">{file.name}</p>
                                    <p className="text-[10px] text-neon-pink font-mono uppercase">{(file.size / 1024).toFixed(1)} KB // ENCRYPTED</p>
                                </div>
                            </div>
                            <button
                                onClick={clearFile}
                                aria-label="Remove uploaded resume"
                                className="p-1.5 hover:bg-red-500/20 rounded-full text-muted-foreground hover:text-red-500 transition-colors focus:outline-none focus:ring-2 focus:ring-red-500"
                            >
                                <X className="h-4 w-4" aria-hidden="true" />
                            </button>
                        </div>

                        {/* Status Bar */}
                        <div className="space-y-1" role="progressbar" aria-valuenow={status === 'done' ? 100 : 60} aria-valuemin={0} aria-valuemax={100} aria-label="Upload progress">
                            <div className="h-1 w-full bg-gray-800 rounded-full overflow-hidden">
                                <div
                                    className={cn("h-full bg-neon-pink transition-all duration-1000 ease-out", status === 'done' ? "w-full" : "w-[60%] animate-pulse")}
                                />
                            </div>
                            <div className="flex justify-between text-[10px] font-mono text-neon-pink/80 uppercase" aria-live="polite">
                                <span>{status === 'done' ? 'UPLOAD COMPLETE' : 'UPLOADING...'}</span>
                                <span>{status === 'done' ? '100%' : '60%'}</span>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
