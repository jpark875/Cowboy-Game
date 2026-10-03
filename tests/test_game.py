"""Headless tests for the game rules."""

import os
import sys
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "Python Game"))

import pygame  # noqa: E402
import pytest  # noqa: E402

import Game as g  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_game(monkeypatch):
    monkeypatch.setattr(g.uvage, "is_pressing", lambda key: False)
    monkeypatch.setattr(pygame.mouse, "get_pressed", lambda *a, **k: (0, 0, 0))
    g.reset()
    for enemy in g.enemies:
        enemy.badguy.x = 900
        enemy.badguy.y = 560
    yield


def press(monkeypatch, *keys):
    monkeypatch.setattr(g.uvage, "is_pressing", lambda key: key in keys)


def click(monkeypatch, down=True):
    monkeypatch.setattr(pygame.mouse, "get_pressed", lambda *a, **k: (int(down), 0, 0))


@pytest.mark.parametrize(
    ("ticks", "hp"),
    [(0, 1), (2000, 1), (2001, 2), (3001, 4), (4001, 6), (5001, 8), (6001, 10), (99999, 10)],
)
def test_enemy_health_rises_with_time(ticks, hp):
    assert g.enemy_hp(ticks) == hp


def test_a_single_click_fires_from_the_cowboy():
    g.bullet.fire(g.cowboy, 20)
    assert g.bullet.flying
    assert g.bullet.bullet_image.x == g.cowboy.cowman.x + 5
    assert g.bullet.bullet_image.y == g.cowboy.cowman.y


def test_holding_the_mouse_fires_without_a_lost_first_tick(monkeypatch):
    click(monkeypatch)
    g.tick()
    assert g.bullet.flying


def test_bullet_leaves_the_screen_then_can_refire():
    g.bullet.fire(g.cowboy, 60)
    for _ in range(40):
        g.bullet.update(g.enemies)
    assert not g.bullet.flying
    g.bullet.fire(g.cowboy, 60)
    assert g.bullet.flying


def test_bullet_is_consumed_by_one_hit_and_damages_once():
    enemy = g.enemies[0]
    enemy.hp = enemy.max_hp = 5
    enemy.badguy.x, enemy.badguy.y = 300, g.cowboy.cowman.y
    g.cowboy.cowman.x = 100
    g.bullet.fire(g.cowboy, 15)

    for _ in range(60):
        g.bullet.update(g.enemies)

    assert enemy.hp == 4
    assert not g.bullet.flying


def test_killed_enemy_respawns_tougher_later_in_the_run():
    enemy = g.enemies[0]
    enemy.badguy.x = 300
    enemy.hp = 0

    enemy.update(ticks=3500)

    assert enemy.badguy.x == 899  # respawned at 900, then stepped once
    assert enemy.hp == enemy.max_hp == 4


def test_pineapples_raise_bullet_speed_up_to_the_cap(monkeypatch):
    for _ in range(30):
        g.fruit.pineapple.x, g.fruit.pineapple.y = g.cowboy.cowman.x, g.cowboy.cowman.y
        g.fruit.active = True
        g.update()
    assert g.bullet_speed == g.MAX_BULLET_SPEED


def test_first_pineapple_adds_the_boost():
    g.fruit.pineapple.x, g.fruit.pineapple.y = g.cowboy.cowman.x, g.cowboy.cowman.y
    g.fruit.active = True
    g.update()
    assert g.bullet_speed == g.BASE_BULLET_SPEED + g.PINEAPPLE_BOOST
    assert not g.fruit.active


def test_pineapple_spawns_on_the_timer():
    g.timer.ticks = g.FRUIT_INTERVAL - 1
    g.update()
    assert g.fruit.active


def test_two_hits_kill_the_cowboy():
    enemy = g.enemies[0]
    enemy.badguy.x, enemy.badguy.y = g.cowboy.cowman.x, g.cowboy.cowman.y
    for _ in range(g.HIT_FRAMES - 1):
        g.cowboy.take_contact(g.enemies)
    assert g.cowboy.hits == 0 and not g.cowboy.dead
    g.cowboy.take_contact(g.enemies)
    assert g.cowboy.hits == 1 and not g.cowboy.dead
    for _ in range(g.HIT_FRAMES):
        g.cowboy.take_contact(g.enemies)
    assert g.cowboy.dead


def test_game_ends_when_an_enemy_reaches_the_house():
    g.enemies[1].badguy.x = g.HOUSE_X
    g.update()
    assert not g.running


def test_space_restarts_with_original_settings(monkeypatch):
    g.bullet_speed = 45
    g.timer.ticks = 4000
    g.cowboy.cowman.x = 300
    g.cowboy.contact_frames = 100
    g.running = False

    press(monkeypatch, "space")
    g.tick()

    assert g.running
    assert g.bullet_speed == g.BASE_BULLET_SPEED
    assert g.timer.ticks == 0
    assert (g.cowboy.cowman.x, g.cowboy.cowman.y) == g.Cowboy.START
    assert g.cowboy.contact_frames == 0
    assert all(e.hp == 1 for e in g.enemies)


def test_game_over_waits_for_space(monkeypatch):
    g.running = False
    g.tick()
    assert not g.running


def test_movement_keys_and_screen_bounds(monkeypatch):
    start = g.cowboy.cowman.x
    press(monkeypatch, "d")
    g.cowboy.move()
    assert g.cowboy.cowman.x == start + g.cowboy.speed

    g.cowboy.cowman.x = 750
    g.cowboy.move()
    assert g.cowboy.cowman.x == 750

    press(monkeypatch, "w")
    g.cowboy.cowman.y = 50
    g.cowboy.move()
    assert g.cowboy.cowman.y == 50


def test_cacti_block_the_cowboy():
    cactus = g.scenery[0]
    g.cowboy.cowman.x, g.cowboy.cowman.y = cactus.x, cactus.y
    g.update()
    assert g.cowboy.cowman.overlap(cactus) == [0, 0]


def test_a_full_frame_renders_in_both_states():
    g.draw()
    g.running = False
    g.draw()
