# Open the viewer from Cursor

The viewer is a local web app. Rather than embed it, the integration binds a key in Cursor
that opens the **currently focused `.md`** in the viewer (in your browser), reusing the single
shared daemon. Two trigger points result — a keybinding and the command palette.

Cursor is VS Code-based, so these configs work unchanged in VS Code.

## How it avoids duplicate servers

The task calls `server.mjs <file>`, which is idempotent: it pings the daemon recorded in
`/tmp/interactive-plan-viewer.json`, **reuses it if alive**, and only spawns a new daemon
if none is running. Each keypress is just a short-lived client process (ping → register →
open browser → exit). There is never more than one server.

## Setup

1. **Task** — copy [`docs/cursor/tasks.example.json`](cursor/tasks.example.json) in via
   Command Palette → *Tasks: Open User Tasks* (merge into the existing `tasks` array if you
   have one). A user task is available in every project; use `.vscode/tasks.json` instead if
   you want it per-repo. Edit the absolute path to `server.mjs` for your machine — `~` is not
   expanded in `args`. `${file}` is the absolute path of the active editor file.

2. **Keybinding** — copy [`docs/cursor/keybindings.example.json`](cursor/keybindings.example.json)
   in via Command Palette → *Preferences: Open Keyboard Shortcuts (JSON)* (again, merge into the
   existing array). Default binding is `cmd-shift-m`, scoped to markdown files; `args` must match
   the task's `label`.

3. **Use it** — open a plan `.md` and press `cmd-shift-m`, **or** open the command palette
   (`cmd-shift-P`) → *Tasks: Run Task* → *Open in interactive-plan viewer*. The viewer opens
   (or focuses) the tab for that plan.

Run it on a non-`.md` file and `server.mjs` just prints an error and exits — harmless.

## Notes

- The reverse direction is already wired: code refs (`file.ts:123`) in the viewer open in
  Cursor via `editorCommand` in `config.json` (`cursor --goto {path}:{line}:{col}`). That
  requires the `cursor` CLI on your `PATH` — install it from Cursor's Command Palette →
  *Shell Command: Install 'cursor' command*.
- Stop the daemon with `node app/server.mjs --stop`; check it with `--status`.
- Using Zed instead? See [`zed-integration.md`](zed-integration.md).
