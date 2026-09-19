from pathlib import Path


def test_expected_source_packages_exist() -> None:
    root = Path(__file__).parents[1]
    expected = ("scout", "providers", "scoring", "database", "experiments")
    for package in expected:
        assert (root / "src" / "commerce" / package / "__init__.py").is_file()
