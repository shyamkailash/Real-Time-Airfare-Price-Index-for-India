module.exports = {
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        // Light enterprise theme
        'body-bg': '#F4F7FB',
        'content-bg': '#FFFFFF',
        'sidebar-dark': '#071A35',
        'sidebar-secondary': '#0B2345',
        'primary-blue': '#1557B0',
        'bright-blue': '#1769E0',
        'airtn-teal': '#00BFA6',
        'success-green': '#16A34A',
        'warning-amber': '#F59E0B',
        'error-red': '#DC2626',
        'primary-text': '#172033',
        'secondary-text': '#64748B',
        'muted-text': '#94A3B8',
        'border-light': '#E2E8F0',
        'card-bg': '#FFFFFF',
        'chart-grid': '#E8EEF5',
        
        // Legacy colors (for compatibility)
        graphite: '#0B1220',
        slatebg: '#111827',
        surface: '#172033',
        teal: '#14B8A6',
        cyan: '#22D3EE',
        amber: '#F59E0B',
        emerald: '#22C55E',
        rose: '#F43F5E',
        ptext: '#F8FAFC',
        stext: '#94A3B8',
        borders: '#263449'
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        }
      },
      animation: {
        fadeIn: 'fadeIn 0.2s ease-in-out'
      }
    }
  },
  plugins: []
}
