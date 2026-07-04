---
name: atlassian-docs
version: 0.2.1
description: |
  Atlassian MCP integration for Jira, Confluence, and Bitbucket. Provides read and write
  access to all three services through bundled FastMCP 3 servers. Use for product
  documentation lookup, issue management, sprint tracking, wiki authoring, repository
  operations, and PR workflows. Do not use for credential setup, OAuth setup, or
  public web browsing outside approved Atlassian hosts.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
agents: [spec-agent, pm, qa-agent, interviewer, swe]
---

## Enterprise Preamble

- Stay inside the current project unless the user explicitly names another path.
- Do not call public telemetry, public update checks, public tunnels, cookie import, or public scraping flows.
- Use policy-gated tools only when the active profile allows them.
- Commit after each discrete behavior change — do not accumulate unrelated edits across multiple files before committing.
- Each commit message must follow Conventional Commits: `<type>[scope]: <description>` (types: feat, fix, docs, refactor, test, chore, perf, ci).
- Never use `--no-verify`, `--force` (use `--force-with-lease`), or `--no-gpg-sign` unless explicitly instructed.
- Sequence for rebasing: stage → commit → fetch → rebase → push.

# Atlassian Docs

Three bundled FastMCP 3 servers expose Jira, Confluence, and Bitbucket over stdio.
Install once, configure via environment variables, run per-service.

Do not vendor or import `mcp-atlassian` into `codebase-engine`. The bundled servers
replace the generic `mcp-atlassian` connector. Treat external Atlassian egress as
explicitly policy-gated.

Source lives in `atlassian-docs/mcp/`. See `atlassian-docs/mcp/README.md` for
setup and MCP client config examples.

## Setup

```bash
cd atlassian-docs/mcp
pip install -e .
```

Start each server independently:

```bash
mcp-jira        # Jira MCP server
mcp-confluence  # Confluence MCP server
mcp-bitbucket   # Bitbucket MCP server
```

## Workflow

1. Read local code, docs, and `codebase-engine` output first when they can answer the question.
2. Use Atlassian tools when the user needs product context, requirements, Jira issue detail,
   Confluence docs, or Bitbucket repository state not available locally.
3. Confirm the target server is running and env vars are set before calling tools.
4. Scope every query to a named project key, issue key, space, repo slug, or page title.
5. Prefer `detail='summary'` (default) for lists; use `detail='full'` only when raw fields are needed.
6. Retrieve only the minimum required pages, issues, or commits.
7. Cite page titles, issue keys, URLs, or file paths in every response.

## Jira MCP Tools

Server: `mcp-jira` | Config prefix: `JIRA_MCP_*`

**Health**
- `jira_health_check()` — verify connectivity and auth

**Issues**
- `jira_issue_create(project, summary, issue_type, description, priority, assignee, labels, due_date, custom_fields)`
- `jira_issue_update(issue_key, summary, description, priority, assignee, labels, due_date, custom_fields)`
- `jira_issue_get(issue_key, detail)` — `detail='summary'|'full'`
- `jira_issue_delete(issue_key, delete_subtasks)`
- `jira_issue_link(link_type, inward_issue, outward_issue)`
- `jira_subtask_create(parent_key, summary, description, priority, assignee, labels, due_date)`
- `jira_project_get_schema(project, issue_type)` — debug custom fields

**Search**
- `jira_search_issues(project, assignee, status, priority, labels, created_after, created_before, updated_after, updated_before, max_results, start_at, detail)`
- `jira_search_jql(jql, max_results, start_at, detail)`

**Filters**
- `jira_filter_create(name, jql, description, favourite)`
- `jira_filter_list()`
- `jira_filter_get(filter_id)`
- `jira_filter_execute(filter_id, max_results, start_at, detail)`
- `jira_filter_update(filter_id, name, jql, description, favourite)`
- `jira_filter_delete(filter_id)`

**Workflow**
- `jira_workflow_get_transitions(issue_key)`
- `jira_workflow_transition(issue_key, transition_id, fields)`

**Comments**
- `jira_comment_add(issue_key, body)`
- `jira_comment_list(issue_key, detail)`
- `jira_comment_update(issue_key, comment_id, body)`
- `jira_comment_delete(issue_key, comment_id)`

**Projects**
- `jira_project_list(detail)`
- `jira_project_get(project_key, detail)`
- `jira_project_issue_types(project_key)`

**Boards & Sprints**
- `jira_board_list(project_key)`
- `jira_board_get(board_id, detail)`
- `jira_sprint_list(board_id, state)` — state: `active|closed|future`
- `jira_sprint_get(sprint_id, detail)`
- `jira_sprint_issues(sprint_id, max_results, start_at, detail)`
- `jira_sprint_add_issues(sprint_id, issue_keys)`
- `jira_sprint_remove_issues(issue_keys)`

**Users**
- `jira_user_search(query, max_results, detail)`
- `jira_user_get(username, detail)`
- `jira_user_myself(detail)`

**Attachments**
- `jira_attachment_add(issue_key, file_path, filename)`
- `jira_attachment_get(attachment_id)`
- `jira_attachment_delete(attachment_id)`
- `jira_attachment_download(attachment_id, max_size)`

**Worklogs**
- `jira_worklog_add(issue_key, time_spent, comment, started)` — time_spent e.g. `"2h"`, `"30m"`, `"1d"`
- `jira_worklog_list(issue_key)`
- `jira_worklog_delete(issue_key, worklog_id)`

**Metadata**
- `jira_priority_list()`
- `jira_status_list()`

## Confluence MCP Tools

Server: `mcp-confluence` | Config prefix: `CONFLUENCE_MCP_*`

**Health**
- `confluence_health_check()`

**Pages**
- `confluence_page_get(page_id, detail)`
- `confluence_page_get_by_title(space_key, title, detail)`
- `confluence_page_create(space_key, title, body, parent_id)` — body in storage format (XHTML)
- `confluence_page_update(page_id, title, body, version)` — version required for optimistic locking
- `confluence_page_delete(page_id)`
- `confluence_page_move(page_id, target_id, position)` — position: `append|before|after`
- `confluence_page_copy(page_id, destination_space, title)`
- `confluence_page_children(page_id, limit, start, detail)`
- `confluence_page_ancestors(page_id, detail)`
- `confluence_page_history(page_id)`
- `confluence_page_version(page_id, version)`
- `confluence_page_restore(page_id, version, message)`

**Search**
- `confluence_search_cql(cql, limit, start, detail)` — CQL query language
- `confluence_search(query, space_key, content_type, limit, start, detail)` — text search

**Spaces**
- `confluence_space_list(limit, start, detail)`
- `confluence_space_get(space_key, detail)`
- `confluence_space_create(key, name, description)`
- `confluence_space_pages(space_key, limit, start, detail)`

**Comments**
- `confluence_comment_add(page_id, body)`
- `confluence_comment_list(page_id, limit, start, detail)`
- `confluence_comment_update(comment_id, body, version)`
- `confluence_comment_delete(comment_id)`

**Attachments**
- `confluence_attachment_add(page_id, file_path, filename)`
- `confluence_attachment_list(page_id, limit, start, detail)`
- `confluence_attachment_get(attachment_id, detail)`
- `confluence_attachment_delete(attachment_id)`
- `confluence_attachment_download(attachment_id, max_size)`

**Labels**
- `confluence_label_add(page_id, label)`
- `confluence_label_remove(page_id, label)`
- `confluence_label_get(page_id, detail)`

**Blog Posts**
- `confluence_blog_create(space_key, title, body)`
- `confluence_blog_list(space_key, limit, start, detail)`
- `confluence_blog_get(blog_id, detail)`
- `confluence_blog_update(blog_id, title, body, version)`
- `confluence_blog_delete(blog_id)`

**Permissions**
- `confluence_permissions_get(page_id)`
- `confluence_permissions_set(page_id, restrictions)`

**Content Utilities**
- `confluence_content_convert(value, from_repr, to_repr)` — convert between `storage|editor|wiki|view`
- `confluence_content_from_markdown(markdown)` — convert markdown → Confluence storage XHTML
- `confluence_macro_render(macro_name, parameters, body, body_type)` — render any macro as storage XHTML

**Users**
- `confluence_user_get(account_id, detail)`
- `confluence_user_current(detail)`

## Bitbucket MCP Tools

Server: `mcp-bitbucket` | Config prefix: `BITBUCKET_MCP_*`

**Health**
- `bitbucket_health_check()`

**Projects**
- `bitbucket_project_list(limit, start, detail)`
- `bitbucket_project_get(project_key, detail)`
- `bitbucket_project_create(key, name, description)`

**Repositories**
- `bitbucket_repo_list(project, limit, start, detail)`
- `bitbucket_repo_get(project, repo, detail)`
- `bitbucket_repo_create(project, name, description)`
- `bitbucket_repo_delete(project, repo)`
- `bitbucket_repo_fork(project, repo, name)`

**Branches**
- `bitbucket_branch_list(project, repo, limit, start, detail)`
- `bitbucket_branch_create(project, repo, name, start_point)`
- `bitbucket_branch_delete(project, repo, name)`
- `bitbucket_branch_default(project, repo, detail)`

**Commits**
- `bitbucket_commit_list(project, repo, branch, limit, start, detail)`
- `bitbucket_commit_get(project, repo, commit_id, detail)`
- `bitbucket_commit_diff(project, repo, commit_id)`

**Pull Requests**
- `bitbucket_pr_list(project, repo, state, limit, start, detail)` — state: `OPEN|MERGED|DECLINED|ALL`
- `bitbucket_pr_get(project, repo, pr_id, detail)`
- `bitbucket_pr_create(project, repo, title, source_branch, target_branch, description, reviewers)`
- `bitbucket_pr_update(project, repo, pr_id, title, description)`
- `bitbucket_pr_merge(project, repo, pr_id, message)`
- `bitbucket_pr_decline(project, repo, pr_id)`
- `bitbucket_pr_reopen(project, repo, pr_id)`
- `bitbucket_pr_diff(project, repo, pr_id)`
- `bitbucket_pr_commits(project, repo, pr_id, detail)`
- `bitbucket_pr_activities(project, repo, pr_id)`

**PR Comments**
- `bitbucket_pr_comment_add(project, repo, pr_id, text, file_path, line)` — supports inline comments
- `bitbucket_pr_comment_list(project, repo, pr_id, detail)`
- `bitbucket_pr_comment_update(project, repo, pr_id, comment_id, text)`
- `bitbucket_pr_comment_delete(project, repo, pr_id, comment_id)`

**PR Reviews**
- `bitbucket_pr_approve(project, repo, pr_id)`
- `bitbucket_pr_unapprove(project, repo, pr_id)`
- `bitbucket_pr_needs_work(project, repo, pr_id)` — Data Center only

**PR Reviewers**
- `bitbucket_pr_reviewer_list(project, repo, pr_id)`
- `bitbucket_pr_reviewer_add(project, repo, pr_id, username)`
- `bitbucket_pr_reviewer_remove(project, repo, pr_id, username)`

**Files**
- `bitbucket_file_browse(project, repo, path, at)` — browse directory tree
- `bitbucket_file_content(project, repo, path, at)` — get file content

**Tags**
- `bitbucket_tag_list(project, repo, limit, start, detail)`
- `bitbucket_tag_create(project, repo, name, target, message)`
- `bitbucket_tag_delete(project, repo, name)`

**Webhooks**
- `bitbucket_webhook_list(project, repo)`
- `bitbucket_webhook_create(project, repo, name, url, events)`
- `bitbucket_webhook_delete(project, repo, webhook_id)`

**Build Status**
- `bitbucket_build_status_get(commit_id)`
- `bitbucket_build_status_set(commit_id, state, key, url, description)` — state: `SUCCESSFUL|FAILED|INPROGRESS`

**Diff**
- `bitbucket_diff(project, repo, from_ref, to_ref)`

## Common Patterns

**detail parameter**: All read tools accept `detail='summary'` (default, concise) or `detail='full'` (raw API response). Use summary for lists; full when you need every field.

**Pagination**: All list tools accept `limit`/`max_results` (default 25/50) and `start`/`start_at` for offset.

**Auth auto-detection**: Each server detects auth mode from env vars — no explicit `AUTH_TYPE` needed unless overriding.

## Allowed Use

- Query Jira issues, projects, sprints, and worklogs for requirements and task context.
- Read and write Confluence pages, spaces, and blog posts for documentation.
- Inspect Bitbucket repos, PRs, branches, and commits for code review and release context.
- Create and update Jira issues, comments, and transitions as part of a defined workflow.
- Cross-check Atlassian context against local code before recommending changes.

## Prohibited Use

- Do not upload, download, or read attachment file paths through Atlassian tools outside an explicitly approved workflow.
- Do not read credentials, cookies, browser sessions, keyring entries, or OAuth token files.
- Do not enable SSL bypass, public tunnels, public telemetry, or public scraping.
- Do not broaden egress beyond the configured Atlassian host URLs.
- Do not set up credentials yourself — tell the user what env vars are missing.

## Policy Requirements

- Read-only code inspection is allowed.
- Shell write, git write, deployment, database read, ticket creation, and browser use require policy approval unless the active profile says otherwise.
- Credential reads, cookie import, public tunnels, public telemetry, and public scraping are disabled by default.

## Output Rules

- Report findings with file paths, concrete evidence, and recommended actions.
- Do not include secrets, raw credentials, cookie values, full prompts, or full data extracts.
- Prefer structured summaries that can map to AG-UI events later.
