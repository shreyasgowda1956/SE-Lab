import pytest

from ride_share_fare import (
    extra_distance_fare,
    seats_and_bags_ok,
    pickup_status,
)


@pytest.mark.parametrize(
    "cab,distance,zone,subscriber,expected",
    [
        ("mini", 5, "city", False, 0),
        ("mini", 10, "city", False, 60),
        ("sedan", 11, "city", True, 0),
        ("sedan", 12, "city", True, 12),
        ("suv", 13, "city", True, 12),
        ("mini", 10, "outstation", False, 90),
        ("mini", 30, "city", False, 500),
        ("mini", 30, "outstation", False, 750),
    ],
)
def test_fare_branches(cab, distance, zone, subscriber, expected):
    assert extra_distance_fare(cab, distance, zone, subscriber) == expected


@pytest.mark.parametrize("cab", ["bike", "van"])
def test_invalid_cab(cab):
    with pytest.raises(ValueError, match="unknown cab type"):
        extra_distance_fare(cab, 10, "city", False)


@pytest.mark.parametrize("distance", [-1, -10])
def test_negative_distance(distance):
    with pytest.raises(ValueError, match="invalid distance"):
        extra_distance_fare("mini", distance, "city", False)


@pytest.mark.parametrize(
    "passengers,bags,wheelchair,expected",
    [
        (2, 3, True, True),
        (3, 1, True, False),
        (4, 2, False, True),
        (5, 1, False, False),
        (2, 3, False, False),
    ],
)
def test_seat_and_bag_branches(passengers, bags, wheelchair, expected):
    assert seats_and_bags_ok(passengers, bags, wheelchair) is expected


@pytest.mark.parametrize(
    "minutes,scheduled,airport,expected",
    [
        (10, True, False, "on_time"),
        (9, True, False, "delayed"),
        (-6, True, False, "missed"),
        (5, False, False, "on_time"),
        (4, False, False, "delayed"),
        (-11, False, False, "missed"),
        (20, True, True, "on_time"),
        (19, True, True, "delayed"),
        (4, True, True, "missed"),
        (15, False, True, "on_time"),
        (14, False, True, "delayed"),
        (-1, False, True, "missed"),
    ],
)
def test_pickup_branches(minutes, scheduled, airport, expected):
    assert pickup_status(minutes, scheduled, airport) == expected
