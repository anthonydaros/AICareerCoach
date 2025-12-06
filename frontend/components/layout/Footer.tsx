import Link from "next/link";

export function Footer() {
    return (
        <footer className="w-full border-t border-white/5 py-6 md:py-0">
            <div className="container flex flex-col items-center justify-between gap-4 md:h-24 md:flex-row">
                <p className="text-center text-sm leading-loose text-muted-foreground md:text-left">
                    Built by{" "}
                    <Link
                        href="#"
                        target="_blank"
                        rel="noreferrer"
                        className="font-medium underline underline-offset-4"
                    >
                        Anthony Max
                    </Link>
                    . The source code is available on{" "}
                    <Link
                        href="https://github.com/anthonymax"
                        target="_blank"
                        rel="noreferrer"
                        className="font-medium underline underline-offset-4"
                    >
                        GitHub
                    </Link>
                    .
                </p>
            </div>
        </footer>
    );
}
