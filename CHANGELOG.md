# Changelog

## 1.0.0
  * Added new entities to `INCLUDED_ENTITIES` and updated integration test accordingly.[#9](https://github.com/singer-io/tap-ms-dynamics-365-crm/pull/9)
  * `incidentresolution`, `msdyn_bookingalert`, `serviceappointment`, and custom activity entities switch from `FULL_TABLE` to `INCREMENTAL` on re-discovery. Re-discover and full-resync these streams.
  * Primary keys now come from EntityDefinitions' `PrimaryIdAttribute` instead of the `$metadata` XML `Key`
  * Added ~900 entities supported by the Precog connector (Omnichannel, Sales Insights, AI Builder, IoT, Playbooks, Customer Voice, and Dataverse platform/admin tables) to `INCLUDED_ENTITIES`

## 0.0.3
  * Added support for syncing custom entities [#8](https://github.com/singer-io/tap-ms-dynamics-365-crm/pull/8)

## 0.0.2
  * Dependency upgrade
  * Update cci config

## 0.0.1
  * Initial Commit
