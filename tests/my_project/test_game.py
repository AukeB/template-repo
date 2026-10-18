"""Module for testing game.py"""

import pygame as pg
import pytest

from my_project.game import Game
from my_project.renderer import Renderer


@pytest.fixture(scope="function", name="game")
def fixture_game(mock_config):
    """Creates a Game with a headless window and closes the window afterwards."""
    game = Game(config=mock_config)

    yield game

    game.renderer.quit()


def _post_event(event_type, **attributes):
    """Queues a pygame event so the next event read returns it.

    Args:
        event_type (int): The pygame event type, such as pg.QUIT.
        attributes (object): Extra event fields, such as the pressed key.
    """

    event = pg.event.Event(event_type, **attributes)

    pg.event.post(event)


# Testing the "__init__" method from the "Game" class.


def test_init_reads_fps_and_creates_renderer(game):
    """The frame rate comes from the config, the game starts running, and a renderer is created."""
    assert game.fps == 60
    assert game.running is True
    assert isinstance(game.renderer, Renderer)


# Testing the "_handle_events" method from the "Game" class.


def test_handle_events_stops_on_window_close(game):
    """Closing the window stops the game."""
    _post_event(pg.QUIT)

    game._handle_events()

    assert game.running is False


def test_handle_events_stops_on_escape(game):
    """Pressing Escape stops the game."""
    _post_event(pg.KEYDOWN, key=pg.K_ESCAPE)

    game._handle_events()

    assert game.running is False


def test_handle_events_ignores_other_keys(game):
    """Other key presses leave the game running."""
    _post_event(pg.KEYDOWN, key=pg.K_a)

    game._handle_events()

    assert game.running is True


# Testing the "_update" method from the "Game" class.


def test_update_returns_none(game):
    """The placeholder update does nothing and returns None."""
    assert game._update(0.016) is None


# Testing the "_loop" method from the "Game" class.


def test_loop_runs_until_the_game_stops(game):
    """The loop keeps running frames until a quit event stops it."""
    _post_event(pg.QUIT)

    game._loop()

    assert game.running is False


def test_loop_renders_each_frame(game, monkeypatch):
    """Every frame of the loop is drawn before the loop checks for a stop."""
    frames = []

    def fake_render():
        frames.append("frame")

    monkeypatch.setattr(game.renderer, "render", fake_render)
    _post_event(pg.QUIT)

    game._loop()

    assert frames == ["frame"]


# Testing the "_quit" method from the "Game" class.


def test_quit_exits_the_process(game):
    """Quitting shuts down pygame and exits the process."""
    with pytest.raises(SystemExit):
        game._quit()


# Testing the "run" method from the "Game" class.


def test_run_loops_then_quits(game, monkeypatch):
    """Run calls the main loop and then the shutdown."""
    calls = []

    def fake_loop():
        calls.append("loop")

    def fake_quit():
        calls.append("quit")

    monkeypatch.setattr(game, "_loop", fake_loop)
    monkeypatch.setattr(game, "_quit", fake_quit)

    game.run()

    assert calls == ["loop", "quit"]
