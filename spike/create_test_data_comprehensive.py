"""
Comprehensive Test Data Generator for MS Dynamics 365 CRM

Creates test records for Sales, Field Service, and Customer Service modules.

Usage:
    # Create data for all sales entities
    python create_test_data_comprehensive.py --config config.json --module sales --count 5

    # Create data for specific entities
    python create_test_data_comprehensive.py --config config.json --entities account,contact,lead --count 10

    # Create data for all modules
    python create_test_data_comprehensive.py --config config.json --module all --count 3

    # Cleanup previously created data
    python create_test_data_comprehensive.py --config config.json --cleanup
"""

import argparse
import json
import sys
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from faker import Faker

sys.path.insert(0, '..')
from tap_ms_dynamics_365_crm.client import Client
from tap_ms_dynamics_365_crm.streams import INCLUDED_ENTITIES, get_streams
from entity_templates import ENTITY_TEMPLATES


class DynamicsTestDataGenerator:
    """Comprehensive test data generator for MS Dynamics 365 CRM"""

    def __init__(self, client: Client, count: int = 5, module: str = 'sales',
                 specific_entities: Optional[List[str]] = None):
        self.client = client
        self.count = count
        self.module = module
        self.fake = Faker()
        self.created_records = {}

        # Load entity mappings from CRM metadata
        self._load_entity_mappings()

        # Determine which entities to create
        if specific_entities:
            self.entities_to_create = specific_entities
        elif module == 'all':
            self.entities_to_create = self._get_all_entities()
        else:
            self.entities_to_create = sorted(list(INCLUDED_ENTITIES.get(module, [])))

    def _load_entity_mappings(self):
        """Load entity LogicalName to EntitySetName mappings from CRM metadata"""
        try:
            streams = get_streams(self.client, create_schema=False)
            self._entity_mappings = {}
            for stream_name, stream_obj in streams.items():
                logical_name = stream_obj.tap_stream_id
                entity_set_name = stream_obj.path
                self._entity_mappings[logical_name] = entity_set_name
            print(f"Loaded {len(self._entity_mappings)} entity mappings from CRM metadata")
        except Exception as e:
            print(f"Warning: Could not load entity mappings from metadata: {str(e)}")
            self._entity_mappings = {}

    def _get_all_entities(self) -> List[str]:
        """Get all entities from all modules"""
        all_entities = set()
        for module_entities in INCLUDED_ENTITIES.values():
            all_entities.update(module_entities)
        return sorted(list(all_entities))

    def _get_entity_plural(self, entity: str) -> str:
        """Get plural form of entity name for API endpoint"""
        # First check dynamic mappings from CRM metadata
        if hasattr(self, '_entity_mappings') and entity in self._entity_mappings:
            return self._entity_mappings[entity]

        # For msdyn_ entities, use as-is (already plural)
        if entity.startswith('msdyn_'):
            return f"{entity}s" if not entity.endswith('s') else entity

        # Handle common pluralization rules
        if entity.endswith('y') and len(entity) > 1 and entity[-2] not in 'aeiou':
            # Words ending in consonant + y: change y to ies (e.g., category -> categories)
            return f"{entity[:-1]}ies"
        elif entity.endswith(('s', 'x', 'z', 'ch', 'sh')):
            # Words ending in s, x, z, ch, sh: add es
            return f"{entity}es"
        else:
            # Default: add 's'
            return f"{entity}s"

    def _extract_id_from_response(self, response: Any, entity: str) -> str:
        """Extract entity ID from create response"""
        try:
            if isinstance(response, dict):
                if '@odata.id' in response:
                    odata_id = response['@odata.id']
                    return odata_id.split('(')[1].split(')')[0]
                # Check for ID field
                id_field = f"{entity}id"
                if id_field in response:
                    return response[id_field]
            elif isinstance(response, str):
                return response
        except Exception:
            pass
        return "unknown"

    def create_entity_record(self, entity: str) -> Optional[Dict[str, Any]]:
        """Create a single record for the specified entity"""
        try:
            # Get template for this entity
            template = ENTITY_TEMPLATES.get(entity, {})

            if not template:
                # Create minimal record with just a name field
                record_data = {'name': self.fake.word().title()}
            else:
                # Generate data from template
                record_data = {}
                for field, value_func in template.items():
                    try:
                        record_data[field] = value_func(self.fake)
                    except Exception as e:
                        print(f"    Warning: Could not generate field '{field}': {str(e)}")

            # Get API endpoint
            entity_plural = self._get_entity_plural(entity)

            # Make create request
            response = self.client.make_request('POST', path=entity_plural, body=record_data)
            entity_id = self._extract_id_from_response(response, entity)

            # Track created record
            if entity not in self.created_records:
                self.created_records[entity] = []
            self.created_records[entity].append(entity_id)

            # Get display name
            display_name = record_data.get('name') or record_data.get('msdyn_name') or \
                          record_data.get('title') or record_data.get('subject') or entity_id[:8]

            print(f"  Created {entity}: {display_name} (ID: {entity_id[:8]}...)")
            return {'id': entity_id, **record_data}

        except Exception as e:
            print(f"   Failed to create {entity}: {str(e)}")
            return None

    def generate_all_test_data(self):
        """Generate test data for all selected entities"""
        print("\n" + "="*70)
        print(f"Creating Test Data for MS Dynamics 365 CRM - Module: {self.module.upper()}")
        print("="*70 + "\n")

        total_entities = len(self.entities_to_create)
        if total_entities == 0:
            print("No entities found to create!")
            return

        print(f"Will create {self.count} record(s) for each of {total_entities} entities\n")

        success_count = 0
        failure_count = 0

        for idx, entity in enumerate(self.entities_to_create, 1):
            print(f"[{idx}/{total_entities}] Creating {self.count} {entity} record(s)...")

            entity_success = 0
            for i in range(self.count):
                result = self.create_entity_record(entity)
                if result:
                    entity_success += 1
                else:
                    failure_count += 1

            if entity_success > 0:
                success_count += entity_success
            print()

        print("="*70)
        print(f"Test Data Creation Complete!")
        print(f"  Successfully created: {success_count} records")
        if failure_count > 0:
            print(f"  Failed: {failure_count} records")
        print("="*70)
        self.print_summary()

    def print_summary(self):
        """Print summary of created records"""
        print("\nSummary of Created Records:")
        print("-" * 70)
        total = 0
        for entity in sorted(self.created_records.keys()):
            count = len(self.created_records[entity])
            if count > 0:
                print(f"  {entity:<35} {count:>3} records")
                total += count
        print("-" * 70)
        print(f"  {'TOTAL':<35} {total:>3} records\n")

    def cleanup_test_data(self, cleanup_file: str = 'created_test_data.json'):
        """Delete all created test records"""
        print("\n" + "="*70)
        print("Cleaning Up Test Data")
        print("="*70 + "\n")

        # Load records from file if exists
        if not self.created_records:
            try:
                with open(cleanup_file, 'r') as f:
                    self.created_records = json.load(f)
                print(f"Loaded record IDs from {cleanup_file}\n")
            except FileNotFoundError:
                print(f"No cleanup file found: {cleanup_file}")
                print("No records to cleanup.\n")
                return

        total_deleted = 0
        total_failed = 0

        # Delete in reverse order of creation
        for entity in reversed(sorted(self.created_records.keys())):
            record_ids = self.created_records[entity]
            if not record_ids:
                continue

            print(f"Deleting {len(record_ids)} {entity} record(s)...")
            entity_plural = self._get_entity_plural(entity)

            for record_id in record_ids:
                try:
                    endpoint = f"{self.client.base_url}/{entity_plural}({record_id})"
                    self.client.make_request('DELETE', endpoint=endpoint)
                    print(f"  Deleted {entity} {record_id[:8]}...")
                    total_deleted += 1
                except Exception as e:
                    print(f"   Failed to delete {entity} {record_id[:8]}...: {str(e)}")
                    total_failed += 1

        print("\n" + "="*70)
        print(f"Cleanup Complete!")
        print(f"  Deleted: {total_deleted} records")
        if total_failed > 0:
            print(f"  Failed: {total_failed} records")
        print("="*70 + "\n")

    def save_created_records(self, filename: str = 'created_test_data.json'):
        """Save created record IDs to file"""
        with open(filename, 'w') as f:
            json.dump(self.created_records, f, indent=2)
        print(f"Record IDs saved to {filename}")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Create test data for MS Dynamics 365 CRM',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create data for all sales entities (5 records each)
  python %(prog)s --config config.json --module sales --count 5

  # Create data for specific entities (10 records each)
  python %(prog)s --config config.json --entities account,contact,lead --count 10

  # Create data for all modules (3 records each)
  python %(prog)s --config config.json --module all --count 3

  # Create field service data
  python %(prog)s --config config.json --module field_service --count 5

  # Create customer service data
  python %(prog)s --config config.json --module customer_service --count 5

  # Cleanup previously created data
  python %(prog)s --config config.json --cleanup
        """
    )

    parser.add_argument('--config', required=True, help='Path to configuration file')
    parser.add_argument('--module', default='sales',
                       choices=['sales', 'field_service', 'customer_service', 'all'],
                       help='Module to create data for (default: sales)')
    parser.add_argument('--entities', help='Comma-separated list of specific entities to create')
    parser.add_argument('--count', type=int, default=5,
                       help='Number of records to create per entity (default: 5)')
    parser.add_argument('--cleanup', action='store_true',
                       help='Delete previously created test records')
    parser.add_argument('--cleanup-file', default='created_test_data.json',
                       help='File containing record IDs to cleanup (default: created_test_data.json)')

    args = parser.parse_args()

    # Load configuration
    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{args.config}' not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in configuration file '{args.config}'")
        sys.exit(1)

    # Parse specific entities if provided
    specific_entities = None
    if args.entities:
        specific_entities = [e.strip() for e in args.entities.split(',')]

    # Initialize client and generator
    try:
        with Client(args.config, config) as client:
            generator = DynamicsTestDataGenerator(
                client,
                args.count,
                args.module,
                specific_entities
            )

            if args.cleanup:
                generator.cleanup_test_data(args.cleanup_file)
            else:
                generator.generate_all_test_data()
                generator.save_created_records(args.cleanup_file)
                print(f"Info: Use --cleanup flag to delete these records later\n")

    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
