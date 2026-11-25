# GitHub setup plan and authentication status

## Status (checked 2026-11-25 from the Claude Code cloud session)

| Item | Status |
|------|--------|
| GitHub account | `Polik9000`, reachable through the Claude GitHub connector (API) |
| `gh` CLI in the cloud container | Its token is invalid. Not needed, because the connector is used instead. |
| Repository `Polik9000/integer-complexity-lab` | Created **public** on 2026-11-25 with the lead's approval; `main` pushed. |
| Credentials in the repository | None. No tokens, no e-mail addresses, no local user paths (checked by `git grep` before the first push). |

## Plan

1. **Create the repository** `integer-complexity-lab` under `Polik9000`. It is **public** per the
   project brief, with no auto-init, because the local history is pushed as is.
   *Needs the lead's explicit go-ahead, since public visibility can't really be undone.*
2. **Push** `main` (the initial commit). From then on, use branches and PRs.
3. **Settings** (the lead does these on github.com, ~2 min):
   - Settings → Branches → add a rule for `main`: require a pull request and require status
     checks (`ci`) to pass. Optional at first, but recommended once CI is green.
   - Settings → General: enable "Automatically delete head branches".
   - Leave Actions enabled (needed for CI). Fork PR workflows need approval (the default).
4. **Attach the repository to the Claude project**, so future Claude Code sessions get it:
   Project settings → Resources → add `Polik9000/integer-complexity-lab`.
5. **Optional:** a short repository description and the topics `integer-complexity`,
   `number-theory`, `lean4` and `experimental-mathematics`.

## Never in the repository

Tokens, API keys, `.env` files, personal e-mail addresses and private correspondence.
`.gitignore` excludes the common credential files. If something leaks, rotate the
credential first, then ask the lead before rewriting any history.
