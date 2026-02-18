# MS Dynamics 365 CRM Test Data Generator

Comprehensive test data generator for MS Dynamics 365 CRM supporting Sales, Field Service, and Customer Service modules.

## Features

- Creates realistic test data using the Faker library
- Supports **3 major modules** with 100+ entity types:
  - **Sales**: Accounts, Contacts, Leads, Opportunities, Quotes, Orders, Invoices, Products
  - **Field Service**: Work Orders, Agreements, Bookings, Resources, Inventory, Assets
  - **Customer Service**: Cases (Incidents), Knowledge Articles, Entitlements, Queues, SLAs
- Maintains relationships between entities
- Saves created record IDs for easy cleanup
- Supports batch cleanup of all created records
- Flexible entity selection (all, specific module, or specific entities)

## Prerequisites

```bash
pip install faker
```

## Configuration

Create a `config.json` file with your MS Dynamics 365 credentials:

```json
{
  "client_id": "your-client-id",
  "client_secret": "your-client-secret",
  "organization_uri": "https://your-org.crm.dynamics.com",
  "redirect_uri": "http://localhost",
  "refresh_token": "your-refresh-token",
  "start_date": "2024-01-01T00:00:00Z"
}
```

## Usage

### Basic Usage

**Create test data for Sales module (default, 5 records per entity):**
```bash
python create_test_data_comprehensive.py --config config.json
```

**Create test data for Field Service module:**
```bash
python create_test_data_comprehensive.py --config config.json --module field_service
```

**Create test data for Customer Service module:**
```bash
python create_test_data_comprehensive.py --config config.json --module customer_service
```

**Create test data for ALL modules:**
```bash
python create_test_data_comprehensive.py --config config.json --module all
```

### Advanced Options

**Specify number of records per entity:**
```bash
python create_test_data_comprehensive.py --config config.json --count 10
```

**Create specific entities only:**
```bash
python create_test_data_comprehensive.py --config config.json --entities "account,contact,lead"
```

**Field Service with 10 records per entity:**
```bash
python create_test_data_comprehensive.py --config config.json --module field_service --count 10
```

**Customer Service with specific entities:**
```bash
python create_test_data_comprehensive.py --config config.json --module customer_service --entities "incident,knowledgearticle"
```

### Cleanup Test Data

**Delete all previously created test records:**
```bash
python create_test_data_comprehensive.py --config config.json --cleanup
```

**Use custom cleanup file:**
```bash
python create_test_data_comprehensive.py --config config.json --cleanup --cleanup-file my_records.json
```

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--config` | `-c` | Path to config JSON file | config.json |
| `--count` | `-n` | Number of records per entity | 5 |
| `--module` | `-m` | Module to create data for | sales |
| `--entities` | `-e` | Comma-separated entity names | All entities in module |
| `--cleanup` | | Cleanup previously created records | False |
| `--cleanup-file` | | JSON file for tracking records | created_test_data.json |

**Valid module values:** `sales`, `field_service`, `customer_service`, `all`

## Supported Entities

### Sales Module (17 entities)
- account
- contact
- lead
- opportunity
- competitor
- quote
- quotedetail
- salesorder
- salesorderdetail
- invoice
- invoicedetail
- product
- pricelevel
- productpricelevel
- discount
- discounttype
- uom (unit of measure)

### Field Service Module (60+ entities)
- msdyn_workorder
- msdyn_workorderservice
- msdyn_workorderproduct
- msdyn_workorderincident
- msdyn_workorderservicetask
- msdyn_agreement
- msdyn_agreementbookingsetup
- msdyn_agreementinvoicesetup
- msdyn_bookableresource
- msdyn_bookableresourcebooking
- msdyn_resourcerequirement
- msdyn_timeentry
- msdyn_warehouse
- msdyn_inventoryadjustment
- msdyn_inventorytransfer
- msdyn_purchaseorder
- msdyn_customerasset
- msdyn_incidenttype
- msdyn_priority
- msdyn_servicetasktype
- ...and 40+ more entities

### Customer Service Module (36+ entities)
- incident (cases)
- knowledgearticle
- queue
- queueitem
- entitlement
- entitlementchannel
- sla
- slakpiinstance
- contract
- contractdetail
- contracttemplate
- customeraddress
- site
- service
- serviceappointment
- phonecall
- email
- task
- appointment
- letter
- fax
- ...and 15+ more entities

## What Gets Created

### Sales Module Example (--count 5)
Creates 5 records each for:
- Accounts, Contacts, Leads, Opportunities, Competitors
- Products, Price Levels, Product Price Levels
- Quotes, Quote Details, Sales Orders, Sales Order Details
- Invoices, Invoice Details, Discounts, Discount Types, Units of Measure

**Total: ~85 records (17 entities × 5)**

### Field Service Module Example (--count 5)
Creates 5 records each for:
- Work Orders, Agreements, Bookings, Resources
- Inventory items, Warehouses, Purchase Orders
- Customer Assets, Incident Types, Priorities
- Service Task Types, Time Entries, and more

**Total: ~300+ records (60+ entities × 5)**

### Customer Service Module Example (--count 5)
Creates 5 records each for:
- Cases (Incidents), Knowledge Articles, Queues
- Entitlements, SLAs, Contracts
- Service Appointments, Phone Calls, Emails
- Tasks, Appointments, and more

**Total: ~180+ records (36+ entities × 5)**

## Example Output

```
======================================================================
Creating Test Data for MS Dynamics 365 CRM - Module: SALES
======================================================================

Will create 5 record(s) for each of 17 entities

[1/17] Creating 5 account record(s)...
  Created account: Tech Innovations Inc (ID: a1b2c3d4...)
  Created account: Global Solutions Ltd (ID: e5f6g7h8...)
  Created account: Acme Corporation (ID: i9j0k1l2...)
  Created account: Digital Dynamics (ID: m3n4o5p6...)
  Created account: Future Systems (ID: q7r8s9t0...)

[2/17] Creating 5 contact record(s)...
  Created contact: John Doe (ID: u1v2w3x4...)
  Created contact: Jane Smith (ID: y5z6a7b8...)
  ...

======================================================================
Test Data Creation Complete!
  Successfully created: 85 records
======================================================================

Summary of Created Records:
----------------------------------------------------------------------
  account                             5 records
  contact                             5 records
  lead                                5 records
  opportunity                         5 records
  product                             5 records
  pricelevel                          5 records
  quote                               5 records
  invoice                             5 records
  salesorder                          5 records
  ...
----------------------------------------------------------------------
  TOTAL                              85 records

Record IDs saved to created_test_data.json
Info: Use --cleanup flag to delete these records later
```

## Entity Templates

The script includes pre-configured templates for 20+ entity types with realistic field mappings:

- **Common Fields**: name, description, email, phone, address
- **Financial Fields**: revenue, budget, price, cost
- **Date Fields**: created date, modified date, scheduled dates
- **Status Fields**: state code, status code
- **Relationship Fields**: account ID, contact ID, opportunity ID

All templates use Faker to generate realistic data that mimics production records.

## Data Relationships

The script intelligently maintains relationships:

1. **Sales Module:**
   - Contacts → linked to Accounts
   - Opportunities → linked to Accounts and Contacts
   - Quotes → linked to Opportunities and Accounts
   - Invoices → linked to Opportunities and Accounts
   - Sales Orders → linked to Opportunities and Accounts

2. **Field Service Module:**
   - Work Orders → linked to Accounts and Service Accounts
   - Bookings → linked to Work Orders and Resources
   - Agreements → linked to Service Accounts
   - Inventory → linked to Warehouses and Products

3. **Customer Service Module:**
   - Cases (Incidents) → linked to Accounts and Contacts
   - Entitlements → linked to Accounts and Contacts
   - Knowledge Articles → linked to Cases
   - Service Appointments → linked to Cases

## Record Tracking

All created record IDs are saved to `created_test_data.json`:

```json
{
  "account": [
    "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6",
    "q7r8s9t0-u1v2-w3x4-y5z6-a7b8c9d0e1f2"
  ],
  "contact": [
    "g3h4i5j6-k7l8-m9n0-o1p2-q3r4s5t6u7v8"
  ]
}
```

This file is used for cleanup operations.

## Cleanup Process

When running with `--cleanup`:

1. Loads record IDs from JSON file
2. Deletes records in **reverse order** of creation
3. Handles dependencies automatically
4. Reports success/failure for each deletion
5. Provides summary of deleted and failed deletions

```
======================================================================
Cleaning Up Test Data
======================================================================

Loaded record IDs from created_test_data.json

Deleting 5 salesorder record(s)...
  Deleted salesorder a1b2c3d4...
  Deleted salesorder e5f6g7h8...
  ...

======================================================================
Cleanup Complete!
  Deleted: 85 records
======================================================================
```

## Notes

- The script creates realistic-looking data using the Faker library
- Relationships between entities are automatically maintained
- All monetary values are randomized within reasonable ranges
- Dates are set relative to the current date
- Record IDs are saved to `created_test_data.json` for future cleanup
- Use `--cleanup` flag to delete all previously created test records
- Failed creations/deletions are reported but don't stop the process
- Entity names are case-insensitive

## Troubleshooting

### Authentication Errors
- Verify your credentials in `config.json`
- Ensure your refresh token is valid
- Check that your app registration has the necessary permissions
- Confirm the organization URI is correct

### Permission Errors
- Verify your user account has permissions to create/delete records
- Check that your app registration has the required API permissions
- Required permission: `Dynamics CRM API` with user impersonation

### Entity Not Found Errors
- Ensure the entity exists in your CRM instance
- Check that the module (Sales, Field Service, Customer Service) is installed
- Some entities may require additional licenses

### API Errors
- Check the entity names and field names match your CRM version
- Some custom fields may need to be adjusted based on your CRM configuration
- Review the error messages for specific field validation issues
- Verify required fields are being populated

### Relationship Errors
- Ensure parent records are created before child records
- The script handles this automatically, but manual entity selection may cause issues
- When using `--entities`, include parent entities (e.g., include "account" when creating "contact")

### Cleanup Failures
- Some records may have dependencies preventing deletion
- Check for cascading delete rules in your CRM configuration
- Re-run cleanup after resolving dependencies
- Manual cleanup may be required for some records

## Best Practices

1. **Start Small**: Begin with `--count 1` to test connectivity and permissions
2. **Module by Module**: Test one module at a time before using `--module all`
3. **Track Your Data**: Keep the `created_test_data.json` file for cleanup
4. **Test Cleanup**: Always test cleanup in a development environment first
5. **Monitor Limits**: Be aware of API rate limits when creating large datasets
6. **Use Specific Entities**: When testing specific features, use `--entities` to create only what you need
