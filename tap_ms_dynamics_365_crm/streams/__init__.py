"""
Stream classes and utilities for MS Dynamics 365 CRM.
"""
from tap_ms_dynamics_365_crm.streams.streams import (
    get_streams,
    build_schema,
    REPLICATION_TO_STREAM_MAP
)

# EntityDefinitions.EntitySetName is normally authoritative for the Web API
# collection URL segment, but a handful of internal/system entities report a
# casing that does not match their actual (case-sensitive) registered route,
# causing a 404 "Resource not found for the segment" error. Map those
# logical names to the correct endpoint casing here.
ENTITY_SET_NAME_OVERRIDES = {
    'attributepicklistvalue': 'attributepicklistvalues',
    'delegatedauthorization': 'delegatedauthorizations',
    'gitsolution': 'gitsolutions',
    'ribbonmetadatatoprocess': 'ribbonmetadatasettoprocess',
}
