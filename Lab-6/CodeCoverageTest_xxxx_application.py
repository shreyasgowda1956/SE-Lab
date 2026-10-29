import pytest

from ride_share_fare import (
    extra_distance_fare,
    seats_and_bags_ok,
    pickup_status,
)


def test_fare_within_included_distance():
    assert extra_distance_fare("sedan", 5, "city", False) == 0


def test_fare_for_mini_cab():
    assert extra_distance_fare("mini", 10, "city", False) == 60


def test_subscriber_gets_extra_included_distance():
    assert extra_distance_fare("sedan", 10, "city", True) == 0


def test_suv_subscriber_does_not_get_extra_included_distance():
    assert extra_distance_fare("suv", 12, "city", True) == 0


def test_outstation_fare():
    assert extra_distance_fare("mini", 10, "outstation", False) == 90


def test_long_city_journey():
    assert extra_distance_fare("mini", 30, "city", False) == 500


def test_invalid_cab_type():
    with pytest.raises(ValueError, match="unknown cab type"):
        extra_distance_fare("bike", 10, "city", False)


def test_negative_distance():
    with pytest.raises(ValueError, match="invalid distance"):
        extra_distance_fare("mini", -1, "city", False)


def test_wheelchair_passenger_limit():
    assert seats_and_bags_ok(2, 3, True) is True
    assert seats_and_bags_ok(3, 1, True) is False


def test_regular_passenger_and_bag_limits():
    assert seats_and_bags_ok(4, 2, False) is True
    assert seats_and_bags_ok(5, 1, False) is False
    assert seats_and_bags_ok(2, 3, False) is False


def test_pickup_on_time():
    assert pickup_status(10, True, False) == "on_time"


def test_pickup_delayed():
    assert pickup_status(0, False, False) == "delayed"


def test_pickup_missed():
    assert pickup_status(-11, False, False) == "missed"


def test_airport_pickup_cutoff():
    assert pickup_status(10, True, True) == "delayed"
