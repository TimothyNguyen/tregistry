import sys

from app.cli import main


def test_cli_lists_agents(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["aa", "list-agents"])
    main()
    output = capsys.readouterr().out
    assert "swe" in output
    assert "orchestrate" in output


def test_cli_lists_skills(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["aa", "list-skills"])
    main()
    output = capsys.readouterr().out
    assert "spec" in output


def test_cli_lists_mcps(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["aa", "list-mcps"])
    main()
    capsys.readouterr()


def test_cli_lists_prompts(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["aa", "list-prompts"])
    main()
    output = capsys.readouterr().out
    assert "claude" in output or "codex" in output


def test_cli_lists_deployments_empty(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["aa", "list-deployments"])
    main()
    capsys.readouterr()


def test_cli_deploy_and_remove(capsys, monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        ["aa", "deploy", "agent", "security", "--namespace", "default"],
    )
    main()
    deploy_output = capsys.readouterr().out.strip()
    assert deploy_output.startswith("deployed default/security")

    monkeypatch.setattr(sys, "argv", ["aa", "remove", "security", "--namespace", "default"])
    main()
    remove_output = capsys.readouterr().out.strip()
    assert "Removed deployment default/security." == remove_output
