# YPG Skills

Four free Claude skills for product people, founders and designers, built by [Your Growth Team](https://github.com/your-growth-team).

A **skill** is a folder of instructions that teaches Claude how to do one job properly. Install it once, then ask for the job in plain English. Each skill below ends in something you can open, share or act on, not a wall of chat text.

| Skill | One-line job | You give it | You get back |
|---|---|---|---|
| [**Three Amigos**](skills/three-amigos) | Stress-test a product idea before you build it | A feature idea or hypothesis | A visual debate between a Business Head, Tech Head and Product & UX Head, with a verdict and next experiment |
| [**Dark Pattern Auditor**](skills/dark-pattern-auditor) | Check a site, app or Figma file against India's CCPA dark-pattern rules | A URL, screenshots or a Figma link | An interactive report: each problem marked on the screen, severity, likely legal exposure, and a compliant fix |
| [**CRO Auditor**](skills/cro-auditor) | Audit an e-commerce product page the way a CRO agency would | Product URL + mobile and desktop screenshots | A before/after prototype of the improved page, every change numbered and explained, plus an image brief |
| [**Dev Mentor**](skills/dev-mentor) | Coach a non-technical person from idea to a launched app | Your idea (and PRDs/designs if you have them) | Step-by-step guidance, one decision at a time, with handover files to keep chats short |

---

## Install in 2 minutes

Pick the one that matches how you use Claude.

### Option A: Claude app (claude.ai or desktop). Easiest.

1. Go to the [**Releases**](../../releases/latest) page of this repo.
2. Download the `.skill` file(s) you want, for example `three-amigos.skill`.
3. In Claude, open **Settings → Skills** (menu names change over time, so search "Skills" in Settings) and upload the file.
4. Switch the skill on. Start a new chat and ask for the job (examples below).

> Skills need a Claude plan that supports them, with code execution / file creation turned on. Check the current requirements in Anthropic's [support docs](https://support.claude.com).

### Option B: Claude Code

Copy the skill folder into your skills directory:

```bash
git clone https://github.com/your-growth-team/skill.git
cp -r skill/skills/three-amigos ~/.claude/skills/        # available in every project
# or, for one project only:
cp -r skill/skills/three-amigos .claude/skills/
```

Restart Claude Code. The skill loads automatically when your request matches it.

### Option C: Just read them

Every skill is plain Markdown. Open `skills/<name>/SKILL.md` to see exactly how it thinks.

---

## How to use each skill

### 🧑‍🤝‍🧑 Three Amigos

**Use it when:** you have a feature idea or hypothesis and want it challenged before anyone writes code.

**Say something like:**
> Use Three Amigos on this: add a "save for later" wishlist to my fragrance app so first-time buyers come back. Users are in India, revenue is from product sales.

**What happens:** it checks your idea has enough detail (and asks up to 4 quick multiple-choice questions if not), then three senior personas argue it out over three rounds (opening positions, cross-examination, closing vote). You get one page: a verdict (Go / Go with conditions / Validate first / Pivot), each person's score, where they agreed and disagreed, kill criteria, the cheapest next experiment, and the full debate as a filterable group chat.

**Best with:** Claude Code or Cowork, where the three personas run as separate parallel agents. In a plain chat it still works, but the debate is simulated in one session (it tells you so).

### 🛡️ Dark Pattern Auditor

**Use it when:** you want a checkout, paywall, onboarding, consent or cancellation flow checked for manipulative design before it becomes a regulatory problem.

**Say something like:**
> Audit https://your-site.com for dark patterns under the CCPA guidelines. Focus on checkout and cancellation.

or share a `figma.com` link, or upload screenshots.

**What happens:** it captures the flows, checks all **13 patterns** named in India's 2023 CCPA Guidelines (false urgency, basket sneaking, confirm shaming, forced action, subscription trap, interface interference, bait and switch, drip pricing, disguised ads, nagging, trick questions, SaaS billing, rogue malware), scores each finding, and builds an interactive HTML report. Problems are outlined on recreated screens, with a switch to a compliant version, fix copy, and acceptance criteria your developers can test. A coverage table shows what was found, cleared, or could not be verified.

**Good to know:** it never completes a payment, starts a paid trial or submits real personal data. It flags risk in careful language ("likely to be treated as…"). **It is not legal advice.**

### 📈 CRO Auditor

**Use it when:** a product page is getting traffic but not enough add-to-carts, and you want a specialist's teardown plus a proposed redesign.

**Say something like:** (attach full-scroll **mobile and desktop** screenshots)
> CRO audit this product page: https://your-store.com/products/example

**What happens:** it first checks it has screenshots for both devices (and asks for the missing one if not), then audits the page through the shopper's doubts (*Is it for me? Why this one? Why believe it? Is it worth it? Can I buy easily?*). The output is one HTML report with a Mobile/Desktop switch, **Before / After / Compare** views, a "Highlight changes" toggle that numbers and explains every change (what, why, which metric it should move), a printable summary, and an image brief for each gallery shot.

**Good to know:** it never reuses your product photos (it uses numbered placeholders and writes a shoot brief), never invents reviews or numbers, and keeps legal text intact. Drop-off causes are labelled as hypotheses unless you give it analytics data. It is strongest for repeat-purchase DTC categories such as skincare, supplements, food and fragrance, and says so when a category is extrapolated.

### 🧭 Dev Mentor

**Use it when:** you're not an engineer but want to build a real mobile app or website with AI writing the code, and don't know what to do next.

**Say something like:**
> Use Dev Mentor. I'm a PM, not technical. I want to build an app for iPhone and Android. I have PRDs and Figma designs. Where do I start?

**What happens:** it asks a few questions, shows a six-phase roadmap (foundations → project skeleton → backend → build → release prep → launch), then walks you through **one decision at a time** in plain language, with official links for every tool or account. When a chat gets long it offers a **handover file**; start a new chat, attach the file and say *"Use Dev Mentor. Read this handover and continue from the Next step."*

**Works best inside a Claude Project**, so your PRDs and the latest handover live in one place.

---

## What each skill needs

"Connectors" are apps you connect to Claude (Settings → Connectors). "Environment" is what must exist where Claude runs the skill. Everything marked optional makes the skill better but is never a blocker.

| Skill | Connectors: required | Connectors: optional | Environment |
|---|---|---|---|
| **Three Amigos** | None | Docs/files connectors (Google Drive, Notion, ClickUp, Figma) so the panel can read your PRDs and research as evidence | Subagents for true parallel debate (Claude Code / Cowork); otherwise it simulates. Artifact publishing or file sending to deliver the page. Playwright for the pre-publish screenshot check (optional). |
| **Dark Pattern Auditor** | None for public URLs. **Figma** if you audit a Figma link | **Figma** (read frames; write findings back as annotations if you ask). A ticket tracker such as **ClickUp**, Jira or Linear if you want one ticket per finding. | Python 3 + Playwright + Chromium for live capture (`pip install playwright && playwright install chromium`), or the Claude in Chrome extension. In plain claude.ai it falls back to fetching page text and asks you for screenshots of flows it can't reach. |
| **CRO Auditor** | None | Web search for the optional competitor scan. Analytics/heatmap exports (e.g. Microsoft Clarity, GA) as files or via a connector, to turn hypotheses into evidence. | Web fetch for the page copy. Python 3 + Pillow (screenshot cropping and palette sampling) and Playwright + Chromium (visual QA of the report). Needs your **mobile and desktop screenshots**. |
| **Dev Mentor** | None | **Figma, Notion, ClickUp, Google Drive**: so it can read your PRDs and designs before recommending anything. Web search to verify prices and install commands. | Nothing to install for the skill itself. File creation lets it save handover files. The tools it *recommends* (GitHub, Node.js, VS Code, Claude Code, Expo, Supabase) are walked through in its setup guide. |

**Rule of thumb:** with no connectors at all, Three Amigos, CRO Auditor and Dev Mentor run fully, and Dark Pattern Auditor runs on URLs and screenshots. Connect **Figma** to unlock Figma audits, and **Drive/Notion/ClickUp** so the skills can read your own documents.

---

## What's in this repo

```
skill/
├── README.md
├── skills/                      ← the real skill folders (Claude Code, or read the source)
│   ├── three-amigos/
│   ├── dark-pattern-auditor/
│   ├── cro-auditor/
│   └── dev-mentor/
└── dist/                        ← ready-to-upload .skill files (also attached to Releases)
```

## Limits worth knowing

- **Dark Pattern Auditor** reflects the CCPA Dark Patterns Guidelines, 2023 and the enforcement examples available when it was written. Rules and orders change, so for anything going to leadership or legal, re-check against the latest CCPA notifications. Output is a product-quality screen, not a legal opinion.
- **CRO Auditor** can only see the page, not why people leave it. Treat its drop-off explanations as hypotheses to test, and run structural suggestions (landing page vs PDP, subscription default) as A/B tests, not verdicts.
- **Three Amigos** personas are simulated points of view. Benchmarks they cite are rough estimates. Use the verdict to decide what to validate, not as proof.
- **Dev Mentor** is not a lawyer or accountant, and it will tell you to check legal, privacy and payments questions with a professional. Prices and plan limits drift; it verifies them or points you to the official page.

## Credits and licences

- The CRO Auditor bundles two design-guidance files so it can work offline: **Frontend Design** (Apache 2.0, licence in `skills/cro-auditor/bundled/frontend-design/`) and **UI/UX Pro Max** (MIT, upstream: [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)). See the `NOTICE.md` beside each.
- Everything else is by Vaastav Parikh / Your Growth Team.

## Feedback

Found a bug or want a new skill? [Open an issue](../../issues), or find us on Instagram: **@YOUR-HANDLE**.
