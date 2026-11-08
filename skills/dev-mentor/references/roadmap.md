# Dev Mentor roadmap (detail)

Read this when planning, when showing the person where they are, or when moving between phases. Walk through it one step at a time; never paste the whole thing at them.

## Contents
1. Phase overview
2. Pre-coding checklist (Phase 1 to start of Phase 4)
3. Mobile vs web differences
4. Phases 3 to 6 in more detail
5. Questions that change the plan

---

## 1. Phase overview

| Phase | Goal | Done when |
| --- | --- | --- |
| 1. Foundations | Make the decisions that are costly to change, and prepare tools, accounts and docs. | Stack, architecture, folder structure and environments are decided; tools installed; repo exists; docs are in the repo. |
| 2. Project skeleton | A real, empty app that runs. | "Hello world" runs on a phone (or browser), code is on GitHub, basic checks run on every change. |
| 3. Backend and services | The plumbing the features need. | Database, login and storage work in dev; notifications, analytics and crash reporting are wired if needed. |
| 4. Build | Ship features in thin end-to-end slices. | All planned slices for the first release are built and tested. |
| 5. Release prep | Ready for real users. | Store accounts (or hosting and domain), beta testing, privacy policy and listings are done. |
| 6. Launch and iterate | Live and improving. | Live in stores or online; monitoring and a feedback loop in place. |

## 2. Pre-coding checklist

Steps 5 to 8 are the expensive-to-change ones, so settle them early even if installs happen later.

| # | Step | What it is (plain language) |
| --- | --- | --- |
| 1 | Install tools | The software on their computer (and phone) needed to build. See `setup-guide.md`. |
| 2 | Create accounts | GitHub, plus Expo (mobile) or a hosting account (web). Store developer accounts wait until release. |
| 3 | GitHub repo | One private repository (project folder with history) for the whole product, with a README and a `.gitignore` (a list of files Git should ignore, such as secrets and build output). |
| 4 | Branching rules | `main` always works. Each change happens on a short-lived branch (a safe copy) and comes back via a pull request (a request to merge, which can be reviewed). Protect `main`. |
| 5 | App architecture | How the code is organised. Default: feature-based — one folder per feature holding its own screens, logic and data calls. Check it against the product's main features. |
| 6 | Folder structure | The concrete layout from step 5: features, shared components, theme, config, `docs/`. |
| 7 | Backend choice | Where data, login and files live. See `stack-defaults.md`. |
| 8 | Environments | Separate dev, staging and production copies so testing never touches real users or real data. |
| 9 | Organise product docs | Export PRDs into the repo's `docs/` folder as Markdown. Add an index to `CLAUDE.md` (which PRD covers which feature). From now on, edit PRDs in the repo only. |
| 10 | Organise UI designs | Export screens and assets; note design tokens (colours, fonts, spacing). If the designs are in Figma, connect the Figma integration so the AI can read them directly. |
| 11 | AI context file | A short `CLAUDE.md` at the repo root: the stack, architecture rules, naming conventions, how to run the app, and the docs index. Claude Code reads it automatically. |
| 12 | Slice the product | Break the scope into small shippable features and order them. Slice one is the thinnest flow that goes end to end (for example: sign up → see home screen → save one thing). |
| 13 | Create the project | Generate the app with TypeScript, then apply the folder structure from step 6. |
| 14 | Run it | "Hello world" on a real phone (Expo Go) or in the browser. |
| 15 | First commit and push | Send the first version to GitHub. |
| 16 | Build slice one | Real coding begins. |

## 3. Mobile vs web differences

| Topic | Mobile (Android/iOS) | Web |
| --- | --- | --- |
| Preview | Expo Go app on a real phone | Local browser at `localhost` |
| Builds | EAS (Expo's cloud build service) | Hosting platform builds automatically from GitHub |
| Release | App Store and Google Play review | Deploy to a hosting provider and connect a domain |
| Accounts at release | Apple Developer Program (yearly fee) and Google Play Console (one-time fee) — verify current prices | Domain name and hosting plan |
| Extra concerns | Push notifications, app permissions, store screenshots, app icons | SEO, browser compatibility, cookie consent where required |

If they want both, recommend one shared backend and decide early whether the web product is a full app or a marketing site; a marketing site can come later and separately.

## 4. Phases 3 to 6 in more detail

**Phase 3 — Backend and services**
- Create backend projects per environment (dev and production at minimum, staging if budget allows).
- Turn on login methods the PRDs need (email, phone OTP, Google, Apple — note Apple sign-in is generally required on iOS if other social logins are offered; verify current App Store rules).
- Design the first database tables from slice one's needs only. Turn on row-level security (rules about who can see which rows) from day one.
- Add crash reporting and analytics early; they're cheap to add now and painful to retrofit.
- Keep secrets (API keys) out of the repo. Explain environment variables in plain terms.

**Phase 4 — Build**
- First: design system (colours, fonts, spacing, shared buttons/inputs) and the navigation shell (tabs or menus, empty screens).
- Then one slice at a time: PRD → small prompt to Claude Code → run it → test by hand → pull request → merge.
- After each slice, check it against the PRD. Keep slices small enough to finish in a few days.
- Optional tooling (for example GStack, an open-source Claude Code skill pack adding planning/review/QA roles) can be trialled on a slice; keep it only if it helps. Check its current README first because such tools change quickly.

**Phase 5 — Release prep**
- Mobile: create store developer accounts, set up TestFlight (iOS) and Internal Testing (Android) for beta users.
- Privacy policy and terms (a professional should review if data is sensitive).
- Store listing: name, description, screenshots, icon, category, data-safety forms.

**Phase 6 — Launch and iterate**
- Submit for review; expect possible rejections and explain them calmly.
- Watch crash reports and analytics in the first weeks.
- Set an update rhythm (for example, every sprint) and a way to collect feedback.

## 5. Questions that change the plan

Ask when relevant, not all at once:
- Main features and screens? (Confirms the architecture and folder layout.)
- Real-time features, payments, push notifications, file uploads? (Each adds services and setup.)
- Sensitive data (financial, health, children's, ID documents)? (Recommend a legal check on the local data protection law before launch, e.g. India's DPDP Act, GDPR in the EU.)
- Designs in Figma? (Connect it.)
- Will others join the repo later? (Affects branching and review rules.)
- Payments: in-app digital goods on mobile usually must use Apple/Google billing; physical goods and services usually don't. Flag for verification against current store rules.
