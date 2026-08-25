from backend.data_pipeline.collectors.mock_collector import MockFareCollector


def test_mock_collector_returns_observations():
    collector = MockFareCollector()

    observations = collector.collect()

    assert len(observations) == 2

    assert observations[0]["flight_number"] == "6E501"
    assert observations[1]["flight_number"] == "6E502"

    assert observations[0]["currency"] == "INR"
    assert observations[1]["currency"] == "INR"

    assert observations[0]["fare"] == "5200.00"
    assert observations[1]["fare"] == "6100.00"