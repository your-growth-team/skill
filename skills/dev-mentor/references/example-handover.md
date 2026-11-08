# Mobile App Build: Handover & Plan

As of 2026-10-04

## How to use this doc

Paste this whole document into a new Claude chat, then send: "Read this handover. Act as my mentor for building this mobile app. Confirm you understand the decisions already made, then continue from the Next step section. Go one decision at a time, explain in plain language, and keep each reply short."

The new session should treat the Decisions section as settled unless the user reopens them, and should not redo the roadmap.

## Context and goal

The user is a product manager with a basic grasp of technology and no engineering background. They want to build one mobile app that runs on both Android and iOS, using AI to write most of the code.

- **Product readiness:** product documentation (PRDs, as Markdown files) and UI designs are already prepared. The app's own features are intentionally not covered in this handover.
- **Where the PRDs live now:** attached to a Claude project in Claude chat, not yet in a repo. They need exporting into the repo (see step 9).
- **Computer:** a Mac.
- **Who codes:** the user, with AI help (Claude Code).
- **What they asked for:** an end-to-end roadmap, then guidance one decision at a time, starting with Phase 1 (foundations: tech stack, device setup, GitHub, file structure, architecture).

## Decisions made so far

| Decision | Choice | Why |
| --- | --- | --- |
| Mobile framework | React Native with Expo, in TypeScript | One codebase for Android and iOS, live preview on a phone via Expo Go, cloud builds (EAS), and the strongest AI coding support. Flutter and fully native were considered and rejected. |
| Backend | Supabase (PostgreSQL, login, file storage, real-time included) | The app stores structured data from user actions, which fits a relational database. Managed service, no lock-in, AI-friendly SQL. Firebase and custom AWS were considered. |
| Data hosting region | Supabase South Asia (Mumbai, ap-south-1) | The user prefers data stored in India. The region is chosen at project creation and is hard to change later. Supabase's official regions page lists it as available. |
| AWS | Not needed now | Only worth revisiting for special compliance, data residency or scale needs. |
| Compliance | Not yet reviewed | If the app handles sensitive data (financial, health), the user should check India's DPDP Act with a lawyer. Claude is not a lawyer. |
| PRD location | Move PRDs into the GitHub repo (`docs/` folder) | Claude Code can only read files on the user's computer, not files attached to a Claude chat project. Keep the repo private. Once coding starts, edit PRDs in the repo only, so there is one source of truth. |
| GStack (Garry Tan's open-source Claude Code skill pack) | Not now; try it when building the first feature slice | It adds planning, review and QA roles on top of Claude Code. It does not change the stack. Its performance claims come from its author, and some skills may suit web apps more than mobile. Keep it only if it helps. |

Before adopting GStack, check its current GitHub README (github.com/garrytan/gstack), since it changes quickly.

## End-to-end roadmap

Six phases, in order. The user is currently at the start of Phase 1.

1. **Foundations:** decide the tech stack, set up the Mac and phone, set up GitHub and the repo structure, choose the app architecture.
2. **Project skeleton:** create the app, run "hello world" on both platforms, set up dev / staging / production environments, add basic automatic checks (CI) on every code change.
3. **Backend and services:** configure Supabase (database, login, file storage), push notifications, analytics, crash reporting.
4. **Build:** design system and navigation shell, then features as thin end-to-end slices in sprints, with testing throughout.
5. **Release prep:** Apple Developer account (about $99 per year) and Google Play account ($25 one-time), beta testing through TestFlight and Play Internal Testing, privacy policy, store listings and screenshots.
6. **Launch and iterate:** store review and submission, monitoring, user feedback, update cycles.

## Steps before the first line of code

The user will execute setup later, so none of these are done yet except the decisions marked as made.

| # | Step | What it is | Status |
| --- | --- | --- | --- |
| 1 | Install tools | Xcode command line tools (includes Git), Homebrew, Node.js, VS Code, Claude Code, and Expo Go on the phone. | To do |
| 2 | Create accounts | GitHub and Expo now. Apple and Google developer accounts wait until launch. | To do |
| 3 | GitHub repo | One private repository for the whole app, with a README and a Node `.gitignore`. | To do |
| 4 | Branching rules | A protected `main` branch that always works, and a short-lived branch per feature merged through pull requests. | To do |
| 5 | App architecture | Recommended: feature-based structure (a folder per feature holding its own screens, logic and data calls). | Next |
| 6 | Folder structure | The concrete layout that follows from step 5, including shared components, theme and config. | To do |
| 7 | Backend choice | Supabase in Mumbai. | Decided |
| 8 | Environments | Separate dev, staging and production so testing never touches real users. | To do |
| 9 | Organize product docs | Export the PRDs from the Claude project and put them in the repo (for example a `docs/` folder in Markdown) so Claude Code can read them while coding. Add an index to `CLAUDE.md` saying which PRD covers which feature. | To do |
| 10 | Organize UI designs | Export screens and assets, and note design tokens (colors, fonts, spacing). If the designs are in Figma, connect it directly. | To do |
| 11 | AI context file | A short `CLAUDE.md` stating the stack, architecture rules and conventions so the AI stays consistent. | To do |
| 12 | Slice the product | Break the scope into small shippable features and order them. Slice one is the thinnest end-to-end flow. | To do |
| 13 | Create the Expo project | Start it with TypeScript and the folder structure from step 6. | To do |
| 14 | Run it on the phone | Confirm "hello world" works through Expo Go. | To do |
| 15 | First commit and push | Send the first version to GitHub. | To do |
| 16 | Build slice one | Real coding begins. | To do |

Steps 5 to 8 are the decisions that are costly to change later, so they come first.

## Next step and open questions

**Continue with step 5, the app architecture.** Explain the recommended feature-based structure, check it against the user's product docs, then move to step 6 (folder structure), step 8 (environments), and the GitHub setup in steps 3 and 4.

Open questions to ask the user when relevant:

- What are the main features and screens in the product docs? This confirms the feature-based architecture fits and shapes the folder layout.
- Does the app need real-time features, payments, push notifications or file uploads? Each affects the Supabase setup and extra services.
- Is the data sensitive (financial, health, children's)? If so, a legal check on India's DPDP Act is advisable before launch.
- Are the UI designs in Figma? If so, the Figma connector can feed them to the AI during the build.
- Will anyone else join the repo later? That affects branching and review rules.

## Discussion summary and working style

The conversation ran in this order: roadmap and Phase 1 outline, tech stack (Expo chosen), Mac setup guide, the 16 pre-coding steps, whether AWS is needed (no), storage needs (structured data, so Supabase), hosting region (Mumbai), a review of GStack (later, not now), and where to keep the PRDs (in the repo, not the chat project).

How the user likes to work:

- One decision at a time, with a short explanation and a clear recommendation, then they confirm or challenge it.
- Plain language. They are a product manager, not an engineer, so define jargon briefly.
- Concise replies, since they often read on a phone.
- They will run the setup steps later, so explain first and execute when they say so.
- Verify facts that may have changed (services, regions, pricing) before stating them.
