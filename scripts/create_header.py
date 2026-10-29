import pathlib

def create_header():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 180" width="880" height="180" fill="none">
  <defs>
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#080c14"/>
      <stop offset="50%" stop-color="#0d1527"/>
      <stop offset="100%" stop-color="#080c14"/>
    </linearGradient>
    <linearGradient id="blue-accent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#60a5fa"/>
    </linearGradient>
    <linearGradient id="border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.4"/>
      <stop offset="40%" stop-color="#1e293b" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#60a5fa" stop-opacity="0.25"/>
    </linearGradient>
  </defs>

  <style>
    .mono { font-family: 'JetBrains Mono', 'Fira Code', Menlo, Consolas, monospace; }
    .sans { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; }
    .pulse { animation: pulse-dot 2s infinite ease-in-out; }
    @keyframes pulse-dot { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
  </style>

  <!-- Card Frame -->
  <rect x="1" y="1" width="878" height="178" rx="16" fill="url(#bg-grad)" stroke="url(#border-grad)" stroke-width="1.5"/>

  <!-- Subtle Ambient Grid -->
  <g opacity="0.05" stroke="#38bdf8" stroke-width="0.75">
    <line x1="0" y1="45" x2="880" y2="45" />
    <line x1="0" y1="90" x2="880" y2="90" />
    <line x1="0" y1="135" x2="880" y2="135" />
    <line x1="220" y1="0" x2="220" y2="180" />
    <line x1="440" y1="0" x2="440" y2="180" />
    <line x1="660" y1="0" x2="660" y2="180" />
  </g>

  <!-- Window controls -->
  <circle cx="36" cy="28" r="5" fill="#ff5f56" opacity="0.8"/>
  <circle cx="52" cy="28" r="5" fill="#ffbd2e" opacity="0.8"/>
  <circle cx="68" cy="28" r="5" fill="#27c93f" opacity="0.8"/>

  <!-- Live telemetry badge top right -->
  <g transform="translate(710, 20)">
    <rect width="134" height="24" rx="12" fill="#38bdf8" fill-opacity="0.08" stroke="#38bdf8" stroke-opacity="0.25" stroke-width="1"/>
    <circle cx="16" cy="12" r="3.5" fill="#38bdf8" class="pulse"/>
    <text x="28" y="16" class="mono" font-size="11" font-weight="600" fill="#38bdf8" letter-spacing="1">SYSTEM: ACTIVE</text>
  </g>

  <!-- Content -->
  <g transform="translate(36, 75)">
    <!-- Title -->
    <text x="0" y="16" class="sans" font-size="34" font-weight="800" fill="#f8fafc" letter-spacing="-0.5">Ahmed Elshaarawy</text>
    
    <!-- Role Subtitle -->
    <text x="0" y="47" class="sans" font-size="16" font-weight="600" fill="url(#blue-accent)" letter-spacing="0.2">Full-Stack &amp; Applied AI Engineer</text>
    
    <!-- Terminal Command Line -->
    <text x="0" y="75" class="mono" font-size="12.5" fill="#94a3b8">
      <tspan fill="#38bdf8">&gt;</tspan> Shipping production mobile &amp; web apps · Integrating LLMs &amp; intelligent systems
    </text>
  </g>
</svg>'''
    out = pathlib.Path("assets/header.svg")
    out.write_text(svg, encoding="utf-8")
    print(f"Wrote {out}")

if __name__ == "__main__":
    create_header()
