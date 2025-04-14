/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html", // Scan all HTML files in app/templates
    "./app/static/src/**/*.js", // Optional: Scan JS files if you use JS to add classes
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
