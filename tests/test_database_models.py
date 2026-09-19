from datetime import date, datetime, timezone

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

from commerce.database.models import (
    Base,
    ContentSignal,
    ExperimentResult,
    HumanDecision,
    Product,
    ProductMetricDaily,
    ScoutScore,
)


def make_session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def test_six_core_tables_are_created() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    assert set(inspect(engine).get_table_names()) == {
        "products",
        "product_metrics_daily",
        "content_signals",
        "scout_scores",
        "human_decisions",
        "experiment_results",
    }


def test_product_relations_and_nullable_observed_metrics() -> None:
    with make_session() as session:
        product = Product(
            platform_product_id="tt-001",
            title="Rechargeable Headlamp",
            category="Outdoor",
            subcategory="Outdoor Lighting",
            current_price=19.99,
            currency="USD",
            source_market="US",
        )
        session.add(product)
        session.flush()

        metric = ProductMetricDaily(
            product_id=product.id,
            snapshot_date=date(2026, 9, 19),
            sales_volume=None,
            gmv=None,
            raw_data={"source": "mock"},
        )
        session.add(metric)
        session.commit()

        assert metric.product_id == product.id
        assert metric.sales_volume is None
        assert metric.gmv is None


def test_score_version_and_human_decision_are_preserved() -> None:
    with make_session() as session:
        product = Product(platform_product_id="tt-002", title="Test Light")
        session.add(product)
        session.flush()
        score = ScoutScore(
            product_id=product.id,
            scored_at=datetime.now(timezone.utc),
            demand_score=25.0,
            growth_score=16.0,
            content_score=17.0,
            competition_score=11.0,
            fulfillment_score=9.0,
            economics_score=4.0,
            total_score=82.0,
            confidence_score=87.0,
            hard_filter_pass=True,
            scoring_model_version="SCOUT_SCORE_V0.1",
        )
        session.add(score)
        session.flush()
        decision = HumanDecision(
            product_id=product.id,
            scout_score_id=score.id,
            decision="PASS",
        )
        session.add(decision)
        session.commit()

        assert score.scoring_model_version == "SCOUT_SCORE_V0.1"
        assert score.confidence_score == 87.0
        assert decision.decision == "PASS"
