import json
import os

from tap_tester.base_suite_tests.base_case import BaseCase


EXPECTED_METADATA_RAW = json.loads('''
{
    "account": {
        "primary_keys": [
            "accountid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 5
    },
    "bookableresource": {
        "primary_keys": [
            "bookableresourceid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "bookableresourcebooking": {
        "primary_keys": [
            "bookableresourcebookingid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "bookableresourcebookingheader": {
        "primary_keys": [
            "bookableresourcebookingheaderid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "bookableresourcecategory": {
        "primary_keys": [
            "bookableresourcecategoryid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "bookableresourcecategoryassn": {
        "primary_keys": [
            "bookableresourcecategoryassnid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "bookableresourcecharacteristic": {
        "primary_keys": [
            "bookableresourcecharacteristicid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "bookableresourcegroup": {
        "primary_keys": [
            "bookableresourcegroupid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "competitor": {
        "primary_keys": [
            "competitorid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "contact": {
        "primary_keys": [
            "contactid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 7
    },
    "contract": {
        "primary_keys": [
            "contractid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "contractdetail": {
        "primary_keys": [
            "contractdetailid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "contracttemplate": {
        "primary_keys": [
            "contracttemplateid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "entitlement": {
        "primary_keys": [
            "entitlementid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "entitlementchannel": {
        "primary_keys": [
            "entitlementchannelid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "entitlementcontacts": {
        "primary_keys": [
            "entitlementcontactid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "entitlemententityallocationtypemapping": {
        "primary_keys": [
            "entitlemententityallocationtypemappingid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "entitlementproducts": {
        "primary_keys": [
            "entitlementproductid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "entitlementtemplate": {
        "primary_keys": [
            "entitlementtemplateid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "entitlementtemplatechannel": {
        "primary_keys": [
            "entitlementtemplatechannelid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "entitlementtemplateproducts": {
        "primary_keys": [
            "entitlementtemplateproductid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "equipment": {
        "primary_keys": [
            "equipmentid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "feedback": {
        "primary_keys": [
            "feedbackid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "incident": {
        "primary_keys": [
            "incidentid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 16
    },
    "incidentknowledgebaserecord": {
        "primary_keys": [
            "incidentknowledgebaserecordid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "incidentresolution": {
        "primary_keys": [
            "activityid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "invoice": {
        "primary_keys": [
            "invoiceid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "invoicedetail": {
        "primary_keys": [
            "invoicedetailid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "knowledgearticle": {
        "primary_keys": [
            "knowledgearticleid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 11
    },
    "knowledgearticleincident": {
        "primary_keys": [
            "knowledgearticleincidentid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "knowledgearticleviews": {
        "primary_keys": [
            "knowledgearticleviewsid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "knowledgebaserecord": {
        "primary_keys": [
            "knowledgebaserecordid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "lead": {
        "primary_keys": [
            "leadid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 5
    },
    "msdyn_actual": {
        "primary_keys": [
            "msdyn_actualid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_agreement": {
        "primary_keys": [
            "msdyn_agreementid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_agreementbookingdate": {
        "primary_keys": [
            "msdyn_agreementbookingdateid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_agreementbookingincident": {
        "primary_keys": [
            "msdyn_agreementbookingincidentid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_agreementbookingproduct": {
        "primary_keys": [
            "msdyn_agreementbookingproductid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_agreementbookingservice": {
        "primary_keys": [
            "msdyn_agreementbookingserviceid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_bookableresourceassociation": {
        "primary_keys": [
            "msdyn_bookableresourceassociationid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_bookingalert": {
        "primary_keys": [
            "activityid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_bookingalertstatus": {
        "primary_keys": [
            "msdyn_bookingalertstatusid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_bookingjournal": {
        "primary_keys": [
            "msdyn_bookingjournalid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_bookingrule": {
        "primary_keys": [
            "msdyn_bookingruleid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_bookingsetupmetadata": {
        "primary_keys": [
            "msdyn_bookingsetupmetadataid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_bookingtimestamp": {
        "primary_keys": [
            "msdyn_bookingtimestampid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_entitlementapplication": {
        "primary_keys": [
            "msdyn_entitlementapplicationid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_fieldservicesetting": {
        "primary_keys": [
            "msdyn_fieldservicesettingid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_fieldserviceslaconfiguration": {
        "primary_keys": [
            "msdyn_fieldserviceslaconfigurationid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_flwconfiguration": {
        "primary_keys": [
            "msdyn_flwconfigurationid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_geofence": {
        "primary_keys": [
            "msdyn_geofenceid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_geofenceevent": {
        "primary_keys": [
            "msdyn_geofenceeventid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_geofencingsettings": {
        "primary_keys": [
            "msdyn_geofencingsettingsid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_geolocationsettings": {
        "primary_keys": [
            "msdyn_geolocationsettingsid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_geolocationtracking": {
        "primary_keys": [
            "msdyn_geolocationtrackingid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_incidenttype": {
        "primary_keys": [
            "msdyn_incidenttypeid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_incidenttypecharacteristic": {
        "primary_keys": [
            "msdyn_incidenttypecharacteristicid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_incidenttypeproduct": {
        "primary_keys": [
            "msdyn_incidenttypeproductid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_incidenttyperesolution": {
        "primary_keys": [
            "msdyn_incidenttyperesolutionid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_incidenttypeservice": {
        "primary_keys": [
            "msdyn_incidenttypeserviceid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_incidenttypeservicetask": {
        "primary_keys": [
            "msdyn_incidenttypeservicetaskid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_incidenttypessetup": {
        "primary_keys": [
            "msdyn_incidenttypessetupid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_inspection": {
        "primary_keys": [
            "msdyn_inspectionid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_inspectionattachment": {
        "primary_keys": [
            "msdyn_inspectionattachmentid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_inspectiondefinition": {
        "primary_keys": [
            "msdyn_inspectiondefinitionid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_inspectioninstance": {
        "primary_keys": [
            "msdyn_inspectioninstanceid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_inspectionresponse": {
        "primary_keys": [
            "msdyn_inspectionresponseid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_inventoryadjustment": {
        "primary_keys": [
            "msdyn_inventoryadjustmentid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_inventoryadjustmentproduct": {
        "primary_keys": [
            "msdyn_inventoryadjustmentproductid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_inventoryjournal": {
        "primary_keys": [
            "msdyn_inventoryjournalid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_inventorytransfer": {
        "primary_keys": [
            "msdyn_inventorytransferid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_nottoexceed": {
        "primary_keys": [
            "msdyn_nottoexceedid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_optimizationrequest": {
        "primary_keys": [
            "msdyn_optimizationrequestid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_organizationalunit": {
        "primary_keys": [
            "msdyn_organizationalunitid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_postalcode": {
        "primary_keys": [
            "msdyn_postalcodeid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_priority": {
        "primary_keys": [
            "msdyn_priorityid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_productinventory": {
        "primary_keys": [
            "msdyn_productinventoryid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_purchaseorder": {
        "primary_keys": [
            "msdyn_purchaseorderid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_purchaseorderbill": {
        "primary_keys": [
            "msdyn_purchaseorderbillid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_purchaseorderproduct": {
        "primary_keys": [
            "msdyn_purchaseorderproductid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_purchaseorderreceipt": {
        "primary_keys": [
            "msdyn_purchaseorderreceiptid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_purchaseorderreceiptproduct": {
        "primary_keys": [
            "msdyn_purchaseorderreceiptproductid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_purchaseordersubstatus": {
        "primary_keys": [
            "msdyn_purchaseordersubstatusid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_requirementchange": {
        "primary_keys": [
            "msdyn_requirementchangeid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_requirementcharacteristic": {
        "primary_keys": [
            "msdyn_requirementcharacteristicid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_requirementdependency": {
        "primary_keys": [
            "msdyn_requirementdependencyid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_requirementgroup": {
        "primary_keys": [
            "msdyn_requirementgroupid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_requirementresourcecategory": {
        "primary_keys": [
            "msdyn_requirementresourcecategoryid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_requirementresourcepreference": {
        "primary_keys": [
            "msdyn_requirementresourcepreferenceid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_requirementstatus": {
        "primary_keys": [
            "msdyn_requirementstatusid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_resolution": {
        "primary_keys": [
            "msdyn_resolutionid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_resourcepaytype": {
        "primary_keys": [
            "msdyn_resourcepaytypeid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_resourcerequirement": {
        "primary_keys": [
            "msdyn_resourcerequirementid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_resourcerequirementdetail": {
        "primary_keys": [
            "msdyn_resourcerequirementdetailid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_resourceterritory": {
        "primary_keys": [
            "msdyn_resourceterritoryid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_rma": {
        "primary_keys": [
            "msdyn_rmaid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_rmaproduct": {
        "primary_keys": [
            "msdyn_rmaproductid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_rmareceipt": {
        "primary_keys": [
            "msdyn_rmareceiptid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_rmareceiptproduct": {
        "primary_keys": [
            "msdyn_rmareceiptproductid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_rmasubstatus": {
        "primary_keys": [
            "msdyn_rmasubstatusid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_rtv": {
        "primary_keys": [
            "msdyn_rtvid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_rtvproduct": {
        "primary_keys": [
            "msdyn_rtvproductid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_rtvsubstatus": {
        "primary_keys": [
            "msdyn_rtvsubstatusid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_scheduleboardsetting": {
        "primary_keys": [
            "msdyn_scheduleboardsettingid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_servicetasktype": {
        "primary_keys": [
            "msdyn_servicetasktypeid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_shipvia": {
        "primary_keys": [
            "msdyn_shipviaid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_slakpi": {
        "primary_keys": [
            "msdyn_slakpiid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_systemuserschedulersetting": {
        "primary_keys": [
            "msdyn_systemuserschedulersettingid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_taxcode": {
        "primary_keys": [
            "msdyn_taxcodeid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_taxcodedetail": {
        "primary_keys": [
            "msdyn_taxcodedetailid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_timeentry": {
        "primary_keys": [
            "msdyn_timeentryid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_timeentrysetting": {
        "primary_keys": [
            "msdyn_timeentrysettingid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_timegroupdetail": {
        "primary_keys": [
            "msdyn_timegroupdetailid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_timeoffrequest": {
        "primary_keys": [
            "msdyn_timeoffrequestid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_trade": {
        "primary_keys": [
            "msdyn_tradeid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_tradecoverage": {
        "primary_keys": [
            "msdyn_tradecoverageid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_warehouse": {
        "primary_keys": [
            "msdyn_warehouseid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_workhourtemplate": {
        "primary_keys": [
            "msdyn_workhourtemplateid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_workorder": {
        "primary_keys": [
            "msdyn_workorderid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_workorderincident": {
        "primary_keys": [
            "msdyn_workorderincidentid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_workordernte": {
        "primary_keys": [
            "msdyn_workordernteid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_workorderproduct": {
        "primary_keys": [
            "msdyn_workorderproductid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_workorderresolution": {
        "primary_keys": [
            "msdyn_workorderresolutionid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_workorderservice": {
        "primary_keys": [
            "msdyn_workorderserviceid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_workorderservicetask": {
        "primary_keys": [
            "msdyn_workorderservicetaskid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_workordersubstatus": {
        "primary_keys": [
            "msdyn_workordersubstatusid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_workordertype": {
        "primary_keys": [
            "msdyn_workordertypeid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "opportunity": {
        "primary_keys": [
            "opportunityid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 5
    },
    "opportunityproduct": {
        "primary_keys": [
            "opportunityproductid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "phonetocaseprocess": {
        "primary_keys": [
            "businessprocessflowinstanceid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 16
    },
    "pricelevel": {
        "primary_keys": [
            "pricelevelid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "product": {
        "primary_keys": [
            "productid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 10
    },
    "productpricelevel": {
        "primary_keys": [
            "productpricelevelid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "queue": {
        "primary_keys": [
            "queueid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "queueitem": {
        "primary_keys": [
            "queueitemid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "queuemembership": {
        "primary_keys": [
            "queuemembershipid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "quote": {
        "primary_keys": [
            "quoteid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "quotedetail": {
        "primary_keys": [
            "quotedetailid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "salesliterature": {
        "primary_keys": [
            "salesliteratureid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "salesliteratureitem": {
        "primary_keys": [
            "salesliteratureitemid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "salesorder": {
        "primary_keys": [
            "salesorderid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "salesorderdetail": {
        "primary_keys": [
            "salesorderdetailid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "serviceappointment": {
        "primary_keys": [
            "activityid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "sla": {
        "primary_keys": [
            "slaid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "slaitem": {
        "primary_keys": [
            "slaitemid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "slakpiinstance": {
        "primary_keys": [
            "slakpiinstanceid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    }
}
''')


class MSDynamics365CRMBaseTest(BaseCase):
    """Setup expectations for test sub classes.

    Metadata describing streams. A bunch of shared methods that are used
    in tap-tester tests. Shared tap-specific methods (as needed).
    """
    start_date = "2019-01-01T00:00:00Z"
    PARENT_TAP_STREAM_ID = "parent-tap-stream-id"
    _expected_metadata_cache = None

    @staticmethod
    def tap_name():
        """The name of the tap."""
        return "tap-ms-dynamics-365-crm"

    @staticmethod
    def get_type():
        """The name of the tap."""
        return "platform.ms-dynamics-365-crm"

    @classmethod
    def expected_metadata(cls):
        """The expected streams and metadata about the streams."""
        if cls._expected_metadata_cache is not None:
            return cls._expected_metadata_cache

        cls._expected_metadata_cache = {
            stream_name: {
                cls.PRIMARY_KEYS: set(stream_info.get("primary_keys", [])),
                cls.REPLICATION_METHOD: stream_info.get("replication_method", cls.INCREMENTAL),
                cls.REPLICATION_KEYS: set(stream_info.get("replication_keys", [])),
                cls.OBEYS_START_DATE: stream_info.get("obeys_start_date", True),
                cls.API_LIMIT: stream_info.get("api_limit", 100),
            }
            for stream_name, stream_info in EXPECTED_METADATA_RAW.items()
        }

        return cls._expected_metadata_cache

    @staticmethod
    def get_credentials():
        """Authentication information for the test account."""
        credentials_dict = {}
        creds = {
            'auth_method': 'client_credentials',
            'client_id': 'TAP_MS_DYNAMICS_365_CRM_CLIENT_ID',
            'client_secret': 'TAP_MS_DYNAMICS_365_CRM_CLIENT_SECRET',
            'organization_uri': 'TAP_TESTER_QLIK_REDIRECT_URI',
            'tenant_id': 'TAP_MS_DYNAMICS_365_CRM_TENANT_ID',
            'refresh_token': 'TAP_MS_DYNAMICS_365_CRM_REFRESH_TOKEN',
        }

        for cred in creds:
            if cred == 'auth_method':
                credentials_dict[cred] = creds[cred]
            else:
                credentials_dict[cred] = os.getenv(creds[cred])

        return credentials_dict

    def get_properties(self, original: bool = True):
        """Configuration of properties required for the tap."""
        return_value = {
            "start_date": "2022-07-01T00:00:00Z",
            "page_size": 100
        }
        if original:
            return return_value

        return_value["start_date"] = self.start_date
        return return_value

    def expected_parent_tap_stream(self, stream=None):
        """return a dictionary with key of table name and value of parent stream"""
        parent_stream = {
            table: properties.get(self.PARENT_TAP_STREAM_ID, None)
            for table, properties in self.expected_metadata().items()}
        if not stream:
            return parent_stream
        return parent_stream[stream]
