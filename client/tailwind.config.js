const { screens } = require('tailwindcss/defaultTheme')

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{vue,js}'],
  theme: {
    extend: {
      colors: {
        primary: '#FFFFFF',
        primaryLight: '#183A56',
        purple: '#7237E5',
        accent: '#7237E5',
        success: '#4faf64',
        warning: '#f4b942',
        error: '#d72638',
      },
      fontFamily: {
        serif: ['source-serif-pro', 'serif'],
        sans: ['Poppins', 'sans-serif'],
      },
    },
    container: {
      padding: {
        DEFAULT: '1rem',
        sm: '2rem',
        lg: '4rem',
        xl: '5rem',
        '2xl': '6rem',
      },
    },
    screens: {
      ...screens,
      '3xl': '1920px',
    },
  },
  plugins: [],
}
