/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        display: ['Sora', 'sans-serif'],
        body: ['IBM Plex Sans', 'sans-serif'],
      },
      colors: {
        surface: '#0B1226',
        card: '#0F1B3D',
        accent: '#F97316',
        mint: '#10B981',
        amber: '#F59E0B',
        rose: '#EF4444',
      },
      boxShadow: {
        glow: '0 0 0 1px rgba(255,255,255,0.06), 0 22px 40px rgba(2,6,23,0.45)',
      },
      keyframes: {
        fadeUp: {
          '0%': { opacity: 0, transform: 'translateY(18px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' },
        },
      },
      animation: {
        fadeUp: 'fadeUp 600ms ease forwards',
      },
    },
  },
  plugins: [],
};
