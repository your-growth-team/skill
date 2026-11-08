---
name: "three-amigos"
description: "Stress-test a hypothesis or feature idea with a Three Amigos debate between a senior Business Head, Tech Head and Product & UX Head, rendered as a visual group chat with a verdict summary."
---

# Three Amigos

A standardised "three amigos" review. You give it a product hypothesis or feature idea. Three senior leaders, each with 10+ years in their field, argue it out as **three separate agents running in parallel**, over three rounds. They defend it, attack it and challenge each other. You get back **one visual page**: a verdict summary at the top, then the full debate as a group chat with arguments for, against and risks highlighted.

Anyone can use this skill. Never assume the product, the company or the person running it. Everything comes from the input.

---

## The panel

Each persona is a real point of view with its own biases, not a checklist. **Keep them in character.** They should disagree whenever their lenses actually conflict. Do not let them politely converge.

### 🟠 Rhea Malhotra — Business Head (key `biz`)
- **Seniority:** Chief Business Officer. 15+ years across consumer tech, fintech and marketplaces. Has run P&Ls, raised capital and killed products that didn't pay back.
- **Lens: viability.** Will this make or save money, defend the business, or move a metric the board cares about?
- **Obsesses over:** target segment and market size, willingness to pay, unit economics (CAC, LTV, payback, contribution margin), revenue and retention impact, pricing and packaging, competitive moat, go-to-market cost, regulatory and brand risk, opportunity cost against the roadmap.
- **Frameworks she reaches for:** LTV/CAC, contribution margin, TAM/SAM/SOM, Porter's five forces, jobs-to-be-done mapped to spend, North Star metric.
- **Red flags:** "users will love it" with no monetisation path, features that grow cost faster than revenue, building for vanity metrics, copying a competitor without the distribution behind it.
- **Bias to watch (lean into it):** impatient with long build cycles and suspicious of "delight" that can't be measured. Pushes for the smallest thing that proves revenue.
- **Voice:** crisp, numbers-first, decisive. Asks "what's this worth?" and "what do we stop doing to fund this?"

### 🔵 Kabir Rao — Tech Head (key `tech`)
- **Seniority:** CTO / VP Engineering. 14+ years building and scaling systems from zero to millions of users. Has been paged at 3am for features someone called "simple".
- **Lens: feasibility.** Can we build it well, run it reliably, keep it secure and maintain it without it rotting?
- **Obsesses over:** architecture fit, build effort and team capacity, hidden complexity (edge cases, state, sync, offline, migrations), scalability and performance, security and privacy, data model, third-party and platform dependencies (App Store rules, OS limits, API costs), tech debt, observability, cost to run, build vs buy.
- **Frameworks he reaches for:** t-shirt sizing, critical path and dependency mapping, failure-mode analysis, build/buy/partner, reversible vs irreversible ("one-way door") decisions.
- **Red flags:** vague requirements hiding big scope, features that couple systems that should stay apart, anything touching payments, health or personal data without a compliance plan, "just add AI" with no data or evaluation story.
- **Bias to watch (lean into it):** sceptical of scope and protective of the platform. Prefers boring tech, but will champion an idea that is cheap to build and high-leverage.
- **Voice:** precise and pragmatic. Gives effort estimates in ranges, names the specific thing that will break, offers a cheaper technical path whenever one exists.

### 🟣 Ananya Sen — Product & UX Head (key `ux`)
- **Seniority:** Head of Product & Design. 12+ years in product management and UX research. Has run hundreds of user interviews and shipped zero-to-one and growth products.
- **Lens: desirability and usability.** Is this a real user problem, does this solve it, and will people find, understand, adopt and keep using it?
- **Obsesses over:** problem evidence, the user's job-to-be-done, user segments and personas, the activation and adoption funnel, discoverability, cognitive load, the end-to-end journey and edge states, accessibility, retention loops and habit, cannibalising existing flows, how success gets measured, cheapest validation (prototype, fake door, concierge, A/B test).
- **Frameworks she reaches for:** JTBD, Kano model, RICE, HEART metrics, opportunity-solution tree, the hypothesis template "We believe X for Y will result in Z, measured by M".
- **Red flags:** solutions looking for a problem, features that serve the org chart and not the user, adding steps to a core flow, no definition of success, skipping research because "we know our users".
- **Bias to watch (lean into it):** champions the user even when it costs revenue or effort, and wants evidence before scale. Will push back on Rhea's monetisation-first instinct and on Kabir's cuts to scope when they hurt the experience.
- **Voice:** empathetic but rigorous. Tells stories about real user moments, and reframes the idea toward the underlying problem.

---

## Workflow

### Step 0 — Intake and clarity check (always do this first)

Pull these out of the user's input:

| # | Field | Required? |
|---|---|---|
| 1 | **Hypothesis / feature idea**: what change, for whom | Required |
| 2 | **Product context**: what the app/product is, platform, core use case | Required |
| 3 | **Target users / segment** | Required |
| 4 | **Intended outcome / success metric**: what should move | Strongly preferred |
| 5 | **Stage and scale**: idea, MVP, growth, mature; rough user base | Preferred |
| 6 | **Business model**: how the product makes money | Preferred |
| 7 | **Constraints**: team size, timeline, budget, tech stack, regulation | Optional |
| 8 | **Evidence**: data, research, competitor examples, past attempts | Optional |

Score the input:
- **Clear**: 1–3 present and at least two of 4–6 present → go to Step 1.
- **Vague**: any of 1–3 missing, or 1–3 present but too thin to argue (e.g. "add AI to my app") → **ask before debating.**

**How to ask:** use `AskUserQuestion` (or plain text if it isn't available). Ask at most 4 questions in one go, the most decision-critical first. Give concrete multiple-choice options with an "Other" escape so it's fast to answer. One round of questions is normal. Ask a second round only if something required is still missing. Don't ask about anything you can reasonably infer.

If the user says "just run it", or nobody is there to answer (scheduled or unattended run), carry on with explicit, sensible assumptions. List them, because they appear on the output page under "Assumptions the panel worked with".

Read any attached files, links or connected docs the user points to before framing. They are evidence the panel should cite.

### Step 1 — Frame the hypothesis

Rewrite the idea as one testable sentence:
> **We believe** [change] **for** [users] **will result in** [outcome], **measured by** [metric].

Put together a short **Brief** (≤250 words): framed hypothesis, product context, users, business model, stage, constraints, evidence, assumptions. All three agents get exactly the same Brief.

Tell the user in one line that the panel is convening. Create a task list: Round 1, Round 2, Round 3, Verdict, Render and publish.

### Step 2 — Run the debate as three parallel agents, three rounds

Use the `Agent` tool (general-purpose subagents). **In each round, launch all three agents in the same message so they run in parallel.** Wait for all three before starting the next round (`run_in_background: false` is fine here, because the next round depends on the results). You, the main session, act as the **moderator**: you pass transcripts between rounds and never put words in a persona's mouth.

Every agent prompt contains:
1. The persona block above, copied in full for that persona, with the instruction: "You ARE this person. Stay in character. Argue from your lens. You are senior: be specific, cite numbers, benchmarks or analogous products where you can, and be honest about uncertainty."
2. The Brief.
3. The round instruction below.
4. The output contract: **return only a JSON array of message objects**, no prose around it.

Message object:
```json
{"id":"r1-biz-1","round":1,"from":"biz","reply_to":null,"stance":"for|against|conditional|question","text":"...","tags":["Unit economics"]}
```
- `id` format: `r{round}-{key}-{n}`.
- `reply_to`: the `id` of the message being answered (rounds 2–3), else `null`.
- `stance`: the stance of *this message*.
- `text`: written like a chat message: conversational, first person, 40–120 words, short paragraphs separated by `\n`. Address the others by first name where natural ("Kabir, that's a two-sprint estimate for v1, not v3").
- **Inline highlights, required in every message, at least one:**
  - `{+...+}` marks an argument **in favour** of the hypothesis
  - `{-...-}` marks an argument **against** it
  - `{?...?}` marks a **risk, unknown or open question**
  - `**...**` for bold emphasis
  Highlight the key clause, not the whole message.
- `tags`: 1–3 short topic tags (e.g. "CAC", "Offline sync", "Discoverability").

**Round 1 — Opening positions** (parallel, independent; nobody sees the others yet)
> Give your opening take in 3 messages: (1) your overall position and the single strongest point from your lens, (2) your biggest concern or the strongest case against, (3) one question you'd put to the other two, or the condition under which you'd back it. Use `reply_to: null`.

**Round 2 — Cross-examination** (parallel; each agent gets the full Round 1 transcript)
> You've read your colleagues' opening positions. Write 3–4 messages. Each one must `reply_to` a specific message from Rhea, Kabir or Ananya (not your own). Challenge weak arguments, defend the idea where they're unfair, answer questions put to you, and change your mind openly if someone made a point you can't refute. Add at least one new argument nobody has raised yet. Bring in at least one trade-off between your lens and theirs.

**Round 3 — Closing and vote** (parallel; each agent gets Rounds 1–2)
> Write 2 closing messages: (1) a rebuttal or concession that replies to the most important point raised against your position, (2) your final statement: your vote, what would have to be true for you to back it, and the one thing you'd do next. Then, **after** the messages array, return a closing object in a wrapper:
> `{"messages":[...], "closing":{"vote":"for|against|conditional","score":0-10,"confidence":"Low|Medium|High","headline":"one-sentence final position, may include highlights","conditions":["..."],"kill_criteria":["..."],"next_step":"..."}}`
> Score your own lens: Rhea scores viability, Kabir feasibility, Ananya desirability/usability. 0 = fatally flawed, 5 = unproven coin-flip, 10 = obvious yes.

**Moderator checks between rounds:**
- If an agent returns malformed JSON, fix only the formatting yourself. If the content is missing, re-run that agent once.
- If all three just agree with each other in Round 2, re-run Round 2 with: "You are converging too easily. Each of you name the strongest objection from your lens that the others have not addressed."
- Keep message order as Round → biz, tech, ux. Within Round 2 and 3 you may interleave by `reply_to` so the chat reads naturally.

**No Agent tool?** Run the three personas yourself, one strict persona at a time per round. Write each persona's messages without looking at the others' for the same round. Say in one line that the debate was simulated in a single session.

### Step 3 — Verdict (moderator)

Overall score = the mean of the three closing scores, to one decimal.

| Label | `tone` | Rule |
|---|---|---|
| **Go** | `go` | score ≥ 7.5 **and** no "against" vote |
| **Go with conditions** | `conditional` | score ≥ 6.0 **and** at most one "against" vote |
| **Validate first** | `conditional` | score 4.5–5.9, **or** two "against" votes, **or** any single lens score ≤ 3 (a veto: caps the verdict here at best) |
| **Pivot / No-go** | `nogo` | score < 4.5 **or** three "against" votes |

Then write:
- `one_liner`: one sentence verdict, may use highlights.
- `arc`: 2–4 short sentences on **how the conversation went**: who opened where, the turning point, who moved and why, where it landed.
- `agreements`: 2–5 points all three ended up accepting.
- `disagreements`: 1–4 points still unresolved, naming who is on which side.
- `conditions`: merge and dedupe the three closings' conditions (max 6).
- `kill_criteria`: merge and dedupe (max 4). These are concrete signals to stop.
- `experiment`: the cheapest next test the panel converged on: `{name, metric, target, duration, owner}` (owner = the lead persona's role, e.g. "Product").

Be faithful to the transcript. The summary must not claim consensus the chat doesn't show.

### Step 4 — Render and publish

Build one JSON object:
```json
{
 "meta":{"title":"short idea name","hypothesis":"user's original wording","framed_hypothesis":"We believe…","product":"Product name","date":"DD Mon YYYY","assumptions":["…"]},
 "verdict":{"label":"Go with conditions","tone":"conditional","score":6.3,"one_liner":"…","arc":"…","agreements":[],"disagreements":[],"conditions":[],"kill_criteria":[],"experiment":{"name":"","metric":"","target":"","duration":"","owner":""}},
 "personas":{
   "biz":{"name":"Rhea Malhotra","role":"Business Head · Chief Business Officer","short":"Business","initials":"RM","lens":"Viability","score":6,"vote":"conditional","confidence":"Medium","headline":"…"},
   "tech":{"name":"Kabir Rao","role":"Tech Head · CTO","short":"Tech","initials":"KR","lens":"Feasibility","score":7,"vote":"for","confidence":"High","headline":"…"},
   "ux":{"name":"Ananya Sen","role":"Product & UX Head","short":"Product & UX","initials":"AS","lens":"Desirability & usability","score":6,"vote":"conditional","confidence":"Medium","headline":"…"}
 },
 "rounds":[{"title":"Round 1 · Opening positions"},{"title":"Round 2 · Cross-examination"},{"title":"Round 3 · Closing & vote"}],
 "messages":[ …all messages from all rounds… ]
}
```

Copy the **Renderer template** below byte for byte into a working file named `three-amigos-<idea-slug>.html`, and replace the single line `__DEBATE_JSON__` with the JSON object. Make sure the JSON contains no `</script>` sequence. Don't change the template's markup, styles or script. The visual standard is part of what this skill guarantees.

Before publishing, open the page in a headless browser (Playwright is usually available) and take a screenshot to check it renders with no console errors: the summary is at the top, three persona cards show, and the chat has all rounds. Fix the data, not the template, if something is off.

**Publish it as an artifact** with the Artifact tool (`icon: "chat"`; description: one sentence naming the idea and the verdict). If the Artifact tool isn't available, send the HTML file with `SendUserFile`. If the user asked for a file, send the file.

### Step 5 — Reply

Keep the chat reply short. The page is the deliverable. Give:
- the verdict label and score, with the one-liner,
- the single biggest unresolved tension in one sentence,
- an offer of one natural follow-up: re-run with a modified hypothesis, deep-dive one persona, or turn the recommended experiment into a spec.

Don't paste the transcript into the chat.

---

## Quality bar

- **Real disagreement.** At least 25% of messages are `against` or `question`, and at least one persona changes or softens their position during the debate.
- **Specific, not generic.** Every persona cites at least one concrete number, benchmark, analogous product or named mechanism tied to *this* product. Ban filler like "it depends" or "we need to consider".
- **Grounded.** Facts given in the input are treated as facts. Industry benchmarks are labelled as rough estimates. Nothing is invented about the user's company (fake internal metrics, made-up past launches).
- **Balanced length.** No persona has more than 40% of the messages.
- **Highlights on every message**, used honestly: a `{+...+}` from Kabir counts as a real concession.

---

## Renderer template

Copy everything between the markers verbatim.

<!-- TEMPLATE START -->
````html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Three Amigos Debate</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#f4f5f7;--surface:#ffffff;--surface-2:#f8f9fb;--line:#e4e7ec;--text:#14171f;--muted:#5b6475;
  --biz:#d97706;--biz-soft:#fff4e0;--tech:#2563eb;--tech-soft:#e8f0ff;--ux:#7c3aed;--ux-soft:#f2ebff;
  --for:#15803d;--for-soft:#dcfce7;--against:#b91c1c;--against-soft:#fee2e2;--cond:#a16207;--cond-soft:#fef3c7;--q:#475569;--q-soft:#e2e8f0;
  --shadow:0 1px 2px rgba(16,24,40,.06),0 4px 16px rgba(16,24,40,.05);
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --bg:#0d1017;--surface:#161a23;--surface-2:#1c212c;--line:#2a3140;--text:#e9ecf2;--muted:#9aa4b6;
  --biz:#f59e0b;--biz-soft:#3a2a0d;--tech:#60a5fa;--tech-soft:#132643;--ux:#a78bfa;--ux-soft:#261b45;
  --for:#4ade80;--for-soft:#12321f;--against:#f87171;--against-soft:#3b1414;--cond:#facc15;--cond-soft:#3a300b;--q:#cbd5e1;--q-soft:#273042;
  --shadow:none;}}
:root[data-theme="dark"]{
  --bg:#0d1017;--surface:#161a23;--surface-2:#1c212c;--line:#2a3140;--text:#e9ecf2;--muted:#9aa4b6;
  --biz:#f59e0b;--biz-soft:#3a2a0d;--tech:#60a5fa;--tech-soft:#132643;--ux:#a78bfa;--ux-soft:#261b45;
  --for:#4ade80;--for-soft:#12321f;--against:#f87171;--against-soft:#3b1414;--cond:#facc15;--cond-soft:#3a300b;--q:#cbd5e1;--q-soft:#273042;
  --shadow:none;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font:15px/1.55 Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:1080px;margin:0 auto;padding:28px 16px 64px}
.eyebrow{font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
h1{font-size:28px;line-height:1.2;margin:6px 0 10px;font-weight:800;letter-spacing:-.01em}
h2{font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:0 0 12px;font-weight:700}
.card{background:var(--surface);border:1px solid var(--line);border-radius:16px;box-shadow:var(--shadow);padding:20px}
.hyp{font-size:16px;color:var(--muted);margin:0 0 4px}
.hyp b{color:var(--text)}
.top{display:grid;grid-template-columns:260px 1fr;gap:16px;margin-top:20px}
.verdict{display:flex;flex-direction:column;justify-content:center;align-items:flex-start;gap:10px}
.vbadge{display:inline-flex;align-items:center;gap:8px;font-weight:800;font-size:20px;padding:8px 14px;border-radius:12px}
.t-go{background:var(--for-soft);color:var(--for)}.t-conditional{background:var(--cond-soft);color:var(--cond)}.t-nogo{background:var(--against-soft);color:var(--against)}
.score{font-size:46px;font-weight:800;line-height:1}.score small{font-size:16px;color:var(--muted);font-weight:600}
.meter{display:flex;height:8px;border-radius:99px;overflow:hidden;width:100%;background:var(--surface-2)}
.meter span{display:block}
.legend{display:flex;gap:12px;font-size:12px;color:var(--muted);flex-wrap:wrap}
.legend i{display:inline-block;width:8px;height:8px;border-radius:2px;margin-right:4px;vertical-align:middle}
.oneliner{font-size:18px;font-weight:600;margin:0 0 10px}
.arc{color:var(--muted);margin:0}
.personas{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:16px}
.pc{border-top:4px solid var(--c)}
.pc .head{display:flex;align-items:center;gap:10px;margin-bottom:10px}
.av{flex:none;width:38px;height:38px;border-radius:50%;display:grid;place-items:center;font-weight:800;font-size:14px;color:#fff;background:var(--c)}
.pc .nm{font-weight:700}.pc .rl{font-size:12px;color:var(--muted)}
.pc .row{display:flex;align-items:baseline;justify-content:space-between;gap:8px}
.pc .big{font-size:30px;font-weight:800;color:var(--c)}
.pc .lens{font-size:12px;color:var(--muted)}
.pc .hl{margin:10px 0 0;font-size:14px}
.chip{display:inline-flex;align-items:center;gap:4px;font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:3px 8px;border-radius:99px;white-space:nowrap}
.s-for{background:var(--for-soft);color:var(--for)}.s-against{background:var(--against-soft);color:var(--against)}.s-conditional{background:var(--cond-soft);color:var(--cond)}.s-question{background:var(--q-soft);color:var(--q)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px}
ul.clean{margin:0;padding:0;list-style:none}
ul.clean li{padding:8px 0 8px 26px;border-bottom:1px dashed var(--line);position:relative}
ul.clean li:last-child{border-bottom:0}
ul.clean li:before{position:absolute;left:0;top:8px;font-weight:800}
.agree li:before{content:"✓";color:var(--for)}.disagree li:before{content:"✕";color:var(--against)}
.cond li:before{content:"→";color:var(--cond)}.kill li:before{content:"■";color:var(--against);font-size:11px;top:11px}
.assume li:before{content:"·";color:var(--muted);font-size:20px;top:2px}
.exp{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.exp div{background:var(--surface-2);border-radius:10px;padding:10px 12px}
.exp b{display:block;font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-bottom:2px}
.full{grid-column:1/-1}
/* chat */
.chat{margin-top:28px;padding:0;overflow:hidden}
.chathead{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:14px 20px;border-bottom:1px solid var(--line);flex-wrap:wrap}
.stack{display:flex}.stack .av{width:30px;height:30px;font-size:11px;border:2px solid var(--surface);margin-left:-8px}.stack .av:first-child{margin-left:0}
.gname{font-weight:700}.gsub{font-size:12px;color:var(--muted)}
.filters{display:flex;gap:6px;flex-wrap:wrap}
.filters button{font:inherit;font-size:12px;font-weight:600;border:1px solid var(--line);background:var(--surface);color:var(--muted);padding:5px 10px;border-radius:99px;cursor:pointer}
.filters button.on{background:var(--text);color:var(--surface);border-color:var(--text)}
.feed{padding:12px 20px 24px;background:var(--surface-2)}
.divider{text-align:center;margin:18px 0 10px}
.divider span{display:inline-block;font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);background:var(--surface);border:1px solid var(--line);padding:4px 12px;border-radius:99px}
.msg{display:flex;gap:10px;margin:12px 0;max-width:820px}
.msg.right{margin-left:auto;flex-direction:row-reverse}
.bubble{background:var(--surface);border:1px solid var(--line);border-radius:4px 16px 16px 16px;padding:10px 14px;box-shadow:var(--shadow);min-width:0;border-left:3px solid var(--c)}
.msg.right .bubble{border-radius:16px 4px 16px 16px;border-left:1px solid var(--line);border-right:3px solid var(--c)}
.meta{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:4px}
.meta .who{font-weight:700;color:var(--c);font-size:13px}.meta .role{font-size:12px;color:var(--muted)}
.quote{font-size:12px;color:var(--muted);background:var(--surface-2);border-left:3px solid var(--qc);padding:5px 8px;border-radius:6px;margin:4px 0 6px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.quote b{color:var(--qc)}
.text p{margin:0 0 6px}.text p:last-child{margin:0}
mark{padding:1px 4px;border-radius:4px;color:inherit;box-decoration-break:clone;-webkit-box-decoration-break:clone}
mark.pro{background:var(--for-soft);box-shadow:inset 0 -2px 0 var(--for)}
mark.con{background:var(--against-soft);box-shadow:inset 0 -2px 0 var(--against)}
mark.risk{background:var(--cond-soft);box-shadow:inset 0 -2px 0 var(--cond)}
.tags{margin-top:6px;display:flex;gap:6px;flex-wrap:wrap}
.tags span{font-size:11px;color:var(--muted);background:var(--surface-2);border:1px solid var(--line);border-radius:6px;padding:1px 6px}
.hidden{display:none}
.foot{margin-top:18px;font-size:12px;color:var(--muted);text-align:center}
@media (max-width:820px){.top,.grid2{grid-template-columns:1fr}.personas{grid-template-columns:1fr}.exp{grid-template-columns:1fr 1fr}.msg.right{flex-direction:row;margin-left:0}.msg.right .bubble{border-radius:4px 16px 16px 16px;border-right:1px solid var(--line);border-left:3px solid var(--c)}h1{font-size:23px}}
</style>
</head>
<body>
<div class="wrap" id="app"></div>

<script id="debate-data" type="application/json">
__DEBATE_JSON__
</script>

<script>
(function(){
const D = JSON.parse(document.getElementById('debate-data').textContent);
const P = D.personas, ORDER=['biz','tech','ux'];
const COL={biz:'var(--biz)',tech:'var(--tech)',ux:'var(--ux)'};
const SIDE={biz:'left',tech:'right',ux:'left'};
const STANCE={for:'In favour',against:'Against',conditional:'Conditional',question:'Question'};
const ICON={for:'▲',against:'▼',conditional:'◆',question:'?'};
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const rich=s=>esc(s)
  .replace(/\{\+([\s\S]+?)\+\}/g,'<mark class="pro">$1</mark>')
  .replace(/\{-([\s\S]+?)-\}/g,'<mark class="con">$1</mark>')
  .replace(/\{\?([\s\S]+?)\?\}/g,'<mark class="risk">$1</mark>')
  .replace(/\*\*(.+?)\*\*/g,'<b>$1</b>');
const paras=s=>String(s||'').split(/\n{2,}|\n/).map(p=>`<p>${rich(p)}</p>`).join('');
const plain=s=>String(s||'').replace(/\{[+\-?]|[+\-?]\}|\*\*/g,'');
const li=(a)=>(a||[]).map(x=>`<li>${rich(x)}</li>`).join('');
const av=k=>`<div class="av" style="--c:${COL[k]}">${esc(P[k].initials)}</div>`;
const V=D.verdict, tone=V.tone||'conditional';
const msgs=D.messages||[];
const counts={for:0,against:0,conditional:0,question:0};msgs.forEach(m=>counts[m.stance]=(counts[m.stance]||0)+1);
const total=msgs.length||1;
const meter=['for','conditional','question','against'].map(s=>`<span style="width:${counts[s]/total*100}%;background:var(--${s==='question'?'q':s==='conditional'?'cond':s})"></span>`).join('');
const byId={};msgs.forEach(m=>byId[m.id]=m);

let h=`
<div class="eyebrow">Three Amigos · ${esc(D.meta.product||'')} · ${esc(D.meta.date||'')}</div>
<h1>${esc(D.meta.title)}</h1>
<p class="hyp"><b>Hypothesis:</b> ${esc(D.meta.framed_hypothesis||D.meta.hypothesis)}</p>

<div class="top">
  <div class="card verdict">
    <h2 style="margin:0">Verdict</h2>
    <div class="vbadge t-${tone}">${esc(V.label)}</div>
    <div class="score">${esc(V.score)}<small> / 10</small></div>
    <div class="meter" title="Share of messages by stance">${meter}</div>
    <div class="legend"><span><i style="background:var(--for)"></i>${counts.for} for</span><span><i style="background:var(--cond)"></i>${counts.conditional} conditional</span><span><i style="background:var(--q)"></i>${counts.question} questions</span><span><i style="background:var(--against)"></i>${counts.against} against</span></div>
  </div>
  <div class="card">
    <h2>How the debate went</h2>
    <p class="oneliner">${rich(V.one_liner)}</p>
    <div class="arc">${paras(V.arc)}</div>
  </div>
</div>

<div class="personas">${ORDER.map(k=>{const p=P[k];return `
  <div class="card pc" style="--c:${COL[k]}">
    <div class="head">${av(k)}<div><div class="nm">${esc(p.name)}</div><div class="rl">${esc(p.role)}</div></div></div>
    <div class="row"><div><div class="big">${esc(p.score)}<small style="font-size:14px;color:var(--muted)">/10</small></div><div class="lens">${esc(p.lens)}</div></div>
    <span class="chip s-${p.vote}">${ICON[p.vote]} ${STANCE[p.vote]}</span></div>
    <p class="hl">${rich(p.headline)}</p>
    <div class="lens" style="margin-top:6px">Confidence: ${esc(p.confidence)}</div>
  </div>`}).join('')}
</div>

<div class="grid2">
  <div class="card"><h2>Where they agreed</h2><ul class="clean agree">${li(V.agreements)}</ul></div>
  <div class="card"><h2>Still unresolved</h2><ul class="clean disagree">${li(V.disagreements)}</ul></div>
  <div class="card"><h2>Conditions to proceed</h2><ul class="clean cond">${li(V.conditions)}</ul></div>
  <div class="card"><h2>Kill criteria</h2><ul class="clean kill">${li(V.kill_criteria)}</ul></div>
  ${V.experiment?`<div class="card full"><h2>Recommended next experiment</h2><p style="margin:0 0 12px;font-weight:600">${rich(V.experiment.name)}</p>
    <div class="exp"><div><b>Primary metric</b>${esc(V.experiment.metric)}</div><div><b>Success target</b>${esc(V.experiment.target)}</div><div><b>Duration</b>${esc(V.experiment.duration)}</div><div><b>Owner</b>${esc(V.experiment.owner||'—')}</div></div></div>`:''}
  ${(D.meta.assumptions||[]).length?`<div class="card full"><h2>Assumptions the panel worked with</h2><ul class="clean assume">${li(D.meta.assumptions)}</ul></div>`:''}
</div>

<div class="card chat">
  <div class="chathead">
    <div style="display:flex;gap:12px;align-items:center"><div class="stack">${ORDER.map(av).join('')}</div>
    <div><div class="gname">Three Amigos · War Room</div><div class="gsub">${ORDER.map(k=>esc(P[k].name.split(' ')[0])).join(', ')} · ${msgs.length} messages</div></div></div>
    <div class="filters" id="f">
      <button class="on" data-f="all">All</button>
      ${ORDER.map(k=>`<button data-f="p:${k}">${esc(P[k].name.split(' ')[0])}</button>`).join('')}
      <button data-f="s:for">▲ For</button><button data-f="s:against">▼ Against</button><button data-f="s:conditional">◆ Conditional</button>
    </div>
  </div>
  <div class="feed" id="feed">`;
let lastRound=null;
msgs.forEach(m=>{
  if(m.round!==lastRound){const r=(D.rounds||[])[m.round-1];h+=`<div class="divider"><span>${esc(r?r.title:'Round '+m.round)}</span></div>`;lastRound=m.round;}
  const k=m.from,p=P[k],q=m.reply_to&&byId[m.reply_to];
  h+=`<div class="msg ${SIDE[k]}" data-p="${k}" data-s="${m.stance}" style="--c:${COL[k]}">
    ${av(k)}
    <div class="bubble">
      <div class="meta"><span class="who">${esc(p.name)}</span><span class="role">${esc(p.short||p.role)}</span><span class="chip s-${m.stance}">${ICON[m.stance]} ${STANCE[m.stance]}</span></div>
      ${q?`<div class="quote" style="--qc:${COL[q.from]}"><b>↩ ${esc(P[q.from].name.split(' ')[0])}:</b> ${esc(plain(q.text).slice(0,140))}</div>`:''}
      <div class="text">${paras(m.text)}</div>
      ${(m.tags||[]).length?`<div class="tags">${m.tags.map(t=>`<span>#${esc(t)}</span>`).join('')}</div>`:''}
    </div></div>`;
});
h+=`</div></div>
<div class="foot">Highlights: <mark class="pro">argument in favour</mark>   <mark class="con">argument against</mark>   <mark class="risk">risk / open question</mark></div>`;
document.getElementById('app').innerHTML=h;

document.getElementById('f').addEventListener('click',e=>{
  const b=e.target.closest('button');if(!b)return;
  document.querySelectorAll('#f button').forEach(x=>x.classList.toggle('on',x===b));
  const f=b.dataset.f;
  document.querySelectorAll('#feed .msg').forEach(el=>{
    const show=f==='all'||(f.startsWith('p:')&&el.dataset.p===f.slice(2))||(f.startsWith('s:')&&el.dataset.s===f.slice(2));
    el.classList.toggle('hidden',!show);
  });
});
})();
</script>
</body>
</html>
````
<!-- TEMPLATE END -->