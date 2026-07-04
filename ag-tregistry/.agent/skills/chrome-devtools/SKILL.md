---
name: chrome-devtools
version: 0.1.1
description: |
  Chrome DevTools MCP integration for browser automation, debugging, performance analysis,
  and network inspection. Provides 45 tools via the official chrome-devtools-mcp server.
  Use for UI testing, Playwright-style interactions, screenshot capture, console/network
  debugging, performance traces, and heap memory analysis. External npm package — not bundled.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [qa-agent, design-agent, swe]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Chrome DevTools

Official Chrome DevTools MCP server (`chrome-devtools-mcp`) exposing 45 tools over stdio.
Connects to Chrome via CDP. Works headless or headed, with existing Chrome instances or fresh ones.

## Setup

Add to `.agent-config.json` in the target repo:

```json
{
  "mcps": [
    {
      "name": "chrome-devtools",
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  ]
}
```

Then run:

```bash
npx agent-architecture install
```

Requires Node.js LTS and Chrome (current stable or newer).

### Connect to existing Chrome instance

```json
"args": ["-y", "chrome-devtools-mcp@latest", "--browser-url", "http://localhost:9222"]
```

### Headless mode

```json
"args": ["-y", "chrome-devtools-mcp@latest", "--headless"]
```

## Workflow

1. Open a page with `new_page` or `navigate_page`.
2. Interact using input tools (`click`, `fill`, `press_key`).
3. Assert state via `get_console_message`, `list_network_requests`, or `take_screenshot`.
4. Run `performance_start_trace` / `performance_stop_trace` / `performance_analyze_insight` for perf.
5. Use `lighthouse_audit` for accessibility and best-practice scoring.
6. Close pages with `close_page` when done.

## Tools

### Navigation
- `new_page()` — open a new browser tab
- `navigate_page(url)` — navigate current page to URL
- `list_pages()` — list open tabs
- `select_page(page_id)` — switch active tab
- `close_page(page_id)` — close a tab
- `wait_for(selector_or_condition)` — wait for element or network idle

### Input Automation
- `click(selector)` — click element
- `click_at(x, y)` — click at coordinates
- `fill(selector, value)` — fill input field
- `fill_form(fields)` — fill multiple fields
- `type_text(text)` — type text at cursor
- `press_key(key)` — keyboard press (e.g. `Enter`, `Tab`)
- `hover(selector)` — hover over element
- `drag(source, target)` — drag and drop
- `upload_file(selector, path)` — upload file via input
- `handle_dialog(action, text)` — accept/dismiss alerts

### Screenshots & Snapshots
- `take_screenshot()` — capture full page screenshot
- `take_snapshot()` — capture DOM accessibility snapshot

### Emulation
- `emulate(device)` — emulate mobile device
- `resize_page(width, height)` — resize viewport

### Debugging
- `evaluate_script(expression)` — run JS in page context
- `get_console_message(index)` — get single console entry
- `list_console_messages()` — list all console output
- `lighthouse_audit(url, categories)` — run Lighthouse audit

### Screencast
- `screencast_start()` — begin live page capture
- `screencast_stop()` — stop capture

### Network
- `list_network_requests()` — list all captured network requests
- `get_network_request(id)` — get details of a single request

### Performance
- `performance_start_trace(categories)` — start Chrome trace
- `performance_stop_trace()` — stop trace and collect data
- `performance_analyze_insight(trace)` — analyze trace for bottlenecks

### Memory
- Heap snapshot capture and analysis tools — use for memory leak investigation

### Extensions
- `install_extension(path)`, `list_extensions()`, `reload_extension(id)`,
  `trigger_extension_action(id)`, `uninstall_extension(id)`

## Common Patterns

**Playwright-style test flow:**
```
new_page → navigate_page(url) → fill(selector, value) → click(submit) →
wait_for(success_selector) → take_screenshot → close_page
```

**Debug failing request:**
```
navigate_page(url) → list_network_requests → get_network_request(id)
```

**Performance audit:**
```
navigate_page(url) → performance_start_trace → [interact] →
performance_stop_trace → performance_analyze_insight
```

**Accessibility check:**
```
navigate_page(url) → lighthouse_audit(url, categories=["accessibility"])
```

## Allowed Use

- Browser UI testing and interaction automation.
- Screenshot capture for visual regression and design review.
- Console and network debugging during development.
- Performance tracing and Lighthouse audits.
- Heap snapshot analysis for memory leaks.

## Prohibited Use

- Do not use `upload_file` to read or exfiltrate local file contents.
- Do not navigate to URLs outside the approved test scope.
- Do not persist browser sessions or cookies between unrelated tasks.
- Do not install browser extensions in shared or production Chrome instances.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
