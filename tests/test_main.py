from app.main import get_greeting


def test_get_greeting():
    assert get_greeting() == "Welcome to Auto Driving Car Simulation!"
