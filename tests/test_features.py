from __future__ import annotations

from textual.app import App


def test_textual_env_var(monkeypatch):
    monkeypatch.setenv("TEXTUAL", "")
    app = App()
    assert app.features == set()
    assert app.devtools_enabled is False
    assert app.debug is False

    monkeypatch.setenv("TEXTUAL", "devtools")
    app = App()
    assert app.features == {"devtools"}
    assert app.devtools_enabled is True
    assert app.debug is False

    monkeypatch.setenv("TEXTUAL", "devtools,debug")
    app = App()
    assert app.features == {"devtools", "debug"}
    assert app.devtools_enabled is True
    assert app.debug is True

    monkeypatch.setenv("TEXTUAL", "devtools, debug")
    app = App()
    assert app.features == {"devtools", "debug"}
    assert app.devtools_enabled is True
    assert app.debug is True
