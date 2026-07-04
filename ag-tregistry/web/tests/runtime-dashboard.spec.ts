import { expect, test } from "@playwright/test";

test("runtime dashboard shows installed hosts, agents, and MCPs", async ({ page }) => {
  await page.goto("/");

  await expect(page.getByRole("heading", { name: /installed runtime inventory/i })).toBeVisible();
  await expect(page.getByText(/current session runtime/i)).toBeVisible();

  await page.getByRole("button", { name: "agents" }).click();
  await expect(page.getByText("orchestrate")).toBeVisible();
  await expect(page.getByText("claude, codex, copilot").first()).toBeVisible();

  await page.getByRole("button", { name: "mcps" }).click();
  await expect(page.getByText("codebase-engine", { exact: true }).first()).toBeVisible();

  await page.getByRole("button", { name: "hosts" }).click();
  await expect(page.getByText("CLAUDE.md").first()).toBeVisible();
});
