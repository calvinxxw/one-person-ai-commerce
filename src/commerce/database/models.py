"""SQLAlchemy models for the Scout V0.1 closed-loop data model."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from sqlalchemy import JSON, Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    platform_product_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(512))
    category: Mapped[str | None] = mapped_column(String(128))
    subcategory: Mapped[str | None] = mapped_column(String(128))
    product_url: Mapped[str | None] = mapped_column(Text)
    seller_id: Mapped[str | None] = mapped_column(String(128))
    current_price: Mapped[float | None] = mapped_column(Float)
    currency: Mapped[str | None] = mapped_column(String(8))
    source_market: Mapped[str | None] = mapped_column(String(32))
    first_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str | None] = mapped_column(String(32))

    metrics: Mapped[list["ProductMetricDaily"]] = relationship(back_populates="product")
    content_signals: Mapped[list["ContentSignal"]] = relationship(back_populates="product")
    scores: Mapped[list["ScoutScore"]] = relationship(back_populates="product")
    decisions: Mapped[list["HumanDecision"]] = relationship(back_populates="product")
    experiments: Mapped[list["ExperimentResult"]] = relationship(back_populates="product")


class ProductMetricDaily(Base):
    __tablename__ = "product_metrics_daily"
    __table_args__ = (UniqueConstraint("product_id", "snapshot_date"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    snapshot_date: Mapped[date] = mapped_column(Date)
    price: Mapped[float | None] = mapped_column(Float)
    sales_volume: Mapped[int | None] = mapped_column(Integer)
    gmv: Mapped[float | None] = mapped_column(Float)
    views: Mapped[int | None] = mapped_column(Integer)
    clicks: Mapped[int | None] = mapped_column(Integer)
    ctr: Mapped[float | None] = mapped_column(Float)
    orders: Mapped[int | None] = mapped_column(Integer)
    conversion_rate: Mapped[float | None] = mapped_column(Float)
    creator_count: Mapped[int | None] = mapped_column(Integer)
    video_count: Mapped[int | None] = mapped_column(Integer)
    sales_growth_7d: Mapped[float | None] = mapped_column(Float)
    sales_growth_30d: Mapped[float | None] = mapped_column(Float)
    raw_data: Mapped[dict[str, Any] | None] = mapped_column(JSON)

    product: Mapped[Product] = relationship(back_populates="metrics")


class ContentSignal(Base):
    __tablename__ = "content_signals"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    snapshot_date: Mapped[date] = mapped_column(Date)
    keyword: Mapped[str | None] = mapped_column(String(256))
    hashtag: Mapped[str | None] = mapped_column(String(256))
    related_video_count: Mapped[int | None] = mapped_column(Integer)
    engagement_signal: Mapped[float | None] = mapped_column(Float)
    trend_signal: Mapped[float | None] = mapped_column(Float)
    creator_signal: Mapped[float | None] = mapped_column(Float)
    visual_demo_score: Mapped[float | None] = mapped_column(Float)
    hook_potential_score: Mapped[float | None] = mapped_column(Float)
    source: Mapped[str | None] = mapped_column(String(128))
    raw_data: Mapped[dict[str, Any] | None] = mapped_column(JSON)

    product: Mapped[Product] = relationship(back_populates="content_signals")


class ScoutScore(Base):
    __tablename__ = "scout_scores"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    scored_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    demand_score: Mapped[float] = mapped_column(Float)
    growth_score: Mapped[float] = mapped_column(Float)
    content_score: Mapped[float] = mapped_column(Float)
    competition_score: Mapped[float] = mapped_column(Float)
    fulfillment_score: Mapped[float] = mapped_column(Float)
    economics_score: Mapped[float] = mapped_column(Float)
    total_score: Mapped[float] = mapped_column(Float)
    confidence_score: Mapped[float | None] = mapped_column(Float)
    hard_filter_pass: Mapped[bool | None] = mapped_column(Boolean)
    filter_reasons: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    ai_summary: Mapped[str | None] = mapped_column(Text)
    risk_summary: Mapped[str | None] = mapped_column(Text)
    recommended_action: Mapped[str | None] = mapped_column(String(32))
    scoring_model_version: Mapped[str] = mapped_column(String(64), index=True)

    product: Mapped[Product] = relationship(back_populates="scores")
    decisions: Mapped[list["HumanDecision"]] = relationship(back_populates="scout_score")


class HumanDecision(Base):
    __tablename__ = "human_decisions"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    scout_score_id: Mapped[int] = mapped_column(ForeignKey("scout_scores.id"), index=True)
    decision: Mapped[str] = mapped_column(String(16))
    reason: Mapped[str | None] = mapped_column(Text)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    product: Mapped[Product] = relationship(back_populates="decisions")
    scout_score: Mapped[ScoutScore] = relationship(back_populates="decisions")


class ExperimentResult(Base):
    __tablename__ = "experiment_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    experiment_id: Mapped[str] = mapped_column(String(128), index=True)
    start_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    end_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    videos_published: Mapped[int | None] = mapped_column(Integer)
    impressions: Mapped[int | None] = mapped_column(Integer)
    video_views: Mapped[int | None] = mapped_column(Integer)
    product_clicks: Mapped[int | None] = mapped_column(Integer)
    ctr: Mapped[float | None] = mapped_column(Float)
    add_to_cart: Mapped[int | None] = mapped_column(Integer)
    orders: Mapped[int | None] = mapped_column(Integer)
    conversion_rate: Mapped[float | None] = mapped_column(Float)
    revenue: Mapped[float | None] = mapped_column(Float)
    product_cost: Mapped[float | None] = mapped_column(Float)
    shipping_cost: Mapped[float | None] = mapped_column(Float)
    platform_fee: Mapped[float | None] = mapped_column(Float)
    ad_cost: Mapped[float | None] = mapped_column(Float)
    total_cost: Mapped[float | None] = mapped_column(Float)
    profit: Mapped[float | None] = mapped_column(Float)
    result: Mapped[str | None] = mapped_column(String(16))
    notes: Mapped[str | None] = mapped_column(Text)

    product: Mapped[Product] = relationship(back_populates="experiments")
