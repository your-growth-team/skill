# Setup guide (installs and accounts, with links)

Give these as numbered plain-text steps, one small group at a time, and always include the link. After each install, give the check command. Install commands and requirements change — if you can browse, confirm on the official page; otherwise tell them to follow the official page if anything differs.

Explain "terminal" the first time: a text window where you type commands to the computer. Mac: open Spotlight (Cmd+Space), type "Terminal". Windows: open "Terminal" or "PowerShell" from the Start menu.

## Mac

| # | Tool | What it's for | Link / command | Check it worked |
| --- | --- | --- | --- | --- |
| 1 | Xcode Command Line Tools | Apple's basic developer tools; includes Git (version history). | In Terminal: `xcode-select --install` | `git --version` |
| 2 | Homebrew | An app store for developer tools, run from the terminal. | https://brew.sh (copy the install command on that page) | `brew --version` |
| 3 | Node.js (LTS version) | Runs JavaScript/TypeScript tools on the computer; Expo and Next.js need it. | https://nodejs.org (choose LTS) or `brew install node` | `node -v` and `npm -v` |
| 4 | VS Code | Code editor for reading and lightly editing files. | https://code.visualstudio.com | Opens normally |
| 5 | Claude Code | The AI coding assistant that works inside the project folder. | https://docs.claude.com/en/docs/claude-code/overview (follow the current install steps there) | `claude --version` |
| 6 | Expo Go (on the phone, mobile projects) | Previews the app live on a real phone. | https://expo.dev/go (links to App Store and Google Play) | App opens |

Optional, later:
- Xcode (full app, for iPhone simulator): https://apps.apple.com/app/xcode/id497799835 — large download; not needed while Expo Go works.
- Android Studio (Android emulator): https://developer.android.com/studio
- GitHub Desktop (visual alternative to Git commands): https://desktop.github.com

## Windows

| # | Tool | What it's for | Link | Check it worked |
| --- | --- | --- | --- | --- |
| 1 | Git for Windows | Version history. | https://git-scm.com/downloads | `git --version` |
| 2 | Node.js (LTS) | Runs the project's tools. | https://nodejs.org | `node -v` |
| 3 | VS Code | Code editor. | https://code.visualstudio.com | Opens normally |
| 4 | Claude Code | AI coding assistant in the project folder. | https://docs.claude.com/en/docs/claude-code/overview (check its current Windows instructions) | `claude --version` |
| 5 | Expo Go (on the phone) | Live app preview. | https://expo.dev/go | App opens |

Note for Windows users building for iPhone: Expo Go and EAS cloud builds mean they don't need a Mac to develop and ship, but some iOS debugging is easier on a Mac. Mention this only if iOS matters to them.

## Useful VS Code extensions

Install from the Extensions panel in VS Code (search by name): ESLint, Prettier, and the Expo Tools extension for mobile projects.

## Accounts

| Account | When | Link |
| --- | --- | --- |
| GitHub | Phase 1 | https://github.com/signup |
| Expo (mobile) | Phase 1 | https://expo.dev/signup |
| Supabase (backend) | Phase 3 (or Phase 1 if deciding the region now) | https://supabase.com/dashboard |
| Vercel or Netlify (web hosting) | Phase 2 | https://vercel.com/signup or https://app.netlify.com/signup |
| Apple Developer Program | Phase 5 — paid yearly, verify current price | https://developer.apple.com/programs/ |
| Google Play Console | Phase 5 — one-time fee, verify current price | https://play.google.com/console |

## Common first errors (explain in plain language)

- `command not found` → the tool isn't installed, or the terminal was opened before installing. Close and reopen the terminal, then check again.
- Permission errors with `npm install -g` on Mac → don't use `sudo`; installing Node via Homebrew usually avoids this.
- Phone can't connect to Expo → phone and computer must be on the same Wi-Fi; or start with the tunnel option (`npx expo start --tunnel`).
