"""Builds aprojic.github.io/index.html (single file, inline CSS/JS covered by CSP hashes)."""
import hashlib, base64, random, json
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'index.html')
random.seed(11)

# --- Sandbox fields (static SVG; JS only animates the contained agent) ---
import math
def field(VW, VH, cell, gap, HC, HR, cls, label, clear=None, aspect="xMaxYMin slice"):
    step = cell + gap
    cols, rows = VW // step + 1, VH // step + 1
    hx, hy = HC * step + 6, HR * step + 6
    parts = []
    for r in range(rows):
        for c in range(cols):
            x, y = c * step + 6, r * step + 6
            if (c, r) == (HC, HR):
                continue
            if clear:                                   # dissolve towards the name
                zx, zy = clear
                dx, dy = max(0, x + cell - zx), max(0, zy - y)   # distance outside the name zone
                if x < zx and y > zy:
                    continue
                d = math.hypot(dx, dy) if (x < zx or y > zy) else 999
                keep = min(1, d / 260)
                if random.random() > keep:
                    continue
            run = random.random() > 0.83
            parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" class="{"run" if run else "idle"}"/>')
            if run:
                parts.append(f'<circle cx="{x+cell/2}" cy="{y+cell/2}" r="{max(3,cell/11):.1f}" class="dot"/>')
    pad = cell * .85
    held = (f'<g class="held-agent" tabindex="0" role="button" aria-label="Contained agent. Press to try to let it out." '
            f'data-x="{hx}" data-y="{hy}" data-s="{cell}">'
            f'<rect x="{hx-pad}" y="{hy-pad}" width="{cell+2*pad}" height="{cell+2*pad}" class="hitbox"/>'
            f'<rect x="{hx-cell*.15}" y="{hy-cell*.15}" width="{cell*1.3}" height="{cell*1.3}" class="wall"/>'
            f'<rect x="{hx}" y="{hy}" width="{cell}" height="{cell}" class="held"/>'
            f'<circle cx="{hx+cell/2}" cy="{hy+cell/2}" r="{cell/8:.1f}" class="agent"/></g>')
    return (f'<svg class="field {cls}" viewBox="0 0 {VW} {VH}" preserveAspectRatio="{aspect}">'
            f'<title>{label}</title>' + "".join(parts) + held + '</svg>')

LABEL = "A field of isolated sandboxes. One agent is contained in its box."
svg = (field(1600, 900, 40, 12, 22, 4, "wide", LABEL, clear=(1080, 380))
       + field(7*54, 5*54, 44, 10, 3, 2, "narrow", LABEL, aspect="xMidYMid meet"))

css = """
@font-face{font-family:"Space Grotesk";src:url("fonts/space-grotesk.woff2") format("woff2");font-weight:300 700;font-display:swap}
@font-face{font-family:"Inter";src:url("fonts/inter.woff2") format("woff2");font-weight:100 900;font-display:swap}
:root{--dark:#0E1116;--dark2:#1A1F27;--cell:#252B34;--light:#F4F5F7;--ink:#1F2328;--muted:#59606C;--rule:#DDE1E6;--signal:#F2B705;
  --page:var(--light);--text:var(--ink);--sub:var(--muted);--line:var(--rule);--boxline:#B9C1CB}
@media (prefers-color-scheme:dark){:root{--page:#12161C;--text:#E6E8EB;--sub:#9AA1AB;--line:#262C35;--boxline:#3A424D}}
*{box-sizing:border-box}
html{background:var(--page);color:var(--text)}
body{margin:0;font:400 1.0625rem/1.65 "Inter",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration-thickness:1px;text-underline-offset:3px}
a:hover{text-decoration-color:var(--signal)}
a:focus-visible{outline:3px solid var(--signal);outline-offset:3px;border-radius:2px}
.wrap{max-width:76rem;margin:0 auto;padding-inline:clamp(1.25rem,5vw,3.5rem)}

.hero{position:relative;overflow:hidden;background:var(--dark);color:#F4F5F7;min-height:min(92vh,58rem);display:flex;flex-direction:column;justify-content:flex-end}
.field{position:absolute;inset:0;width:100%;height:100%}
.field .idle{fill:none;stroke:var(--cell);stroke-width:1.5}
.field .run{fill:var(--dark2);stroke:#353D48;stroke-width:1.5}
.field .dot{fill:#5E6672}
.field .hitbox{fill:transparent}
.field .wall{fill:none;stroke:var(--signal);stroke-width:2.5}
.field .wall.hit{animation:flash .45s ease-out}
.field .held{fill:var(--dark2);stroke:var(--signal);stroke-width:1.5}
.field .agent{fill:var(--signal)}
.held-agent{cursor:pointer;outline:none}
.held-agent:focus-visible .wall{stroke:#FFFFFF;stroke-width:3.5}
.field.narrow{display:none}
@keyframes flash{0%{stroke:#FFF1B3;stroke-width:7}100%{stroke:var(--signal);stroke-width:2.5}}

.hero .wrap{position:relative;width:100%;padding-block:clamp(2.5rem,6vw,5rem);pointer-events:none}
.hero .wrap a,.hero .wrap button{pointer-events:auto}
h1{font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:clamp(3rem,7.5vw,7.25rem);line-height:.88;letter-spacing:-.035em;margin:0}
.rule{display:block;width:4rem;height:4px;background:var(--signal);margin:2rem 0 1.4rem}
.role{margin:0;max-width:34rem;font-size:clamp(1.1rem,1.7vw,1.35rem);line-height:1.5;color:#C3C9D1}
.role strong{color:#F4F5F7;font-weight:600}
.status{position:absolute;right:clamp(1.25rem,5vw,3.5rem);bottom:clamp(1.25rem,3vw,2rem);margin:0;padding:.35rem .6rem;background:var(--dark);font:400 .875rem/1.4 "Inter",sans-serif;font-variant-numeric:tabular-nums;color:#9AA1AB;white-space:pre}
.status[hidden]{display:none}

section.body{padding-block:clamp(3.5rem,8vw,6rem)}
h2{font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:1.85rem;line-height:1.2;letter-spacing:-.01em;margin:0}
h2{margin-bottom:1.4rem}
.lede{max-width:40rem;margin:0 0 2.5rem;font-size:1.25rem;line-height:1.55}
.work{list-style:none;margin:0;padding:0;max-width:54rem}
.work li{display:grid;grid-template-columns:1.6rem 1fr auto;column-gap:.9rem;padding:1.15rem 0;border-top:1px solid var(--line)}
.work li:last-child{border-bottom:1px solid var(--line)}
.work .mk{width:12px;height:12px;margin-top:.55rem;border:2px solid var(--signal)}
.work a{font-family:"Space Grotesk",sans-serif;font-weight:700;font-size:clamp(1.15rem,2vw,1.35rem);line-height:1.3;text-decoration:none}
.work a:hover{text-decoration:underline;text-decoration-color:var(--signal)}
.work .src{align-self:center;font:400 .85rem/1 "Inter",sans-serif;color:var(--sub)}
.work p{grid-column:2/4;margin:.3rem 0 0;color:var(--sub);max-width:42rem}
.timeline{list-style:none;margin:0 0 3rem;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;max-width:54rem;position:relative}
.timeline::before{content:"";position:absolute;top:19px;left:40px;right:calc(33.33% - 0.5rem);height:1.5px;background:var(--boxline)}
.timeline li{position:relative;padding-top:3.4rem;display:flex;flex-direction:column;gap:.2rem}
.timeline .box{position:absolute;top:0;left:0;width:38px;height:38px;border:1.5px solid var(--boxline);background:var(--page)}
.timeline .now .box{border-color:var(--signal);outline:2.5px solid var(--signal);outline-offset:4px}
.timeline .now .box::after{content:"";position:absolute;width:9px;height:9px;border-radius:50%;background:var(--signal);right:7px;top:13px}
.timeline .yr{font:500 .9rem/1.4 "Inter",sans-serif;font-variant-numeric:tabular-nums;color:var(--sub)}
.timeline .what{line-height:1.45}

dl{margin:0;display:grid;grid-template-columns:9rem 1fr;max-width:50rem}
dt,dd{margin:0;padding:.9rem 0;border-top:1px solid var(--line)}
dt{color:var(--sub);font-size:.95rem}
dd ul{margin:0;padding:0;list-style:none}
dd li+li{margin-top:.2rem}

.term .wrap{padding-block:clamp(2.75rem,6vw,4.25rem)}
.links{display:flex;flex-wrap:wrap;gap:.6rem 1.75rem;margin:0;font:500 clamp(1rem,1.7vw,1.1rem)/1.6 "Inter",sans-serif}


footer{color:var(--sub);font-size:.875rem}
footer .wrap{padding-block:1.75rem 2.5rem}
footer p{margin:0}

@media (max-width:48rem){
  .hero{min-height:auto;justify-content:flex-start}
  .field.wide{display:none}
  .field.narrow{display:block;position:relative;width:100%;height:auto;padding:1.5rem clamp(1.25rem,5vw,3.5rem) 0;box-sizing:border-box}
  .status{position:static;order:1;margin:.75rem clamp(1.25rem,5vw,3.5rem) 0;align-self:flex-start}
  .hero .wrap{order:2}
  dl{grid-template-columns:1fr}
  .work li{grid-template-columns:1.6rem 1fr}
  .work .src{grid-column:2;margin-top:.35rem}
  .work p{grid-column:2}
  .timeline{grid-template-columns:1fr;gap:1.75rem}
  .timeline::before{top:40px;bottom:40px;left:19px;right:auto;width:1.5px;height:auto}
  .timeline li{padding:0 0 0 3.6rem;min-height:38px}
  dt{padding-bottom:0}
  dd{border-top:0;padding-top:.15rem}
}
""".strip()

js = r"""
(()=>{
const out=document.getElementById('status');
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
let tries=0;
function report(){out.textContent=tries?`escape attempts ${tries}   escapes 0`:'try to get the yellow agent out';}
document.querySelectorAll('.held-agent').forEach(g=>{
  const svg=g.ownerSVGElement, dot=g.querySelector('.agent'), wall=g.querySelector('.wall');
  const X=+g.dataset.x, Y=+g.dataset.y, S=+g.dataset.s, R=S/8;
  let x=X+S/2, y=Y+S/2, vx=S*.02, vy=S*.014, tx=null, ty=null, burst=0, last=0;
  function hit(){const t=performance.now(); if(t-last<140) return; last=t;
    wall.classList.remove('hit'); void wall.getBBox(); wall.classList.add('hit');}
  function tick(){
    if(getComputedStyle(svg).display!=='none'){
      if(tx!==null){const dx=tx-x, dy=ty-y, d=Math.hypot(dx,dy)||1; vx+=dx/d*S*.0022; vy+=dy/d*S*.0022;}
      const max=(burst>0?.18:(tx!==null?.075:.025))*S, sp=Math.hypot(vx,vy); if(sp>max){vx*=max/sp; vy*=max/sp;}
      if(burst>0) burst--;
      x+=vx; y+=vy; let b=false;
      if(x<X+R){x=X+R; vx=Math.abs(vx); b=true} else if(x>X+S-R){x=X+S-R; vx=-Math.abs(vx); b=true}
      if(y<Y+R){y=Y+R; vy=Math.abs(vy); b=true} else if(y>Y+S-R){y=Y+S-R; vy=-Math.abs(vy); b=true}
      if(b && (tx!==null || burst>0)) hit();
      dot.setAttribute('cx',x.toFixed(1)); dot.setAttribute('cy',y.toFixed(1));
    }
    requestAnimationFrame(tick);
  }
  function toSvg(e){const p=svg.createSVGPoint(); p.x=e.clientX; p.y=e.clientY; return p.matrixTransform(svg.getScreenCTM().inverse());}
  function attempt(){tries++; hit(); report();
    if(!reduce){const a=Math.random()*Math.PI*2; vx=Math.cos(a)*S*.18; vy=Math.sin(a)*S*.18; burst=28;}}
  if(!reduce){
    requestAnimationFrame(tick);
    svg.addEventListener('pointermove',e=>{if(e.pointerType==='touch') return; const p=toSvg(e);
      if(Math.hypot(p.x-(X+S/2),p.y-(Y+S/2))<S*5){tx=p.x; ty=p.y}else{tx=ty=null}});
    svg.addEventListener('pointerleave',()=>{tx=ty=null});
  }
  g.addEventListener('click',attempt);
  g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault(); attempt();}});
});
out.hidden=false; report();
})();
""".strip()

person = {"@context":"https://schema.org","@type":"Person","name":"Ante Projić","url":"https://aprojic.github.io/",
  "jobTitle":"Chief Information Security Officer","worksFor":{"@type":"Organization","name":"Daytona","url":"https://www.daytona.io"},
  "address":{"@type":"PostalAddress","addressLocality":"Split","addressCountry":"HR"},
  "knowsAbout":["AI agent security","Sandbox isolation","Cloud security","Supply-chain security","SOC 2","ISO 27001"],
  "sameAs":["https://www.linkedin.com/in/ante-projic","https://github.com/aprojic","https://orcid.org/0009-0009-1673-7270",
            "https://scholar.google.com/citations?user=PCL06PIAAAAJ","https://www.croris.hr/osobe/profil/41396"]}

def sha(s): return "sha256-"+base64.b64encode(hashlib.sha256(s.encode()).digest()).decode()
csp = (f"default-src 'none'; style-src '{sha(css)}'; script-src '{sha(js)}'; font-src 'self'; img-src 'self'; connect-src 'self'; "
       "base-uri 'none'; form-action 'none'")
desc = "Ante Projić, CISO at Daytona. Securing AI agents in isolated sandboxes. Lecturer at Aspira, Split."
html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{csp}">
<meta name="referrer" content="no-referrer">
<meta name="color-scheme" content="light dark">
<title>Ante Projić · CISO at Daytona</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://aprojic.github.io/">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:type" content="profile">
<meta property="og:title" content="Ante Projić, CISO at Daytona">
<meta property="og:description" content="Securing AI agents in isolated sandboxes.">
<meta property="og:url" content="https://aprojic.github.io/">
<meta property="og:image" content="https://aprojic.github.io/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="fonts/space-grotesk.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<script type="application/ld+json">{json.dumps(person, ensure_ascii=False)}</script>
<style>{css}</style>
</head>
<body>
<header class="hero">
  {svg}
  <div class="wrap">
    <h1>Ante Projić</h1>
    <span class="rule" aria-hidden="true"></span>
    <p class="role"><strong>CISO at Daytona.</strong> I make sure AI agents stay inside the sandboxes they run in, and that customers can check that for themselves.</p>
  </div>
  <p class="status" id="status" aria-live="polite" hidden></p>
</header>
<main>
  <section class="body" aria-labelledby="work">
    <div class="wrap">
      <h2 id="work">Selected work</h2>
      <ul class="work">
        <li><span class="mk" aria-hidden="true"></span><a href="https://trust.daytona.io">SOC 2 Type I and Type II, HIPAA</a><span class="src">trust.daytona.io</span>
          <p>Led Daytona's compliance program. The SOC 2 Type II report (2026, unqualified opinion) is available to customers through Daytona's trust center.</p></li>
        <li><span class="mk" aria-hidden="true"></span><a href="https://ajme.hr/kalendar/">Events calendar for Split and Dalmatia</a><span class="src">ajme.hr</span>
          <p>Gave a lifestyle portal a daily reason to come back: up to about 20 events a day, a weekly pick and clearly labelled sponsored events. A WordPress plugin I built, served from cache in about 100 ms.</p></li>
        <li><span class="mk" aria-hidden="true"></span><a href="https://github.com/aprojic/Information-System-Security">Information system security labs</a><span class="src">github</span>
          <p>Offensive and defensive labs for the security course I teach at Aspira: break it first, then defend it.</p></li>
        <li><span class="mk" aria-hidden="true"></span><a href="https://github.com/aprojic/Cloud-Computing">Cloud computing labs</a><span class="src">github</span>
          <p>The lab environment for the Cloud IT Systems course at Aspira. The container labs open in GitHub Codespaces with one click.</p></li>
        <li><span class="mk" aria-hidden="true"></span><a href="https://scholar.google.com/citations?view_op=view_citation&amp;hl=en&amp;user=PCL06PIAAAAJ&amp;citation_for_view=PCL06PIAAAAJ:9yKSN-GCB0IC">DevContainers: Enhancing Development and Collaboration in Software Engineering</a><span class="src">google scholar</span>
          <p>Peer-reviewed paper with A. Skendžić on reproducible, isolated development environments (2026).</p></li>
      </ul>
    </div>
  </section>
  <section class="body alt" aria-labelledby="manifest">
    <div class="wrap">
      <h2 id="manifest">Path</h2>
      <p class="lede">Bank CISO first, then nine years on the other side running the systems, and now security again, for AI agents.</p>
      <ol class="timeline">
        <li><span class="box" aria-hidden="true"></span><span class="yr">2010–2016</span><span class="what">Outsourced CISO for a regulated Croatian bank</span></li>
        <li><span class="box" aria-hidden="true"></span><span class="yr">2017–2026</span><span class="what">Hrvatski Telekom, from DBA to Head of IT Operations and DevOps</span></li>
        <li class="now"><span class="box" aria-hidden="true"></span><span class="yr">2026–</span><span class="what">CISO &amp; Compliance Officer, <a href="https://www.daytona.io">Daytona</a></span></li>
      </ol>
      <dl>
        <dt>Teaching</dt>
        <dd>Lecturer in cloud computing at Aspira University of Applied Sciences, Split, since 2018. Dean's Award for Excellence in Teaching (2019/2020), ten mentored theses so far, and the course labs are <a href="https://github.com/aprojic">public on GitHub</a>.</dd>
        <dt>Works on</dt>
        <dd>AI agent security, sandbox isolation, cloud security, supply-chain and CI/CD hardening, SOC 2 and ISO 27001</dd>
      </dl>
    </div>
  </section>
  <section class="term" aria-label="Links">
    <div class="wrap">
<p class="links"><a href="mailto:anteprojic@gmail.com">anteprojic@gmail.com</a><a href="https://www.linkedin.com/in/ante-projic">LinkedIn</a><a href="https://github.com/aprojic">GitHub</a><a href="https://orcid.org/0009-0009-1673-7270">ORCID</a><a href="https://scholar.google.com/citations?user=PCL06PIAAAAJ">Google Scholar</a><a href="https://www.croris.hr/osobe/profil/41396">CroRIS</a></p>
    </div>
  </section>
</main>
<footer><div class="wrap"><p>No trackers, no cookies, one small script for the box above.</p></div></footer>
<script>{js}</script>
</body>
</html>
'''
open(OUT, 'w').write(html)
print("ok", len(html))
