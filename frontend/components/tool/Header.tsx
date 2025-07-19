"use client";

import { Button } from "@/components/ui/button";
import { Moon, Sun, Bot } from "lucide-react";
import { useTheme } from "next-themes";
import Image from "next/image";

export function Header() {
  const { theme, setTheme } = useTheme();
  const iconText = theme === "dark" ? "text-white" : "text-black";
  const iconHoverBg =
    theme === "dark" ? "hover:bg-white/20" : "hover:bg-slate-600/10";

  return (
    <header className="sticky top-0 z-50 w-full bg-secondary text-secondary-foreground shadow-lg">
      <div className="container mx-auto flex items-center justify-between px-4 py-4 gap-2">
        <div className="flex items-center gap-2 bg-white/10 backdrop-blur-sm pb-1 rounded-md flex-shrink-0">
          <Image
            src="/deloitte.png"
            alt="Business Analyst Logo"
            width={100}
            height={26}
            className={theme === "dark" ? "filter brightness-0 invert" : ""}
          />
        </div>
        <div className="text-center flex-1 min-w-0">
          <h1 className="text-xl md:text-2xl font-bold truncate">
            Business Analyst Agent
          </h1>
          <p className="text-xs md:text-sm opacity-90 truncate">
            Intelligente Dokumentenanalyse und KI-gestützte Einblicke
          </p>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          <Button
            variant="outline"
            size="icon"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className={`bg-white/10 border-0 ${iconText} ${iconHoverBg}`}
          >
            <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
            <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
            <span className="sr-only">Toggle theme</span>
          </Button>
        </div>
      </div>
    </header>
  );
}
