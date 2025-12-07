import type { Metadata } from "next";
import { Orbitron, Rajdhani } from "next/font/google";
import { ResultsProvider } from "@/contexts/ResultsContext";
import "./globals.css";

const orbitron = Orbitron({
  variable: "--font-orbitron",
  subsets: ["latin"],
});

const rajdhani = Rajdhani({
  weight: ["300", "400", "500", "600", "700"],
  variable: "--font-rajdhani",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AI Career Coach | Future of Work",
  description: "Advanced AI-powered career coaching and ATS optimization.",
  robots: {
    index: false,
    follow: false,
  },
  icons: {
    icon: '/favicon.ico',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${orbitron.variable} ${rajdhani.variable} font-sans antialiased bg-background text-foreground selection:bg-neon-cyan selection:text-black`}
      >
        {/* Skip Link for Accessibility */}
        <a
          href="#main-content"
          className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-[100] focus:px-4 focus:py-2 focus:bg-neon-cyan focus:text-black focus:rounded focus:font-bold focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-neon-pink"
        >
          Skip to main content
        </a>
        <ResultsProvider>{children}</ResultsProvider>
      </body>
    </html>
  );
}
