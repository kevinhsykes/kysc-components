// kysc-components Tailwind preset
// Consumers extend their tailwind.config.js via `presets: [require('kysc_components/tailwind/preset.js')]`.
// Override any token in the consumer config — Tailwind merges presets shallowly per key.

module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          bg: '#ffffff',
          fg: '#0f172a',
          muted: '#e2e8f0',
          accent: '#2563eb',
        },
      },
      spacing: {
        'kysc-gutter': '1.5rem',
        'kysc-section': '6rem',
      },
      maxWidth: {
        'kysc-content': '72rem',
      },
    },
  },
};
