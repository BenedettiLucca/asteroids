"""Basic tests for asteroids game math and structure."""
import math
import pytest


def test_circle_collision_basic():
    """Basic circle collision math (pure function test)."""
    def circles_collide(x1, y1, r1, x2, y2, r2):
        dx = x1 - x2
        dy = y1 - y2
        distance = math.sqrt(dx*dx + dy*dy)
        return distance < (r1 + r2)

    # Overlapping
    assert circles_collide(0, 0, 10, 5, 0, 10) is True
    # Not overlapping
    assert circles_collide(0, 0, 5, 20, 0, 5) is False
    # Touching
    assert circles_collide(0, 0, 10, 20, 0, 10) is False  # strict < for now


def test_asteroid_score_values():
    """Test score value logic based on asteroid radius (extracted from get_score_value)."""
    def get_score_value(radius):
        if radius > 40:
            return 20
        elif radius > 20:
            return 50
        else:
            return 100

    assert get_score_value(50) == 20   # large
    assert get_score_value(30) == 50   # medium
    assert get_score_value(15) == 100  # small
