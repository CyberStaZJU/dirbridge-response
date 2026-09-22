"""Deterministic equivalence test for the E4 FedScale duration convention."""
from types import SimpleNamespace

from e4_profile_duration_reference import fedscale_completion_time
from utils.fedscale_trace import _profile_duration


def test_known_profile_matches_official_formula():
    args = SimpleNamespace(
        fedscale_default_duration=1.0,
        fedscale_upload_size_mb=1.0,
        fedscale_download_size_mb=2.0,
        local_bs=8,
        local_period=10,
        fedscale_batch_size=0,
        fedscale_local_steps=0,
        fedscale_augmentation_factor=3.0,
    )
    record = {"computation": 12.5, "communication": 25.0}
    expected = fedscale_completion_time(12.5, 25.0, 8, 10, 1.0, 2.0)
    actual = _profile_duration(record, args)
    assert abs(actual - expected) < 1e-12
    assert abs(actual - 3.12) < 1e-12


def test_payload_units_are_numeric_megabytes():
    # The E4 convention is one numeric MB in each direction by default.
    assert fedscale_completion_time(0.0, 10.0, 1.0, 1.0, 1.0, 1.0) == 0.2


if __name__ == "__main__":
    test_known_profile_matches_official_formula()
    test_payload_units_are_numeric_megabytes()
    print("e4_fedscale_units=PASS")
