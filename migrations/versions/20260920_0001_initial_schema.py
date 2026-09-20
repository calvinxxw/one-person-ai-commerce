"""create initial commerce schema

Revision ID: 20260920_0001
Revises:
"""

from alembic import op
import sqlalchemy as sa


revision = "20260920_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("platform_product_id", sa.String(length=128), nullable=False),
        sa.Column("title", sa.String(length=512), nullable=False),
        sa.Column("category", sa.String(length=128)),
        sa.Column("subcategory", sa.String(length=128)),
        sa.Column("product_url", sa.Text()),
        sa.Column("seller_id", sa.String(length=128)),
        sa.Column("current_price", sa.Float()),
        sa.Column("currency", sa.String(length=8)),
        sa.Column("source_market", sa.String(length=32)),
        sa.Column("first_seen_at", sa.DateTime(timezone=True)),
        sa.Column("last_seen_at", sa.DateTime(timezone=True)),
        sa.Column("status", sa.String(length=32)),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("platform_product_id"),
    )
    op.create_index("ix_products_platform_product_id", "products", ["platform_product_id"], unique=True)

    op.create_table(
        "product_metrics_daily",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("snapshot_date", sa.Date(), nullable=False),
        sa.Column("price", sa.Float()),
        sa.Column("sales_volume", sa.Integer()),
        sa.Column("gmv", sa.Float()),
        sa.Column("views", sa.Integer()),
        sa.Column("clicks", sa.Integer()),
        sa.Column("ctr", sa.Float()),
        sa.Column("orders", sa.Integer()),
        sa.Column("conversion_rate", sa.Float()),
        sa.Column("creator_count", sa.Integer()),
        sa.Column("video_count", sa.Integer()),
        sa.Column("sales_growth_7d", sa.Float()),
        sa.Column("sales_growth_30d", sa.Float()),
        sa.Column("raw_data", sa.JSON()),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("product_id", "snapshot_date"),
    )
    op.create_index("ix_product_metrics_daily_product_id", "product_metrics_daily", ["product_id"], unique=False)

    op.create_table(
        "content_signals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("snapshot_date", sa.Date(), nullable=False),
        sa.Column("keyword", sa.String(length=256)),
        sa.Column("hashtag", sa.String(length=256)),
        sa.Column("related_video_count", sa.Integer()),
        sa.Column("engagement_signal", sa.Float()),
        sa.Column("trend_signal", sa.Float()),
        sa.Column("creator_signal", sa.Float()),
        sa.Column("visual_demo_score", sa.Float()),
        sa.Column("hook_potential_score", sa.Float()),
        sa.Column("source", sa.String(length=128)),
        sa.Column("raw_data", sa.JSON()),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_content_signals_product_id", "content_signals", ["product_id"], unique=False)

    op.create_table(
        "scout_scores",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("scored_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("demand_score", sa.Float(), nullable=False),
        sa.Column("growth_score", sa.Float(), nullable=False),
        sa.Column("content_score", sa.Float(), nullable=False),
        sa.Column("competition_score", sa.Float(), nullable=False),
        sa.Column("fulfillment_score", sa.Float(), nullable=False),
        sa.Column("economics_score", sa.Float(), nullable=False),
        sa.Column("total_score", sa.Float(), nullable=False),
        sa.Column("confidence_score", sa.Float()),
        sa.Column("hard_filter_pass", sa.Boolean()),
        sa.Column("filter_reasons", sa.JSON()),
        sa.Column("ai_summary", sa.Text()),
        sa.Column("risk_summary", sa.Text()),
        sa.Column("recommended_action", sa.String(length=32)),
        sa.Column("scoring_model_version", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_scout_scores_product_id", "scout_scores", ["product_id"], unique=False)
    op.create_index("ix_scout_scores_scoring_model_version", "scout_scores", ["scoring_model_version"], unique=False)

    op.create_table(
        "human_decisions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("scout_score_id", sa.Integer(), nullable=False),
        sa.Column("decision", sa.String(length=16), nullable=False),
        sa.Column("reason", sa.Text()),
        sa.Column("decided_at", sa.DateTime(timezone=True)),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["scout_score_id"], ["scout_scores.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_human_decisions_product_id", "human_decisions", ["product_id"], unique=False)
    op.create_index("ix_human_decisions_scout_score_id", "human_decisions", ["scout_score_id"], unique=False)

    op.create_table(
        "experiment_results",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("experiment_id", sa.String(length=128), nullable=False),
        sa.Column("start_at", sa.DateTime(timezone=True)),
        sa.Column("end_at", sa.DateTime(timezone=True)),
        sa.Column("videos_published", sa.Integer()),
        sa.Column("impressions", sa.Integer()),
        sa.Column("video_views", sa.Integer()),
        sa.Column("product_clicks", sa.Integer()),
        sa.Column("ctr", sa.Float()),
        sa.Column("add_to_cart", sa.Integer()),
        sa.Column("orders", sa.Integer()),
        sa.Column("conversion_rate", sa.Float()),
        sa.Column("revenue", sa.Float()),
        sa.Column("product_cost", sa.Float()),
        sa.Column("shipping_cost", sa.Float()),
        sa.Column("platform_fee", sa.Float()),
        sa.Column("ad_cost", sa.Float()),
        sa.Column("total_cost", sa.Float()),
        sa.Column("profit", sa.Float()),
        sa.Column("result", sa.String(length=16)),
        sa.Column("notes", sa.Text()),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_experiment_results_product_id", "experiment_results", ["product_id"], unique=False)
    op.create_index("ix_experiment_results_experiment_id", "experiment_results", ["experiment_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_experiment_results_experiment_id", table_name="experiment_results")
    op.drop_index("ix_experiment_results_product_id", table_name="experiment_results")
    op.drop_table("experiment_results")
    op.drop_index("ix_human_decisions_scout_score_id", table_name="human_decisions")
    op.drop_index("ix_human_decisions_product_id", table_name="human_decisions")
    op.drop_table("human_decisions")
    op.drop_index("ix_scout_scores_scoring_model_version", table_name="scout_scores")
    op.drop_index("ix_scout_scores_product_id", table_name="scout_scores")
    op.drop_table("scout_scores")
    op.drop_index("ix_content_signals_product_id", table_name="content_signals")
    op.drop_table("content_signals")
    op.drop_index("ix_product_metrics_daily_product_id", table_name="product_metrics_daily")
    op.drop_table("product_metrics_daily")
    op.drop_index("ix_products_platform_product_id", table_name="products")
    op.drop_table("products")
