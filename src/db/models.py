from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class InspectionResult(Base):
    __tablename__ = 'inspection_results'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    result = Column(String)         # 'PASS' | 'FAIL' | 'WARN'
    confidence = Column(Float)      # 0.0 - 1.0
    defect_types = Column(JSON)     # e.g., ['scratch', 'dust']
    defect_score = Column(Float)
    frame_path = Column(String)     # archived image path
    
    # Production context for root cause analysis
    shift_id = Column(String)       # 'morning' | 'evening' | 'night'
    operator_id = Column(String)    # who was operating line
    batch_id = Column(String)       # material batch/lot number
    line_speed_mpm = Column(Float)  # conveyor speed at time of inspection
    ambient_temp_c = Column(Float)  # optional: env sensor
    hour_of_day = Column(Integer)   # 0-23
    parts_since_last_clean = Column(Integer) # maintenance correlation

class DefectRegion(Base):
    __tablename__ = 'defect_regions'
    
    id = Column(Integer, primary_key=True)
    inspection_id = Column(Integer, ForeignKey('inspection_results.id'))
    defect_type = Column(String)
    x = Column(Integer)
    y = Column(Integer)
    w = Column(Integer)
    h = Column(Integer)
    confidence = Column(Float)

class ProductionContext(Base):
    __tablename__ = 'production_context'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    shift_id = Column(String)
    batch_id = Column(String)
    operator_id = Column(String)
    notes = Column(Text)            # manual notes from operator
