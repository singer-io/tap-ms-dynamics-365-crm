import sys
import json
import singer
from tap_ms_dynamics_365_crm.client import Client
from tap_ms_dynamics_365_crm.discover import discover
from tap_ms_dynamics_365_crm.sync import sync

LOGGER = singer.get_logger()

REQUIRED_CONFIG_KEYS = [
    'client_id',
    'client_secret',
    'organization_uri',
    'redirect_uri',
    'refresh_token',
    'start_date'
]

def do_discover(client: Client):
    """
    Discover and emit the catalog to stdout
    """
    LOGGER.info("Starting discover")
    catalog = discover(client=client)
    json.dump(catalog.to_dict(), sys.stdout, indent=2)
    LOGGER.info("Finished discover")


@singer.utils.handle_top_exception(LOGGER)
def main():
    """
    Run the tap
    """
    parsed_args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)
    state = {}
    if parsed_args.state:
        state = parsed_args.state

    with Client(parsed_args.config_path, parsed_args.config) as client:
        if parsed_args.discover:
            do_discover(client=client)
        elif parsed_args.catalog:
            sync(
                client=client,
                config=parsed_args.config,
                catalog=parsed_args.catalog,
                state=state)


if __name__ == "__main__":
    main()

