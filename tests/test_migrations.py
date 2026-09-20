from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect


EXPECTED_TABLES = {
    "products",
    "product_metrics_daily",
    "content_signals",
    "scout_scores",
    "human_decisions",
    "experiment_results",
}


def test_upgrade_head_creates_schema(tmp_path: Path) -> None:
    database_url = f"sqlite:///{tmp_path / 'migration-test.db'}"
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", database_url)

    command.upgrade(config, "head")

    engine = create_engine(database_url)
    assert EXPECTED_TABLES | {"alembic_version"} == set(
        inspect(engine).get_table_names()
    )
