import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Phone-style Calculator", page_icon="🧮", layout="centered")
st.title("Phone-style Calculator — Click or Type")

# The HTML/CSS/JS calculator is fully self-contained and embedded as a Streamlit component.
html_code = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    :root{
      --bg-start:#2b2b2b;
      --bg-end:#000;
      --calc-bg-top:#1e1e1e;
      --calc-bg-bottom:#0f0f0f;
      --glass: rgba(255,255,255,0.04);
      --accent:#ff9500;
      --accent-dark:#e08600;
      --equal:#34c759;
      --gray:#bdbdbd;
      --btn-dark: linear-gradient(180deg,#2b2b2b,#1a1a1a);
      --transition:all .14s cubic-bezier(.2,.8,.2,1);
    }
    html,body {
      height:100%;
      margin:0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial;
      background: radial-gradient(circle at top left, var(--bg-start), var(--bg-end));
      -webkit-font-smoothing:antialiased;
      -moz-osx-font-smoothing:grayscale;
      display:flex;
      align-items:center;
      justify-content:center;
      padding:20px;
      box-sizing:border-box;
    }
    .container{
      width:360px;
      max-width:95vw;
      border-radius:36px;
      padding:22px;
      background: linear-gradient(180deg, var(--calc-bg-top), var(--calc-bg-bottom));
      box-shadow: 0 20px 60px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.03);
      border:1px solid rgba(255,255,255,0.04);
      animation:pop .45s ease;
    }
    @keyframes pop {
      from { transform: scale(.96); opacity:0 }
      to   { transform: scale(1); opacity:1 }
    }
    .display {
      height:86px;
      background:linear-gradient(180deg, rgba(0,0,0,0.95), rgba(0,0,0,0.86));
      border-radius:14px;
      padding:12px 18px;
      color:#fff;
      text-align:right;
      font-size:42px;
      line-height:1;
      box-shadow: inset 0 -6px 18px rgba(255,255,255,0.02);
      display:flex;
      align-items:center;
      justify-content:flex-end;
      overflow:hidden;
      white-space:nowrap;
    }
    .small {
      font-size:14px;
      color:rgba(255,255,255,0.45);
      position:absolute;
      left:18px;
      top:10px;
    }
    .grid {
      margin-top:16px;
      display:grid;
      grid-template-columns: repeat(4,1fr);
      grid-gap:12px;
    }
    button.calc {
      height:72px;
      border-radius:36px;
      font-size:22px;
      font-weight:600;
      border:0;
      cursor:pointer;
      transition: var(--transition);
      box-shadow: 0 6px 14px rgba(0,0,0,0.5), inset 0 2px 4px rgba(255,255,255,0.02);
      user-select:none;
      -webkit-tap-highlight-color: transparent;
    }
    /* default dark button */
    button.calc.btn-dark {
      background: var(--btn-dark);
      color:white;
    }
    /* gray small buttons */
    button.calc.btn-gray {
      background: linear-gradient(180deg,#d1d1d1,#b5b5b5);
      color:#111;
    }
    /* operator */
    button.calc.btn-op {
      background: linear-gradient(180deg,var(--accent),var(--accent-dark));
      color:white;
    }
    button.calc.btn-eq {
      background: linear-gradient(180deg,var(--equal), #2fbf4d);
      color:white;
      grid-row: 4 / 6;
      height: 156px;
      border-radius: 36px;
    }
    /* wide zero */
    button.calc.btn-zero {
      grid-column: 1 / 3;
      border-radius: 36px;
    }
    /* press effect - bounce */
    button.calc:active {
      transform: translateY(3px) scale(0.98);
      box-shadow: 0 3px 8px rgba(0,0,0,0.6), inset 0 1px 2px rgba(255,255,255,0.02);
    }
    button.calc:focus { outline: none; }
    .hint {
      text-align:center;
      margin-top:10px;
      color: rgba(255,255,255,0.55);
      font-size:13px;
    }
    /* responsive */
    @media (max-width:420px){
      .container{ padding:16px; }
      .display{ font-size:36px; height:74px; }
      button.calc{ height:62px; font-size:20px; }
    }
  </style>
</head>
<body>
  <div class="container" role="application" aria-label="Calculator">
    <div style="position:relative;">
      <div class="small">Phone Calculator</div>
      <div id="display" class="display">0</div>
    </div>

    <div class="grid" id="keys">
      <!-- Row 1 -->
      <button class="calc btn-gray" data-key="AC">AC</button>
      <button class="calc btn-gray" data-key="back">←</button>
      <button class="calc btn-gray" data-key="%">%</button>
      <button class="calc btn-op" data-key="/">÷</button>

      <!-- Row 2 -->
      <button class="calc btn-dark" data-key="7">7</button>
      <button class="calc btn-dark" data-key="8">8</button>
      <button class="calc btn-dark" data-key="9">9</button>
      <button class="calc btn-op" data-key="*">×</button>

      <!-- Row 3 -->
      <button class="calc btn-dark" data-key="4">4</button>
      <button class="calc btn-dark" data-key="5">5</button>
      <button class="calc btn-dark" data-key="6">6</button>
      <button class="calc btn-op" data-key="-">−</button>

      <!-- Row 4 -->
      <button class="calc btn-dark" data-key="1">1</button>
      <button class="calc btn-dark" data-key="2">2</button>
      <button class="calc btn-dark" data-key="3">3</button>
      <button class="calc btn-op" data-key="+">+</button>

      <!-- Row 5 -->
      <button class="calc btn-dark btn-zero" data-key="0">0</button>
      <button class="calc btn-dark" data-key=".">.</button>
      <button class="calc btn-eq" data-key="=">=</button>
    </div>

    <div class="hint">You can also use your keyboard — numbers, + - * /, Enter (=), Backspace</div>
  </div>

  <!-- Audio (tap sound). Uses a small free sound hosted on pixabay CDN. -->
  <audio id="tapSound" preload="auto">
    <source src="https://cdn.pixabay.com/audio/2021/08/04/audio_86a096b6f9.mp3" type="audio/mpeg">
  </audio>

  <script>
    (function(){
      const display = document.getElementById('display');
      const keys = document.getElementById('keys');
      const tap = document.getElementById('tapSound');

      let expr = '';           // current expression string
      let justEvaluated = false; // if last action was evaluation

      function playTap(){
        try {
          tap.currentTime = 0;
          tap.play();
        } catch(e){}
      }

      function updateDisplay(){
        if(expr === '' ) display.textContent = '0';
        else display.textContent = expr;
      }

      function safeEval(s){
        // Basic safety: allow only digits, operators, dot, parentheses, percent
        if(/^[0-9+\-*/().% \t]+$/.test(s) === false) return 'Error';
        try {
          // handle percent: convert "number%" to "(number/100)"
          // replace occurrences like "50%" => "(50/100)"
          let t = s.replace(/([0-9.]+)%/g, '($1/100)');
          // Evaluate using Function to avoid access to scope
          // eslint-disable-next-line no-new-func
          const res = Function('"use strict";return (' + t + ')')();
          if (res === Infinity || Number.isNaN(res)) return 'Error';
          // round to sensible digits
          const rounded = Math.round((res + Number.EPSILON) * 1e12) / 1e12;
          return String(rounded);
        } catch(e) {
          return 'Error';
        }
      }

      function pressKey(k){
        playTap();
        if(k === 'AC'){
          expr = '';
          justEvaluated = false;
        } else if(k === 'back'){
          if(justEvaluated){
            expr = '';
            justEvaluated = false;
          } else {
            expr = expr.slice(0,-1);
          }
        } else if(k === '='){
          if(expr.trim() === '') return;
          const result = safeEval(expr);
          expr = result;
          justEvaluated = true;
        } else {
          if(justEvaluated && /[0-9.]/.test(k)){
            // if last was result and user types a number, start new
            expr = k;
            justEvaluated = false;
          } else {
            expr += k;
            justEvaluated = false;
          }
        }
        updateDisplay();
      }

      // mouse clicks
      keys.addEventListener('click', function(e){
        const btn = e.target.closest('button');
        if(!btn) return;
        const k = btn.getAttribute('data-key');
        pressKey(k);
      });

      // keyboard
      document.addEventListener('keydown', function(e){
        const allowed = ['0','1','2','3','4','5','6','7','8','9',
                         '+','-','*','/','.','%','(',')'];
        if(allowed.includes(e.key)){
          pressKey(e.key);
          e.preventDefault();
        } else if(e.key === 'Enter' || e.key === '='){
          pressKey('=');
          e.preventDefault();
        } else if(e.key === 'Backspace'){
          pressKey('back');
          e.preventDefault();
        } else if(e.key === 'Escape'){
          pressKey('AC');
          e.preventDefault();
        }
      });

      // Prevent text selection while double-clicking etc.
      document.addEventListener('selectstart', (e) => e.preventDefault());

      // init
      updateDisplay();

      // allow tapping with touchstart to feel more immediate on mobile
      keys.addEventListener('touchstart', function(e){
        const btn = e.target.closest('button');
        if(!btn) return;
        btn.classList.add('touched');
      }, {passive:true});

    })();
  </script>
</body>
</html>
"""

# embed the HTML into Streamlit. height chosen to accommodate design and mobile.
components.html(html_code, height=760, scrolling=True)

st.markdown(
    """
    **Notes & tips**
    - Works on desktop & mobile browsers.
    - Keyboard supported: `0–9`, `+ - * /`, `Enter` (equals), `Backspace` (delete), `Esc` (AC).
    - `%` works as percentage (e.g. `50%` equals `0.5`).
    - If sound doesn't play automatically in some browsers, click any button once (browsers often require a user gesture).
    """
)
