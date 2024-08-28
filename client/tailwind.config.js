/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html', './src/**/*.{vue,js}'],
  theme: {
    extend: {
      colors: {
        primary: '#FFFFFF',
        primaryLight: '#183A56',
        purple: '#7237E5',
        accent: '#d93a00',
        success: '#4faf64',
        warning: '#f4b942',
        error: '#d72638',
      },
      fontFamily: {
        avenir: ['Avenir', 'Helvetica', 'Arial', 'sans-serif'],
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
  },
  plugins: [],
}
