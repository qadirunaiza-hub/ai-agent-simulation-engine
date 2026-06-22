<template>
  <div class="fish-scene">
    <div class="bubble" v-for="b in bubbles" :key="b.id" :style="b.style"></div>

    <svg class="fish-svg" viewBox="0 0 640 270" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <clipPath id="bc"><path :d="B"/></clipPath>

        <filter id="gl" x="-35%" y="-35%" width="170%" height="170%">
          <feGaussianBlur stdDeviation="4.5" result="b"/>
          <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
        <filter id="gs" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="2.2" result="b"/>
          <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
        <filter id="ge" x="-80%" y="-80%" width="260%" height="260%">
          <feGaussianBlur stdDeviation="5.5" result="b"/>
          <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
        <filter id="gb" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="12"/>
        </filter>

        <radialGradient id="bodyFill" cx="52%" cy="34%" r="58%">
          <stop offset="0%"   stop-color="#0A1E3A" stop-opacity="0.96"/>
          <stop offset="100%" stop-color="#020610" stop-opacity="0.99"/>
        </radialGradient>
        <radialGradient id="cyanVol" cx="55%" cy="22%" r="48%">
          <stop offset="0%"   :stop-color="cyan" stop-opacity="0.16"/>
          <stop offset="100%" :stop-color="cyan" stop-opacity="0"/>
        </radialGradient>
        <radialGradient id="pinkVol" cx="42%" cy="80%" r="44%">
          <stop offset="0%"   :stop-color="pink" stop-opacity="0.22"/>
          <stop offset="100%" :stop-color="pink" stop-opacity="0"/>
        </radialGradient>
        <linearGradient id="finC" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%"   :stop-color="cyan" stop-opacity="0.30"/>
          <stop offset="100%" :stop-color="cyan" stop-opacity="0.04"/>
        </linearGradient>
        <linearGradient id="finP" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%"   :stop-color="pink" stop-opacity="0.28"/>
          <stop offset="100%" :stop-color="pink" stop-opacity="0.04"/>
        </linearGradient>
        <linearGradient id="tailG" x1="100%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%"   :stop-color="cyan" stop-opacity="0.20"/>
          <stop offset="55%"  :stop-color="cyan" stop-opacity="0.09"/>
          <stop offset="100%" :stop-color="pink" stop-opacity="0.22"/>
        </linearGradient>
        <radialGradient id="iris" cx="38%" cy="32%" r="62%">
          <stop offset="0%"   :stop-color="pink" stop-opacity="1"/>
          <stop offset="75%"  :stop-color="pink" stop-opacity="0.85"/>
          <stop offset="100%" stop-color="#3A0018" stop-opacity="1"/>
        </radialGradient>
      </defs>

      <!-- ambient -->
      <ellipse cx="300" cy="155" rx="240" ry="120" fill="url(#pinkVol)" filter="url(#gb)"/>
      <ellipse cx="310" cy="138" rx="250" ry="110" fill="url(#cyanVol)" filter="url(#gb)"/>

      <!-- ═══ TAIL ═══ -->
      <g class="tail-group">
        <path d="M 500 132 C 520 105,545 82,575 62 C 590 74,600 105,598 132 C 596 155,598 175,598 195 C 598 218,590 246,575 258 C 545 238,520 215,500 188 Z"
          fill="url(#tailG)"/>
        <path d="M 500 132 C 520 105,545 82,575 62 C 590 74,600 105,598 132 C 596 155,598 175,598 195 C 598 218,590 246,575 258 C 545 238,520 215,500 188 Z"
          :stroke="cyan" stroke-width="1.8" fill="none" filter="url(#gl)" opacity="0.8"/>
        <g filter="url(#gs)">
          <line x1="500" y1="160" x2="598" y2="65"  :stroke="cyan" stroke-width="1.5" opacity="0.65"/>
          <line x1="500" y1="160" x2="598" y2="92"  :stroke="cyan" stroke-width="1.6" opacity="0.72"/>
          <line x1="500" y1="160" x2="598" y2="118" :stroke="cyan" stroke-width="1.8" opacity="0.82"/>
          <line x1="500" y1="160" x2="600" y2="145" :stroke="cyan" stroke-width="2.0" opacity="0.90"/>
          <line x1="500" y1="160" x2="600" y2="162" :stroke="cyan" stroke-width="2.2" opacity="1.00"/>
          <line x1="500" y1="160" x2="600" y2="180" :stroke="cyan" stroke-width="2.0" opacity="0.90"/>
          <line x1="500" y1="160" x2="598" y2="205" :stroke="cyan" stroke-width="1.8" opacity="0.82"/>
          <line x1="500" y1="160" x2="596" y2="228" :stroke="pink" stroke-width="1.6" opacity="0.72"/>
          <line x1="500" y1="160" x2="576" y2="256" :stroke="pink" stroke-width="1.4" opacity="0.60"/>
        </g>
        <line x1="500" y1="160" x2="600" y2="162" stroke="white" stroke-width="1.0" opacity="0.50"/>
        <line x1="500" y1="160" x2="598" y2="145" stroke="white" stroke-width="0.7" opacity="0.35"/>
        <line x1="500" y1="160" x2="598" y2="180" stroke="white" stroke-width="0.7" opacity="0.35"/>
      </g>

      <!-- ═══ BODY FILL ═══ -->
      <path :d="B" fill="url(#bodyFill)"/>
      <path :d="B" fill="url(#cyanVol)"/>
      <path :d="B" fill="url(#pinkVol)"/>
      <!-- specular white on spine -->
      <path d="M 492 130 C 486 70,368 22,268 22 C 188 22,132 55,105 112"
        stroke="white" stroke-width="1.5" fill="none" opacity="0.14"/>

      <!-- ═══ SCALES (clipped arcs) ═══ -->
      <g clip-path="url(#bc)" filter="url(#gs)">
        <!-- cyan arcs, upper rows -->
        <path d="M 148 52 Q 166 38 184 52"  :stroke="cyan" stroke-width="1.3" fill="none" opacity="0.52"/>
        <path d="M 175 48 Q 193 34 211 48"  :stroke="cyan" stroke-width="1.3" fill="none" opacity="0.52"/>
        <path d="M 203 46 Q 221 32 239 46"  :stroke="cyan" stroke-width="1.3" fill="none" opacity="0.52"/>
        <path d="M 232 46 Q 250 32 268 46"  :stroke="cyan" stroke-width="1.3" fill="none" opacity="0.52"/>
        <path d="M 260 47 Q 278 33 296 47"  :stroke="cyan" stroke-width="1.3" fill="none" opacity="0.50"/>
        <path d="M 288 50 Q 306 36 324 50"  :stroke="cyan" stroke-width="1.2" fill="none" opacity="0.48"/>
        <path d="M 315 54 Q 333 40 351 54"  :stroke="cyan" stroke-width="1.2" fill="none" opacity="0.46"/>
        <path d="M 341 60 Q 359 46 377 60"  :stroke="cyan" stroke-width="1.1" fill="none" opacity="0.43"/>
        <path d="M 365 68 Q 383 54 401 68"  :stroke="cyan" stroke-width="1.1" fill="none" opacity="0.40"/>
        <path d="M 388 78 Q 406 64 424 78"  :stroke="cyan" stroke-width="1.0" fill="none" opacity="0.37"/>

        <path d="M 128 80 Q 146 66 164 80"  :stroke="cyan" stroke-width="1.2" fill="none" opacity="0.48"/>
        <path d="M 158 74 Q 176 60 194 74"  :stroke="cyan" stroke-width="1.2" fill="none" opacity="0.48"/>
        <path d="M 188 70 Q 206 56 224 70"  :stroke="cyan" stroke-width="1.2" fill="none" opacity="0.48"/>
        <path d="M 218 68 Q 236 54 254 68"  :stroke="cyan" stroke-width="1.2" fill="none" opacity="0.48"/>
        <path d="M 248 68 Q 266 54 284 68"  :stroke="cyan" stroke-width="1.2" fill="none" opacity="0.46"/>
        <path d="M 276 70 Q 294 56 312 70"  :stroke="cyan" stroke-width="1.1" fill="none" opacity="0.44"/>
        <path d="M 303 74 Q 321 60 339 74"  :stroke="cyan" stroke-width="1.1" fill="none" opacity="0.42"/>
        <path d="M 329 80 Q 347 66 365 80"  :stroke="cyan" stroke-width="1.0" fill="none" opacity="0.39"/>
        <path d="M 353 88 Q 371 74 389 88"  :stroke="cyan" stroke-width="1.0" fill="none" opacity="0.36"/>
        <path d="M 376 98 Q 394 84 412 98"  :stroke="cyan" stroke-width="0.9" fill="none" opacity="0.33"/>

        <!-- pink arcs, belly rows -->
        <path d="M 120 188 Q 138 204 156 188" :stroke="pink" stroke-width="1.2" fill="none" opacity="0.48"/>
        <path d="M 150 200 Q 168 216 186 200" :stroke="pink" stroke-width="1.2" fill="none" opacity="0.48"/>
        <path d="M 180 210 Q 198 226 216 210" :stroke="pink" stroke-width="1.2" fill="none" opacity="0.48"/>
        <path d="M 210 216 Q 228 232 246 216" :stroke="pink" stroke-width="1.2" fill="none" opacity="0.48"/>
        <path d="M 240 220 Q 258 236 276 220" :stroke="pink" stroke-width="1.2" fill="none" opacity="0.46"/>
        <path d="M 268 222 Q 286 238 304 222" :stroke="pink" stroke-width="1.1" fill="none" opacity="0.44"/>
        <path d="M 296 220 Q 314 236 332 220" :stroke="pink" stroke-width="1.1" fill="none" opacity="0.42"/>
        <path d="M 322 216 Q 340 232 358 216" :stroke="pink" stroke-width="1.0" fill="none" opacity="0.39"/>
        <path d="M 346 210 Q 364 226 382 210" :stroke="pink" stroke-width="1.0" fill="none" opacity="0.36"/>
        <path d="M 369 200 Q 387 216 405 200" :stroke="pink" stroke-width="0.9" fill="none" opacity="0.33"/>
      </g>

      <!-- ═══ DORSAL FIN ═══ -->
      <path d="M 145 26 Q 185 -28 240 -34 Q 298 -28 348 -4 Q 388 15 415 42 L 408 58 Q 372 34 336 16 Q 295 0 248 -6 Q 200 -6 162 42 Z"
        fill="url(#finC)"/>
      <path d="M 145 26 Q 185 -28 240 -34 Q 298 -28 348 -4 Q 388 15 415 42 L 408 58 Q 372 34 336 16 Q 295 0 248 -6 Q 200 -6 162 42 Z"
        :stroke="cyan" stroke-width="1.8" fill="none" filter="url(#gl)" opacity="0.82"/>
      <g filter="url(#gs)">
        <line x1="165" y1="40" x2="178" y2="-2"  :stroke="cyan" stroke-width="1.3" opacity="0.72"/>
        <line x1="184" y1="32" x2="197" y2="-14" :stroke="cyan" stroke-width="1.4" opacity="0.78"/>
        <line x1="205" y1="26" x2="218" y2="-24" :stroke="cyan" stroke-width="1.5" opacity="0.84"/>
        <line x1="226" y1="22" x2="238" y2="-30" :stroke="cyan" stroke-width="1.6" opacity="0.90"/>
        <line x1="248" y1="20" x2="258" y2="-32" :stroke="cyan" stroke-width="1.6" opacity="0.90"/>
        <line x1="269" y1="21" x2="278" y2="-28" :stroke="cyan" stroke-width="1.5" opacity="0.84"/>
        <line x1="290" y1="24" x2="298" y2="-20" :stroke="cyan" stroke-width="1.4" opacity="0.78"/>
        <line x1="310" y1="28" x2="320" y2="-10" :stroke="cyan" stroke-width="1.3" opacity="0.72"/>
        <line x1="330" y1="35" x2="340" y2="0"   :stroke="cyan" stroke-width="1.2" opacity="0.65"/>
        <line x1="350" y1="43" x2="360" y2="12"  :stroke="cyan" stroke-width="1.2" opacity="0.60"/>
        <line x1="368" y1="52" x2="378" y2="24"  :stroke="cyan" stroke-width="1.1" opacity="0.55"/>
        <line x1="385" y1="62" x2="394" y2="38"  :stroke="cyan" stroke-width="1.0" opacity="0.50"/>
      </g>
      <line x1="226" y1="22" x2="238" y2="-30" stroke="white" stroke-width="0.8" opacity="0.42"/>
      <line x1="248" y1="20" x2="258" y2="-32" stroke="white" stroke-width="0.8" opacity="0.42"/>

      <!-- ═══ PECTORAL FINS ═══ -->
      <path d="M 228 152 Q 255 132 288 128 Q 315 128 330 146 Q 312 155 285 158 Q 258 160 228 152 Z"
        fill="url(#finC)"/>
      <path d="M 228 152 Q 255 132 288 128 Q 315 128 330 146 Q 312 155 285 158 Q 258 160 228 152 Z"
        :stroke="cyan" stroke-width="1.4" fill="none" filter="url(#gs)" opacity="0.78"/>
      <g filter="url(#gs)" opacity="0.62">
        <line x1="228" y1="152" x2="290" y2="128" :stroke="cyan" stroke-width="0.9"/>
        <line x1="240" y1="150" x2="316" y2="132" :stroke="cyan" stroke-width="0.9"/>
        <line x1="256" y1="148" x2="330" y2="146" :stroke="cyan" stroke-width="0.9"/>
      </g>

      <path d="M 210 212 Q 236 232 264 240 Q 285 244 298 232 Q 280 218 255 207 Q 232 198 210 212 Z"
        fill="url(#finP)"/>
      <path d="M 210 212 Q 236 232 264 240 Q 285 244 298 232 Q 280 218 255 207 Q 232 198 210 212 Z"
        :stroke="pink" stroke-width="1.4" fill="none" filter="url(#gs)" opacity="0.78"/>
      <g filter="url(#gs)" opacity="0.58">
        <line x1="210" y1="212" x2="298" y2="232" :stroke="pink" stroke-width="0.9"/>
        <line x1="222" y1="220" x2="296" y2="234" :stroke="pink" stroke-width="0.9"/>
        <line x1="238" y1="230" x2="292" y2="236" :stroke="pink" stroke-width="0.8"/>
      </g>

      <!-- ═══ VENTRAL FINS ═══ -->
      <path d="M 185 252 Q 202 274 232 280 Q 255 282 265 268 Q 248 254 222 244 Q 200 238 185 252 Z"
        fill="url(#finP)"/>
      <path d="M 185 252 Q 202 274 232 280 Q 255 282 265 268 Q 248 254 222 244 Q 200 238 185 252 Z"
        :stroke="pink" stroke-width="1.5" fill="none" filter="url(#gs)" opacity="0.8"/>
      <g filter="url(#gs)" opacity="0.58">
        <line x1="185" y1="252" x2="265" y2="268" :stroke="pink" stroke-width="0.9"/>
        <line x1="196" y1="260" x2="262" y2="270" :stroke="pink" stroke-width="0.8"/>
        <line x1="210" y1="268" x2="258" y2="272" :stroke="pink" stroke-width="0.8"/>
      </g>
      <path d="M 298 244 Q 316 262 338 266 Q 356 266 362 254 Q 348 242 326 236 Q 308 232 298 244 Z"
        fill="url(#finP)"/>
      <path d="M 298 244 Q 316 262 338 266 Q 356 266 362 254 Q 348 242 326 236 Q 308 232 298 244 Z"
        :stroke="pink" stroke-width="1.3" fill="none" filter="url(#gs)" opacity="0.72"/>

      <!-- ═══ BODY OUTLINE (top layer) ═══ -->
      <path :d="B" :stroke="cyan" stroke-width="6"   fill="none" filter="url(#gb)" opacity="0.28"/>
      <path :d="B" :stroke="cyan" stroke-width="2.2" fill="none" filter="url(#gl)" opacity="0.88"/>
      <path :d="B" stroke="white" stroke-width="0.9" fill="none" opacity="0.15"/>
      <!-- Pink belly outline -->
      <path d="M 82 200 C 100 234,148 262,222 272 C 300 282,496 258,500 192"
        :stroke="pink" stroke-width="2" fill="none" filter="url(#gs)" opacity="0.62"/>

      <!-- ═══ GILL ═══ -->
      <path d="M 308 28 Q 334 82 334 160 Q 330 220 308 260"
        :stroke="cyan" stroke-width="1.8" fill="none" filter="url(#gs)" opacity="0.65"/>
      <path d="M 308 28 Q 334 82 334 160 Q 330 220 308 260"
        stroke="white" stroke-width="0.7" fill="none" opacity="0.22"/>

      <!-- ═══ EYE ═══ -->
      <g filter="url(#ge)">
        <circle cx="112" cy="155" r="30" :stroke="pink" stroke-width="1.5" fill="none" opacity="0.35"/>
        <circle cx="112" cy="155" r="23" :stroke="cyan" stroke-width="2.5" fill="none"/>
        <circle cx="112" cy="155" r="19" fill="url(#iris)"/>
        <circle cx="112" cy="155" r="10" fill="#030510" opacity="0.95"/>
        <circle cx="119" cy="147" r="5.5" fill="white" opacity="0.82"/>
        <circle cx="124" cy="143" r="2"   fill="white" opacity="0.55"/>
      </g>

      <!-- ═══ MOUTH ═══ -->
      <path d="M 68 148 Q 54 160 68 174"
        :stroke="cyan" stroke-width="2.5" fill="none" stroke-linecap="round"
        filter="url(#gs)" opacity="0.9"/>
      <path d="M 68 148 Q 54 160 68 174"
        stroke="white" stroke-width="0.8" fill="none" stroke-linecap="round" opacity="0.40"/>
      <circle cx="78" cy="140" r="2.5" :fill="cyan" opacity="0.60"/>
    </svg>

    <div class="scan-lines"></div>
  </div>
</template>

<script setup>
const cyan = '#00CFFF'
const pink = '#f97316'

// Elongated fish body — roughly 2:1 width:height ratio
const B = 'M 498 130 C 493 50,368 12,265 12 C 182 12,118 48,90 110 C 74 134,74 170,86 192 C 108 228,162 258,265 268 C 368 278,500 248,502 196 Z'

const bubbles = Array.from({ length: 8 }, (_, i) => ({
  id: i,
  style: {
    left: `${8 + i * 11}%`,
    animationDelay: `${i * 0.65}s`,
    animationDuration: `${2.2 + i * 0.32}s`,
    width:  `${3 + (i % 3) * 2}px`,
    height: `${3 + (i % 3) * 2}px`,
  },
}))
</script>

<style scoped>
.fish-scene {
  position: relative;
  width: 100%;
  max-width: 520px;
  height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: visible;
}

.fish-svg {
  width: 100%;
  max-width: 520px;
  overflow: visible;
  animation: swim 4s ease-in-out infinite;
  filter:
    drop-shadow(0 0 6px  #00CFFF)
    drop-shadow(0 0 18px rgba(0,207,255,0.5))
    drop-shadow(0 0 40px rgba(249,115,22,0.3))
    drop-shadow(0 0 70px rgba(0,207,255,0.12));
}

@keyframes swim {
  0%   { transform: translateY(0px)   rotate(0deg); }
  25%  { transform: translateY(-12px) rotate(-1.1deg); }
  50%  { transform: translateY(0px)   rotate(0deg); }
  75%  { transform: translateY(12px)  rotate(1.1deg); }
  100% { transform: translateY(0px)   rotate(0deg); }
}

.bubble {
  position: absolute;
  bottom: 14%;
  border-radius: 50%;
  border: 1.5px solid #00CFFF;
  opacity: 0;
  animation: rise linear infinite;
  box-shadow: 0 0 6px #00CFFF;
}

@keyframes rise {
  0%   { opacity: 0;   transform: translateY(0)       scale(1);   }
  10%  { opacity: 0.7; }
  88%  { opacity: 0.2; }
  100% { opacity: 0;   transform: translateY(-200px)  scale(1.5); }
}

.scan-lines {
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    0deg, transparent 0px, transparent 3px,
    rgba(0,207,255,0.015) 3px, rgba(0,207,255,0.015) 4px
  );
  pointer-events: none;
}
</style>
