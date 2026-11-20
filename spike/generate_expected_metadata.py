#!/usr/bin/env python3
"""Regenerates tests/expected_metadata.json from a live discovery run.

This is a deliberate, on-demand developer/CI utility -- it is NOT run
automatically before test execution, and intentionally so:
tests/base.py's expected_metadata() treats this file as a frozen regression
baseline that a live discovery run (performed separately, by the actual
integration test suite) is checked against. If this script's output were
regenerated immediately before every test run via the same discovery code
being tested, that comparison would become tautological for the fields
sourced directly from tap discovery logic (primary_keys/replication_method/
replication_keys): a bug in that logic would agree with itself on both
sides and the test would never catch it. That logic already has dedicated
unit test coverage (see tests/unittests/test_streams.py); this script's job
is only to keep the regression baseline in sync with the *sandbox's actual
entity list*, not to validate tap logic.

Re-run this manually (and review the resulting diff) whenever:
 - the sandbox's entity list legitimately changes (entities added/removed)
 - a tap change intentionally alters discovery output
 - CUSTOM_STREAMS_TO_SKIP changes in tests/base.py

Usage (requires sandbox credentials, e.g. the same ones CI uses):
    export TAP_MS_DYNAMICS_365_CRM_CLIENT_ID=...
    export TAP_MS_DYNAMICS_365_CRM_CLIENT_SECRET=...
    export TAP_MS_DYNAMICS_365_CRM_ORGANIZATION_URI=...
    export TAP_MS_DYNAMICS_365_CRM_TENANT_ID=...
    python spike/generate_expected_metadata.py
"""
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from singer import metadata as singer_metadata  # noqa: E402

from tap_ms_dynamics_365_crm.client import Client  # noqa: E402
from tap_ms_dynamics_365_crm.discover import discover  # noqa: E402

OUTPUT_PATH = REPO_ROOT / "tests" / "expected_metadata.json"

REQUIRED_ENV_VARS = (
    "TAP_MS_DYNAMICS_365_CRM_CLIENT_ID",
    "TAP_MS_DYNAMICS_365_CRM_CLIENT_SECRET",
    "TAP_MS_DYNAMICS_365_CRM_ORGANIZATION_URI",
    "TAP_MS_DYNAMICS_365_CRM_TENANT_ID",
)

# Org-specific custom entities (created ad-hoc in the test sandbox) that
# are not part of the tap's standard expected metadata. Must be kept in
# sync with MSDynamics365CRMBaseTest.CUSTOM_STREAMS_TO_SKIP in
# tests/base.py -- duplicated here (rather than imported) so this script
# doesn't need the tap_tester package installed just to write a JSON file.
CUSTOM_STREAMS_TO_SKIP = {
    "componentversionnrddatasource",
    "new_testcustomactivity",
    "new_testelastic",
    "new_testequipmentlog",
    "new_testproject",
    "new_testrichtype",
    "new_testsurveyresponse",
}

# Per-stream `api_limit` overrides: a test-tuning knob (how many records a
# stream's pagination/all-fields tests sample), not a Dataverse metadata
# attribute, so it can't be derived from discovery. Anything not listed
# here falls back to the default already applied by
# MSDynamics365CRMBaseTest.expected_metadata() (100).
API_LIMIT_OVERRIDES = {
    "account": 5,
    "lead": 5,
    "opportunity": 5,
    "contact": 7,
    "incident": 16,
    "phonetocaseprocess": 16,
    "knowledgearticle": 11,
    "product": 10,
}


def _build_config() -> dict:
    missing = [name for name in REQUIRED_ENV_VARS if not os.getenv(name)]
    if missing:
        raise SystemExit(
            "Missing required environment variable(s): " + ", ".join(missing)
        )

    return {
        "auth_method": "client_credentials",
        "client_id": os.environ["TAP_MS_DYNAMICS_365_CRM_CLIENT_ID"],
        "client_secret": os.environ["TAP_MS_DYNAMICS_365_CRM_CLIENT_SECRET"],
        "organization_uri": os.environ["TAP_MS_DYNAMICS_365_CRM_ORGANIZATION_URI"],
        "tenant_id": os.environ["TAP_MS_DYNAMICS_365_CRM_TENANT_ID"],
        "start_date": "2019-01-01T00:00:00Z",
    }


def _stream_metadata(catalog_entry) -> dict:
    root_metadata = singer_metadata.to_map(catalog_entry.metadata).get((), {})
    replication_method = root_metadata.get("forced-replication-method", "FULL_TABLE")
    replication_keys = sorted(root_metadata.get("valid-replication-keys") or [])

    return {
        "primary_keys": sorted(catalog_entry.key_properties or []),
        "replication_method": replication_method,
        "replication_keys": replication_keys,
        # Derived, not independently sourced: every INCREMENTAL stream
        # filters on its replication key (modifiedon) via the configured
        # start_date, and FULL_TABLE streams never filter on it. Verified
        # against all pre-existing entries with zero exceptions before this
        # generator was introduced.
        "obeys_start_date": replication_method == "INCREMENTAL",
        "api_limit": API_LIMIT_OVERRIDES.get(catalog_entry.tap_stream_id, 100),
    }


def main() -> None:
    config = _build_config()

    with Client(config_path=None, config=config) as client:
        catalog = discover(client=client)

    expected_metadata = {
        entry.tap_stream_id: _stream_metadata(entry)
        for entry in sorted(catalog.streams, key=lambda e: e.tap_stream_id)
        if entry.tap_stream_id not in CUSTOM_STREAMS_TO_SKIP
    }

    OUTPUT_PATH.write_text(
        json.dumps(expected_metadata, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(expected_metadata)} streams to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
