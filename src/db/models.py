"""
models.py — SQLAlchemy table definitions.
Owner: DEV2
Includes production context fields for root cause analysis.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class InspectionResult(Base):
    __tablename__ = "inspection_results"

    id              = Column(Integer, primary_key=True, index=True)
    timestamp       = Column(DateTime, default=datetime.utcnow)
    result          = Column(String, nullable=False)   # PASS | WARN | FAIL
    confidence      = Column(Float, nullable=False)
    defect_types    = Column(JSON, default=list)
    frame_path      = Column(String, nullable=True)

    # Production context — required for root cause analysis
    shift_id        = Column(String, nullable=True)    # morning | evening | night
    operator_id     = Column(String, nullable=True)
    batch_id        = Column(String, nullable=True)
    line_speed_mpm  = Column(Float, nullable=True)
    hour_of_day     = Column(Integer, nullable=True)
    parts_since_last_clean = Column(Integer, nullable=True)

    defect_regions  = relationship("DefectRegion", back_populates="inspection")


class DefectRegion(Base):
    __tablename__ = "defect_regions"

    id              = Column(Integer, primary_key=True, index=True)
    inspection_id   = Column(Integer, ForeignKey("inspection_results.id"))
    defect_type     = Column(String)
    x = Column(Integer)
    y = Column(Integer)
    w = Column(Integer)
    h = Column(Integer)
    confidence      = Column(Float)

    inspection      = relationship("InspectionResult", back_populates="defect_regions")
