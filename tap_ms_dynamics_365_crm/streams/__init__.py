"""
Stream classes and utilities for MS Dynamics 365 CRM.
"""
from tap_ms_dynamics_365_crm.streams.streams import (
    BaseStream,
    IncrementalStream,
    FullTableStream,
    get_streams,
    build_schema,
    EXCLUDED_ENTITIES,
    INCLUDED_ENTITIES,
)

STREAMS = {}

