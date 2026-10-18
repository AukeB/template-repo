"""Module for testing utils_pygame.py"""

from types import SimpleNamespace

import pygame as pg

from my_project.utils.utils_pygame import get_window_size_from_screen_resolution


# Testing the "get_window_size_from_screen_resolution" function.


def test_window_size_initializes_display_when_inactive():
    """The display is initialized when it is not active yet."""
    pg.display.quit()

    get_window_size_from_screen_resolution()

    assert pg.display.get_init() is True


def test_window_size_scales_desktop_resolution(monkeypatch):
    """The window is the configured fraction of the desktop resolution."""

    def desktop_sizes():
        sizes = [(1000, 500)]

        return sizes

    monkeypatch.setattr(pg.display, "get_desktop_sizes", desktop_sizes)

    window_size = get_window_size_from_screen_resolution()

    assert window_size == (900, 450)


def test_window_size_clamps_to_minimum(monkeypatch):
    """A window smaller than the minimum is raised to the minimum size."""

    def desktop_sizes():
        sizes = [(100, 100)]

        return sizes

    monkeypatch.setattr(pg.display, "get_desktop_sizes", desktop_sizes)

    window_size = get_window_size_from_screen_resolution(min_width=400, min_height=300)

    assert window_size == (400, 300)


def test_window_size_uses_selected_monitor(monkeypatch):
    """The monitor index picks the desktop size to scale."""

    def desktop_sizes():
        sizes = [(1000, 500), (2000, 1000)]

        return sizes

    monkeypatch.setattr(pg.display, "get_desktop_sizes", desktop_sizes)

    window_size = get_window_size_from_screen_resolution(monitor_index=1)

    assert window_size == (1800, 900)


def test_window_size_falls_back_to_display_info_on_old_pygame(monkeypatch):
    """Older pygame versions read the desktop size from display info."""
    display_info = SimpleNamespace(current_w=2000, current_h=1000)

    def fake_info():
        return display_info

    monkeypatch.setattr(pg.version, "vernum", (1, 9, 6))
    monkeypatch.setattr(pg.display, "Info", fake_info)

    window_size = get_window_size_from_screen_resolution()

    assert window_size == (1800, 900)


def test_window_size_uses_default_desktop_when_info_is_unknown(monkeypatch):
    """When display info reports no size, a 1920x1080 desktop is assumed."""
    display_info = SimpleNamespace(current_w=0, current_h=0)

    def fake_info():
        return display_info

    monkeypatch.setattr(pg.version, "vernum", (1, 9, 6))
    monkeypatch.setattr(pg.display, "Info", fake_info)

    window_size = get_window_size_from_screen_resolution()

    assert window_size == (1728, 972)
