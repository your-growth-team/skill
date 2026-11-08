# Default recommendations

Starting points for a non-technical builder coding with AI help. Adapt to the person; when you deviate, say why in one line. Verify anything time-sensitive (prices, regions, features) before stating it.

## Why these defaults

The person is relying on AI to write most of the code, so prefer: one language across the product (TypeScript), popular tools with lots of public examples (AI writes them well), managed services over self-run servers, and free tiers for early stages.

## Decisions

| Decision | Default | Why | Consider instead when |
| --- | --- | --- | --- |
| Mobile framework | React Native with Expo, in TypeScript | One codebase for Android and iOS, live preview on a phone through Expo Go, cloud builds (EAS), strongest AI coding support. | Flutter if they already have Dart/Flutter developers; fully native (Swift/Kotlin) only for heavy device-specific features (advanced AR, intensive audio/video processing). |
| Web framework | Next.js (React) in TypeScript | Same React knowledge as Expo, huge ecosystem, simple hosting on Vercel or Netlify. | A no-code site builder for a pure marketing site; plain React (Vite) for a simple internal tool. |
| Backend | Supabase (PostgreSQL database, login, file storage, real-time) | Most products store structured data from user actions, which fits a relational database. Managed, generous free tier, standard SQL (no lock-in), AI writes SQL well. | Firebase if the team already knows it or the data is very loosely structured; a custom AWS/GCP setup only for special compliance, residency or scale needs. |
| Data hosting region | The region closest to most users, or the one required by data-residency rules | Lower latency, simpler compliance. The region is chosen when the project is created and is hard to change later — decide it deliberately. Check the provider's current regions page. | Multiple regions only at real scale. |
| Language | TypeScript everywhere | Catches many mistakes before the app runs, and AI tools produce more reliable TypeScript. | — |
| Architecture | Feature-based folders | Each feature's screens, logic and data calls live together, so the AI (and people) can change one feature without touching others. Maps neatly to PRDs. | Very small apps can stay flat at first. |
| Version control | GitHub, private repo, protected `main`, short-lived feature branches merged through pull requests | Safe history, easy rollback, works with Claude Code and CI. | — |
| Environments | dev, staging, production (separate backend projects) | Testing never touches real users or data. | Small projects can start with dev and production and add staging before beta. |
| AI coding | Claude Code working in the repo, guided by `CLAUDE.md` | It reads the actual project files and docs, unlike a chat. | — |
| Hosting (web) | Vercel or Netlify, connected to GitHub | Deploys automatically on every merge; preview links for each pull request. | — |
| Crash reporting / analytics | Sentry for crashes; a product analytics tool such as PostHog or Mixpanel | Cheap to add early, painful to retrofit. | Use the company's existing tools if they have them. |

## Things to raise, not decide

- **Compliance and privacy law:** if the product handles sensitive data, recommend checking the local law (India's DPDP Act, EU GDPR, etc.) with a lawyer. You are not a lawyer.
- **Payments:** which payment provider suits their country and product; whether app store billing rules apply. Recommend verifying with current store rules and, if needed, a professional.
- **Costs:** give rough tiers (free to start, paid as usage grows) and link to pricing pages rather than quoting numbers from memory.
