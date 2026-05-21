/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: "#1F3864",
          light: "#2E5090",
          dark: "#13234A",
        },
      },
    },
  },
  plugins: [],
};
