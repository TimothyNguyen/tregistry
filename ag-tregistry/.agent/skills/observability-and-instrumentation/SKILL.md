---
name: observability-and-instrumentation
version: 0.1.0
description: |
  Add structured observability to code and agent outputs: tracing, structured logging,
  metrics, and AG-UI-compatible event emission. Prevents silent failures in production.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [swe, cloud, qa-agent]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Observability and Instrumentation

Add structured observability to code and agent outputs so failures are visible, diagnosable, and traceable without SSH access.

## When to Use

Invoke when:
- Adding a new service, endpoint, or agent tool
- A production failure was diagnosed by reading logs manually
- An agent output is consumed by a downstream system
- A background job or migration runs without progress reporting

## Instrumentation Patterns

### Structured Logging

Log at structured key-value pairs, not free-text strings.

**Do:**
```js
logger.info('user.created', { userId, email: redact(email), source });
```

**Don't:**
```js
console.log(`Created user ${email} from ${source}`);
```

Log levels:

| Level | When |
|-------|------|
| `error` | Unrecoverable failure — requires human action |
| `warn` | Recoverable anomaly — should be reviewed |
| `info` | Business event — user action, state change, integration call |
| `debug` | Implementation detail — disabled in prod by default |

Rules:
- Never log credentials, session tokens, PII, or full prompt/response text
- Include a correlation ID (`requestId`, `traceId`) on every log line
- Log at entry and exit of every external call (HTTP, DB, MCP tool)

### Tracing

Wrap external calls in a span:

```js
const span = tracer.startSpan('db.query', { attributes: { 'db.table': 'users', 'db.op': 'select' } });
try {
  const result = await db.query(sql, params);
  span.setStatus({ code: SpanStatusCode.OK });
  return result;
} catch (err) {
  span.recordException(err);
  span.setStatus({ code: SpanStatusCode.ERROR });
  throw err;
} finally {
  span.end();
}
```

Minimum spans:
- Each HTTP call out
- Each DB query
- Each MCP tool invocation
- Each agent sub-task dispatch

### Metrics

Define counters and histograms at module init, not inline:

```js
const requestCounter = meter.createCounter('http.requests', { description: 'Total HTTP requests by route and status' });
const latencyHistogram = meter.createHistogram('http.latency_ms', { description: 'Request latency in ms' });
```

Record at the exit point:

```js
requestCounter.add(1, { route: '/users', status: res.statusCode });
latencyHistogram.record(Date.now() - startMs, { route: '/users' });
```

### Agent Output Events (AG-UI Compatible)

When an agent produces output consumed by another system, emit structured events:

```js
emit({ type: 'tool.result', toolName: 'search', status: 'success', resultCount: hits.length, latencyMs });
emit({ type: 'tool.error', toolName: 'search', error: err.message, retryable: true });
```

Event fields:
- `type` — dot-namespaced string: `<domain>.<event>`
- `status` — `success` | `error` | `partial`
- No raw data, credentials, or full prompt text in event payload

## Review Checklist

Before shipping instrumented code:

- [ ] Every external call has entry/exit log lines with correlation ID
- [ ] No credentials, tokens, PII, or full prompt text in any log/event
- [ ] Error path logs include `error.message` and relevant context (not just `"failed"`)
- [ ] Metrics counters and histograms initialized once at module level
- [ ] Agent output events follow `<domain>.<event>` naming
- [ ] Debug logs are off by default in production config

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
