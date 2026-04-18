/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: "#6366f1",
          dark: "#4f46e5",
          light: "#a5b4fc",
        },
        section: {
          ui: "#3b82f6",
          backend: "#22c55e",
          utils: "#94a3b8",
          config: "#eab308",
          tests: "#a855f7",
          external: "#f97316",
        },
      },
    },
  },
  plugins: [],
}
