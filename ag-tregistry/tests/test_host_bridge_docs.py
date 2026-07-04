from pathlib import Path


def test_root_host_bridge_docs_exist():
    assert Path("AGENTS.md").exists()
    assert Path("CLAUDE.md").exists()


def test_host_bridge_docs_reference_runtime_inventory():
    assert "/api/runtime/snapshot" in Path("AGENTS.md").read_text(encoding="utf-8")
    assert "/api/runtime/summary" in Path("CLAUDE.md").read_text(encoding="utf-8")
