import { createContext, useContext, useEffect, useCallback, type ReactNode } from "react";

export type ThemeMode = "light" | "dark" | "system";
export type ResolvedTheme = "light" | "dark";

const DEFAULT_THEME: ThemeMode = "light";

interface ThemeContextValue {
  /** User selected preference: light / dark / system */
  themeMode: ThemeMode;
  /** Resolved final theme after applying system preference */
  isDark: boolean;
  setThemeMode: (mode: ThemeMode) => void;
  /** Convenience toggle: light ↔ dark (skips system) */
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextValue>({
  themeMode: "light",
  isDark: false,
  setThemeMode: () => {},
  toggleTheme: () => {},
});

function resolveIsDark(mode: ThemeMode): boolean {
  if (mode === "dark") return true;
  if (mode === "light") return false;
  // system
  return window.matchMedia?.("(prefers-color-scheme: dark)").matches ?? false;
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const themeMode: ThemeMode = DEFAULT_THEME;
  const isDark = resolveIsDark(themeMode);

  // Apply dark/light class to <html> element for global CSS variable overrides
  useEffect(() => {
    const html = document.documentElement;
    if (isDark) {
      html.classList.add("dark-mode");
    } else {
      html.classList.remove("dark-mode");
    }
  }, [isDark]);

  const setThemeMode = useCallback((_mode: ThemeMode) => {
    // Theme is locked to light; ignore attempts to change.
  }, []);

  const toggleTheme = useCallback(() => {
    // Theme is locked to light; ignore.
  }, []);

  return (
    <ThemeContext.Provider
      value={{ themeMode, isDark, setThemeMode, toggleTheme }}
    >
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme(): ThemeContextValue {
  return useContext(ThemeContext);
}
