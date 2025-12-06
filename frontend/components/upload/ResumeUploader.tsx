"use client";

import { useState } from "react";
import { Upload, FileText, Check, Loader2, ScanLine, X } from "lucide-react";
import { cn } from "@/lib/utils";

export function ResumeUploader() {
    const [isDragActive, setIsDragActive] = useState(false);
    const [file, setFile] = useState<File | null>(null);
    const [status, setStatus] = useState<"idle" | "uploading" | "done">("idle");

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragActive(false);
        if (e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    };

    const handleFile = (f: File) => {
        setFile(f);
        setStatus("uploading");
        setTimeout(() => setStatus("done"), 1500);
    };

    const clearFile = (e: React.MouseEvent) => {
        e.stopPropagation();
        setFile(null);
        setStatus("idle");
    };

    return (
        <div className="font-sans h-full">
            <div
                className={cn(
                    "relative h-full min-h-[120px] border-2 border-dashed transition-all duration-300 rounded-lg flex flex-col items-center justify-center p-6 cursor-pointer group overflow-hidden",
                    isDragActive
                        ? "border-neon-pink bg-neon-pink/10 shadow-[inset_0_0_30px_rgba(188,19,254,0.3)]"
                        : "border-white/10 hover:border-neon-pink/50 hover:bg-white/5",
                    file ? "border-solid border-neon-pink bg-neon-pink/5" : ""
                )}
                onDragOver={(e) => { e.preventDefault(); setIsDragActive(true); }}
                onDragLeave={() => setIsDragActive(false)}
                onDrop={handleDrop}
                onClick={() => document.getElementById('resume-upload-input')?.click()}
            >
                <input
                    id="resume-upload-input"
                    type="file"
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
                                className="p-1.5 hover:bg-red-500/20 rounded-full text-muted-foreground hover:text-red-500 transition-colors"
                            >
                                <X className="h-4 w-4" />
                            </button>
                        </div>

                        {/* Status Bar */}
                        <div className="space-y-1">
                            <div className="h-1 w-full bg-gray-800 rounded-full overflow-hidden">
                                <div
                                    className={cn("h-full bg-neon-pink transition-all duration-1000 ease-out", status === 'done' ? "w-full" : "w-[60%] animate-pulse")}
                                />
                            </div>
                            <div className="flex justify-between text-[10px] font-mono text-neon-pink/80 uppercase">
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
