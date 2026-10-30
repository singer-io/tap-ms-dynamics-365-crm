import json
import os

from tap_tester.base_suite_tests.base_case import BaseCase
from tap_tester import menagerie, runner


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
    "campaign": {
        "primary_keys": [
            "campaignid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "campaignactivity": {
        "primary_keys": [
            "activityid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "campaignactivityitem": {
        "primary_keys": [
            "campaignactivityitemid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "campaignitem": {
        "primary_keys": [
            "campaignitemid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "campaignresponse": {
        "primary_keys": [
            "activityid"
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
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
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
    "list": {
        "primary_keys": [
            "listid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "listmember": {
        "primary_keys": [
            "listmemberid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
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
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
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
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
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
    },
    "accountleads": {
        "primary_keys": ["accountleadid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "activityparty": {
        "primary_keys": ["activitypartyid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "activitypointer": {
        "primary_keys": ["activityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "annotation": {
        "primary_keys": ["annotationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "appointment": {
        "primary_keys": ["activityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "bookingstatus": {
        "primary_keys": ["bookingstatusid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "businessunit": {
        "primary_keys": ["businessunitid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "contactleads": {
        "primary_keys": ["contactleadid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "discount": {
        "primary_keys": ["discountid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "discounttype": {
        "primary_keys": ["discounttypeid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "email": {
        "primary_keys": ["activityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "leadaddress": {
        "primary_keys": ["leadaddressid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "leadcompetitors": {
        "primary_keys": ["leadcompetitorid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "leadproduct": {
        "primary_keys": ["leadproductid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "leadtoopportunitysalesprocess": {
        "primary_keys": ["businessprocessflowinstanceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_customerasset": {
        "primary_keys": ["msdyn_customerassetid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_customerassetcategory": {
        "primary_keys": ["msdyn_customerassetcategoryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_segment": {
        "primary_keys": ["msdyn_segmentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdynmkt_compliancesettings4": {
        "primary_keys": ["msdynmkt_compliancesettings4id"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdynmkt_msdynmkt_purpose_msdynmkt_compliancev4": {
        "primary_keys": ["msdynmkt_msdynmkt_purpose_msdynmkt_compliancev4id"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdynmkt_contactpointconsent4": {
        "primary_keys": ["msdynmkt_contactpointconsent4id"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdynmkt_preferencecenter": {
        "primary_keys": ["msdynmkt_preferencecenterid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdynmkt_purpose": {
        "primary_keys": ["msdynmkt_purposeid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdynmkt_topic": {
        "primary_keys": ["msdynmkt_topicid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msfp_question": {
        "primary_keys": ["msfp_questionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msfp_questionresponse": {
        "primary_keys": ["msfp_questionresponseid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msfp_survey": {
        "primary_keys": ["msfp_surveyid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msfp_surveyinvite": {
        "primary_keys": ["activityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msfp_surveyresponse": {
        "primary_keys": ["activityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "opportunityclose": {
        "primary_keys": ["activityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "opportunitycompetitors": {
        "primary_keys": ["opportunitycompetitorid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "opportunitysalesprocess": {
        "primary_keys": ["businessprocessflowinstanceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "orderclose": {
        "primary_keys": ["activityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "phonecall": {
        "primary_keys": ["activityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "quoteclose": {
        "primary_keys": ["activityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "recurringappointmentmaster": {
        "primary_keys": ["activityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "systemuser": {
        "primary_keys": ["systemuserid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "task": {
        "primary_keys": ["activityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "team": {
        "primary_keys": ["teamid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "teammembership": {
        "primary_keys": ["teammembershipid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "territory": {
        "primary_keys": ["territoryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "transactioncurrency": {
        "primary_keys": ["transactioncurrencyid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "uom": {
        "primary_keys": ["uomid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "uomschedule": {
        "primary_keys": ["uomscheduleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "aciviewmapper": {
        "primary_keys": ["aciviewmapperid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "actioncard": {
        "primary_keys": ["actioncardid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "actioncarduserstate": {
        "primary_keys": ["actioncarduserstateid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "activityfileattachment": {
        "primary_keys": ["activityfileattachmentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "activitymimeattachment": {
        "primary_keys": ["activitymimeattachmentid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "activitymonitor": {
        "primary_keys": ["activitymonitorid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "adminsettingsentity": {
        "primary_keys": ["adminsettingsentityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "adx_portalcomment": {
        "primary_keys": ["activityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "annualfiscalcalendar": {
        "primary_keys": ["userfiscalcalendarid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "appaction": {
        "primary_keys": ["appactionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "appaction_appactionrule_classicrules": {
        "primary_keys": ["appaction_appactionrule_classicrulesid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "appactionmigration": {
        "primary_keys": ["appactionmigrationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "appactionrule": {
        "primary_keys": ["appactionruleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "appactionrule_webresource_scripts": {
        "primary_keys": ["appactionrule_webresource_scriptsid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "appconfig": {
        "primary_keys": ["appconfigid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "appconfiginstance": {
        "primary_keys": ["appconfiginstanceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "appconfigmaster": {
        "primary_keys": ["appconfigmasterid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "applicationuser": {
        "primary_keys": ["applicationuserid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "applicationuserprofile": {
        "primary_keys": ["applicationuserprofileid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "applicationuserrole": {
        "primary_keys": ["applicationuserroleid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "appmodule": {
        "primary_keys": ["appmoduleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "appmodulecomponent": {
        "primary_keys": ["appmodulecomponentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "appmoduleroles": {
        "primary_keys": ["appmoduleroleid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "appnotification": {
        "primary_keys": ["appnotificationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "asyncoperation": {
        "primary_keys": ["asyncoperationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "attachment": {
        "primary_keys": ["attachmentid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "attribute": {
        "primary_keys": ["attributeid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "attributeimageconfig": {
        "primary_keys": ["attributeimageconfigid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "audit": {
        "primary_keys": ["auditid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "availabletimes": {
        "primary_keys": ["availabletimesid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "availabletimesdatasource": {
        "primary_keys": ["availabletimesdatasourceid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "bot": {
        "primary_keys": ["botid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "bot_botcomponent": {
        "primary_keys": ["bot_botcomponentid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "bot_environmentvariabledefinition": {
        "primary_keys": ["bot_environmentvariabledefinitionid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "botcomponent": {
        "primary_keys": ["botcomponentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "botcomponent_botcomponent": {
        "primary_keys": ["botcomponent_botcomponentid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "botcomponent_environmentvariabledefinition": {
        "primary_keys": ["botcomponent_environmentvariabledefinitionid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "botcomponent_workflow": {
        "primary_keys": ["botcomponent_workflowid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "bulkdeletefailure": {
        "primary_keys": ["bulkdeletefailureid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "bulkdeleteoperation": {
        "primary_keys": ["bulkdeleteoperationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "bulkoperation": {
        "primary_keys": ["activityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "bulkoperationlog": {
        "primary_keys": ["bulkoperationlogid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "businessunitnewsarticle": {
        "primary_keys": ["businessunitnewsarticleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "calendar": {
        "primary_keys": ["calendarid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "callbackregistration": {
        "primary_keys": ["callbackregistrationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "canvasapp": {
        "primary_keys": ["canvasappid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "card": {
        "primary_keys": ["cardid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "catalog": {
        "primary_keys": ["catalogid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "catalogassignment": {
        "primary_keys": ["catalogassignmentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "category": {
        "primary_keys": ["categoryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "channelaccessprofileentityaccesslevel": {
        "primary_keys": ["channelaccessprofileentityaccesslevelid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "characteristic": {
        "primary_keys": ["characteristicid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "chat": {
        "primary_keys": ["activityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "columnmapping": {
        "primary_keys": ["columnmappingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "competitoraddress": {
        "primary_keys": ["competitoraddressid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "competitorproduct": {
        "primary_keys": ["competitorproductid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "competitorsalesliterature": {
        "primary_keys": ["competitorsalesliteratureid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "connection": {
        "primary_keys": ["connectionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "connectioninstance": {
        "primary_keys": ["connectioninstanceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "connectionreference": {
        "primary_keys": ["connectionreferenceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "connectionrole": {
        "primary_keys": ["connectionroleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "connectionroleassociation": {
        "primary_keys": ["connectionroleassociationid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "connector": {
        "primary_keys": ["connectorid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "constraintbasedgroup": {
        "primary_keys": ["constraintbasedgroupid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "contactinvoices": {
        "primary_keys": ["contactinvoiceid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "contactorders": {
        "primary_keys": ["contactorderid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "contactquotes": {
        "primary_keys": ["contactquoteid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "conversationtranscript": {
        "primary_keys": ["conversationtranscriptid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "customapi": {
        "primary_keys": ["customapiid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "customapirequestparameter": {
        "primary_keys": ["customapirequestparameterid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "customapiresponseproperty": {
        "primary_keys": ["customapiresponsepropertyid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "customcontrol": {
        "primary_keys": ["customcontrolid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "customcontroldefaultconfig": {
        "primary_keys": ["customcontroldefaultconfigid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "customcontrolresource": {
        "primary_keys": ["customcontrolresourceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "customeraddress": {
        "primary_keys": ["customeraddressid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "datalakefolder": {
        "primary_keys": ["datalakefolderid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "datalakefolderpermission": {
        "primary_keys": ["datalakefolderpermissionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "datalakeworkspace": {
        "primary_keys": ["datalakeworkspaceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "datalakeworkspacepermission": {
        "primary_keys": ["datalakeworkspacepermissionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "dataprocessingconfiguration": {
        "primary_keys": ["dataprocessingconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "desktopflowbinary": {
        "primary_keys": ["desktopflowbinaryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "displaystring": {
        "primary_keys": ["displaystringid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "documenttemplate": {
        "primary_keys": ["documenttemplateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "duplicaterecord": {
        "primary_keys": ["duplicateid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "duplicaterule": {
        "primary_keys": ["duplicateruleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "duplicaterulecondition": {
        "primary_keys": ["duplicateruleconditionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "dynamicproperty": {
        "primary_keys": ["dynamicpropertyid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "dynamicpropertyassociation": {
        "primary_keys": ["dynamicpropertyassociationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "dynamicpropertyinstance": {
        "primary_keys": ["dynamicpropertyinstanceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "dynamicpropertyoptionsetitem": {
        "primary_keys": ["dynamicpropertyoptionsetvalueid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "emailserverprofile": {
        "primary_keys": ["emailserverprofileid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "entity": {
        "primary_keys": ["entityid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "entityanalyticsconfig": {
        "primary_keys": ["entityanalyticsconfigid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "entitydataprovider": {
        "primary_keys": ["entitydataproviderid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "entityimageconfig": {
        "primary_keys": ["entityimageconfigid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "entitykey": {
        "primary_keys": ["entitykeyid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "entityrelationship": {
        "primary_keys": ["entityrelationshipid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "environmentvariabledefinition": {
        "primary_keys": ["environmentvariabledefinitionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "environmentvariablevalue": {
        "primary_keys": ["environmentvariablevalueid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "exchangesyncidmapping": {
        "primary_keys": ["exchangesyncidmappingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "expiredprocess": {
        "primary_keys": ["businessprocessflowinstanceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "exportsolutionupload": {
        "primary_keys": ["exportsolutionuploadid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "fax": {
        "primary_keys": ["activityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "featurecontrolsetting": {
        "primary_keys": ["featurecontrolsettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "fieldpermission": {
        "primary_keys": ["fieldpermissionid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "fieldsecurityprofile": {
        "primary_keys": ["fieldsecurityprofileid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "fileattachment": {
        "primary_keys": ["fileattachmentid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "fixedmonthlyfiscalcalendar": {
        "primary_keys": ["userfiscalcalendarid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "flowmachine": {
        "primary_keys": ["flowmachineid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "flowmachinegroup": {
        "primary_keys": ["flowmachinegroupid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "flowmachineimage": {
        "primary_keys": ["flowmachineimageid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "flowmachineimageversion": {
        "primary_keys": ["flowmachineimageversionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "flowmachinenetwork": {
        "primary_keys": ["flowmachinenetworkid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "flowsession": {
        "primary_keys": ["flowsessionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "goal": {
        "primary_keys": ["goalid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "goalrollupquery": {
        "primary_keys": ["goalrollupqueryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "import": {
        "primary_keys": ["importid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "importdata": {
        "primary_keys": ["importdataid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "importentitymapping": {
        "primary_keys": ["importentitymappingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "importfile": {
        "primary_keys": ["importfileid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "importjob": {
        "primary_keys": ["importjobid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "importlog": {
        "primary_keys": ["importlogid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "importmap": {
        "primary_keys": ["importmapid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "interactionforemail": {
        "primary_keys": ["interactionforemailid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "kbarticle": {
        "primary_keys": ["kbarticleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "kbarticlecomment": {
        "primary_keys": ["kbarticlecommentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "kbarticletemplate": {
        "primary_keys": ["kbarticletemplateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "keyvaultreference": {
        "primary_keys": ["keyvaultreferenceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "languagelocale": {
        "primary_keys": ["languagelocaleid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "letter": {
        "primary_keys": ["activityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "listoperation": {
        "primary_keys": ["listoperationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "mailbox": {
        "primary_keys": ["mailboxid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "mailboxtrackingfolder": {
        "primary_keys": ["mailboxtrackingfolderid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "mailmergetemplate": {
        "primary_keys": ["mailmergetemplateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "managedidentity": {
        "primary_keys": ["managedidentityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "marketingformdisplayattributes": {
        "primary_keys": ["marketingformdisplayattributesid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "metric": {
        "primary_keys": ["metricid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "mobileofflineprofile": {
        "primary_keys": ["mobileofflineprofileid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "mobileofflineprofileitem": {
        "primary_keys": ["mobileofflineprofileitemid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "mobileofflineprofileitemassociation": {
        "primary_keys": ["mobileofflineprofileitemassociationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "mobileofflineprofileitemfilter": {
        "primary_keys": ["mobileofflineprofileitemfilterid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "monthlyfiscalcalendar": {
        "primary_keys": ["userfiscalcalendarid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_accountkpiitem": {
        "primary_keys": ["msdyn_accountkpiitemid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_actioncardactionstat": {
        "primary_keys": ["msdyn_actioncardactionstatid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_actioncardregarding": {
        "primary_keys": ["msdyn_actioncardregardingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_actioncardrolesetting": {
        "primary_keys": ["msdyn_actioncardrolesettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_actioncardstataggregation": {
        "primary_keys": ["msdyn_actioncardstataggregationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_activityanalysiscleanupstate": {
        "primary_keys": ["msdyn_activityanalysiscleanupstateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_activityanalysisconfig": {
        "primary_keys": ["msdyn_activityanalysisconfigid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_adaptivecardconfiguration": {
        "primary_keys": ["msdyn_adaptivecardconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_adjustmenthistory": {
        "primary_keys": ["msdyn_adjustmenthistoryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_adminappstate": {
        "primary_keys": ["msdyn_adminappstateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_agentcapacityupdatehistory": {
        "primary_keys": ["msdyn_agentcapacityupdatehistoryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_agentresourceforecasting": {
        "primary_keys": ["msdyn_agentresourceforecastingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_agentstatushistory": {
        "primary_keys": ["msdyn_agentstatushistoryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aibdataset": {
        "primary_keys": ["msdyn_aibdatasetid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aibdatasetfile": {
        "primary_keys": ["msdyn_aibdatasetfileid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aibdatasetrecord": {
        "primary_keys": ["msdyn_aibdatasetrecordid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aibdatasetscontainer": {
        "primary_keys": ["msdyn_aibdatasetscontainerid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aibfeedbackloop": {
        "primary_keys": ["msdyn_aibfeedbackloopid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aibfile": {
        "primary_keys": ["msdyn_aibfileid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aibfileattacheddata": {
        "primary_keys": ["msdyn_aibfileattacheddataid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aiconfiguration": {
        "primary_keys": ["msdyn_aiconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aicontactsuggestion": {
        "primary_keys": ["msdyn_aicontactsuggestionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aifptrainingdocument": {
        "primary_keys": ["msdyn_aifptrainingdocumentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aimodel": {
        "primary_keys": ["msdyn_aimodelid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aiodimage": {
        "primary_keys": ["msdyn_aiodimageid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aiodlabel": {
        "primary_keys": ["msdyn_aiodlabelid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aiodlabel_msdyn_aiconfiguration": {
        "primary_keys": ["msdyn_aiodlabel_msdyn_aiconfigurationid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_aiodtrainingboundingbox": {
        "primary_keys": ["msdyn_aiodtrainingboundingboxid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aiodtrainingimage": {
        "primary_keys": ["msdyn_aiodtrainingimageid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aitemplate": {
        "primary_keys": ["msdyn_aitemplateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_analysiscomponent": {
        "primary_keys": ["msdyn_analysiscomponentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_analysisjob": {
        "primary_keys": ["msdyn_analysisjobid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_analysisresult": {
        "primary_keys": ["msdyn_analysisresultid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_analysisresultdetail": {
        "primary_keys": ["msdyn_analysisresultdetailid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_analytics": {
        "primary_keys": ["msdyn_analyticsid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_analyticsadminsettings": {
        "primary_keys": ["msdyn_analyticsadminsettingsid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_analyticsforcs": {
        "primary_keys": ["msdyn_analyticsforcsid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_appconfig_msdyn_channelprovider": {
        "primary_keys": ["msdyn_appconfig_msdyn_channelproviderid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_appconfiguration": {
        "primary_keys": ["msdyn_appconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_appconfiguration_applicationextension": {
        "primary_keys": ["msdyn_appconfiguration_applicationextensionid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_appconfiguration_sessiontemplate": {
        "primary_keys": ["msdyn_appconfiguration_sessiontemplateid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_appconfiguration_systemuser": {
        "primary_keys": ["msdyn_appconfiguration_systemuserid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_appinsightsmetadata": {
        "primary_keys": ["msdyn_appinsightsmetadataid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_applicationextension": {
        "primary_keys": ["msdyn_applicationextensionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_applicationtabtemplate": {
        "primary_keys": ["msdyn_applicationtabtemplateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_assetcategorytemplateassociation": {
        "primary_keys": ["msdyn_assetcategorytemplateassociationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_assettemplateassociation": {
        "primary_keys": ["msdyn_assettemplateassociationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_assignmentconfiguration": {
        "primary_keys": ["msdyn_assignmentconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_assignmentconfigurationstep": {
        "primary_keys": ["msdyn_assignmentconfigurationstepid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_assignmentmap": {
        "primary_keys": ["msdyn_assignmentmapid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_assignmentrule": {
        "primary_keys": ["msdyn_assignmentruleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_attribute": {
        "primary_keys": ["msdyn_attributeid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_attributeinfluencestatistics": {
        "primary_keys": ["msdyn_attributeinfluencestatisticsid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_attributevalue": {
        "primary_keys": ["msdyn_attributevalueid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_authenticationsettings": {
        "primary_keys": ["msdyn_authenticationsettingsid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_authsettingsentry": {
        "primary_keys": ["msdyn_authsettingsentryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_autocapturerule": {
        "primary_keys": ["msdyn_autocaptureruleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_autocapturesettings": {
        "primary_keys": ["msdyn_autocapturesettingsid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_bookableresourcecapacityprofile": {
        "primary_keys": ["msdyn_bookableresourcecapacityprofileid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_callablecontext": {
        "primary_keys": ["msdyn_callablecontextid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_callablecontext_msdyn_playbooktemplate": {
        "primary_keys": ["msdyn_callablecontext_msdyn_playbooktemplateid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_cannedmessage": {
        "primary_keys": ["msdyn_cannedmessageid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_capacityprofile": {
        "primary_keys": ["msdyn_capacityprofileid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_caseenrichment": {
        "primary_keys": ["msdyn_caseenrichmentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_casesuggestionrequestpayload": {
        "primary_keys": ["msdyn_casesuggestionrequestpayloadid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_casesuggestionsdatasource": {
        "primary_keys": ["msdyn_casesuggestionsdatasourceid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_casetopic": {
        "primary_keys": ["msdyn_casetopicid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_casetopic_incident": {
        "primary_keys": ["msdyn_casetopic_incidentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_casetopicsetting": {
        "primary_keys": ["msdyn_casetopicsettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_casetopicsummary": {
        "primary_keys": ["msdyn_casetopicsummaryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_cdsentityengagementctx": {
        "primary_keys": ["msdyn_cdsentityengagementctxid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_channelcapability": {
        "primary_keys": ["msdyn_channelcapabilityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_channelprovider": {
        "primary_keys": ["msdyn_channelproviderid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_collabgraphresource": {
        "primary_keys": ["msdyn_collabgraphresourceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_componentlayer": {
        "primary_keys": ["msdyn_componentlayerid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_componentlayerdatasource": {
        "primary_keys": ["msdyn_componentlayerdatasourceid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_connectordatasource": {
        "primary_keys": ["msdyn_connectordatasourceid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_contactkpiitem": {
        "primary_keys": ["msdyn_contactkpiitemid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_contactsuggestionrule": {
        "primary_keys": ["msdyn_contactsuggestionruleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_contactsuggestionruleset": {
        "primary_keys": ["msdyn_contactsuggestionrulesetid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_conversationaction": {
        "primary_keys": ["msdyn_conversationactionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_conversationactionlocale": {
        "primary_keys": ["msdyn_conversationactionlocaleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_conversationdata": {
        "primary_keys": ["msdyn_conversationdataid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_conversationinsight": {
        "primary_keys": ["msdyn_conversationinsightid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_conversationmessageblock": {
        "primary_keys": ["msdyn_conversationmessageblockid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_crmconnection": {
        "primary_keys": ["msdyn_crmconnectionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_csadminconfig": {
        "primary_keys": ["msdyn_csadminconfigid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_customapirulesetconfiguration": {
        "primary_keys": ["msdyn_customapirulesetconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_customcontrolextendedsettings": {
        "primary_keys": ["msdyn_customcontrolextendedsettingsid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_customerassetattachment": {
        "primary_keys": ["msdyn_customerassetattachmentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_customeremailcommunication": {
        "primary_keys": ["msdyn_customeremailcommunicationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_dataanalyticscustomizedreport": {
        "primary_keys": ["msdyn_dataanalyticscustomizedreportid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_dataanalyticsdataset": {
        "primary_keys": ["msdyn_dataanalyticsdatasetid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_dataanalyticsreport": {
        "primary_keys": ["msdyn_dataanalyticsreportid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_dataanalyticsreport_csrmanager": {
        "primary_keys": ["msdyn_dataanalyticsreport_csrmanagerid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_dataanalyticsreport_forecast": {
        "primary_keys": ["msdyn_dataanalyticsreport_forecastid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_dataanalyticsreport_ksinsights": {
        "primary_keys": ["msdyn_dataanalyticsreport_ksinsightsid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_dataanalyticsreport_sareporting": {
        "primary_keys": ["msdyn_dataanalyticsreport_sareportingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_dataanalyticsworkspace": {
        "primary_keys": ["msdyn_dataanalyticsworkspaceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_databaseversion": {
        "primary_keys": ["msdyn_databaseversionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_dataflow": {
        "primary_keys": ["msdyn_dataflowid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_dataflowrefreshhistory": {
        "primary_keys": ["msdyn_dataflowrefreshhistoryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_datahygienesettinginfo": {
        "primary_keys": ["msdyn_datahygienesettinginfoid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_datainsightsandanalyticsfeature": {
        "primary_keys": ["msdyn_datainsightsandanalyticsfeatureid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_datalakeds": {
        "primary_keys": ["msdyn_datalakedsid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_dealmanageraccess": {
        "primary_keys": ["msdyn_dealmanageraccessid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_dealmanagersettings": {
        "primary_keys": ["msdyn_dealmanagersettingsid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_decisioncontract": {
        "primary_keys": ["msdyn_decisioncontractid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_decisionruleset": {
        "primary_keys": ["msdyn_decisionrulesetid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_distributedlock": {
        "primary_keys": ["msdyn_distributedlockid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_duplicatedetectionpluginrun": {
        "primary_keys": ["msdyn_duplicatedetectionpluginrunid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_duplicateleadmapping": {
        "primary_keys": ["msdyn_duplicateleadmappingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_effortpredictionresult": {
        "primary_keys": ["msdyn_effortpredictionresultid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_entityconfig": {
        "primary_keys": ["msdyn_entityconfigid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_entitydeltachange": {
        "primary_keys": ["msdyn_entitydeltachangeid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_entitylinkchatconfiguration": {
        "primary_keys": ["msdyn_entitylinkchatconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_entityrankingrule": {
        "primary_keys": ["msdyn_entityrankingruleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_entityrefreshhistory": {
        "primary_keys": ["msdyn_entityrefreshhistoryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_entityroutingconfiguration": {
        "primary_keys": ["msdyn_entityroutingconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_extendedusersetting": {
        "primary_keys": ["msdyn_extendedusersettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_federatedarticle": {
        "primary_keys": ["msdyn_federatedarticleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_federatedarticleincident": {
        "primary_keys": ["msdyn_federatedarticleincidentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_fileuploadstatustracker": {
        "primary_keys": ["msdyn_fileuploadstatustrackerid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_flowcardtype": {
        "primary_keys": ["msdyn_flowcardtypeid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_forecast": {
        "primary_keys": ["msdyn_forecastid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_forecastconfiguration": {
        "primary_keys": ["msdyn_forecastconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_forecastdefinition": {
        "primary_keys": ["msdyn_forecastdefinitionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_forecastingcache": {
        "primary_keys": ["msdyn_forecastingcacheid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_forecastinsight": {
        "primary_keys": ["msdyn_forecastinsightid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_forecastinstance": {
        "primary_keys": ["msdyn_forecastinstanceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_forecastpredictiondata": {
        "primary_keys": ["msdyn_forecastpredictiondataid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_forecastpredictionstatus": {
        "primary_keys": ["msdyn_forecastpredictionstatusid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_forecastrecurrence": {
        "primary_keys": ["msdyn_forecastrecurrenceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_forecastsettingsandsummary": {
        "primary_keys": ["msdyn_forecastsettingsandsummaryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_functionallocation": {
        "primary_keys": ["msdyn_functionallocationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_gdprdata": {
        "primary_keys": ["msdyn_gdprdataid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_helppage": {
        "primary_keys": ["msdyn_helppageid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_icebreakersconfig": {
        "primary_keys": ["msdyn_icebreakersconfigid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_iermlmodel": {
        "primary_keys": ["msdyn_iermlmodelid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_iermltraining": {
        "primary_keys": ["msdyn_iermltrainingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_inboxconfiguration": {
        "primary_keys": ["msdyn_inboxconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_incident_msdyn_customerasset": {
        "primary_keys": ["msdyn_incident_msdyn_customerassetid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_insightsstorevirtualentity": {
        "primary_keys": ["msdyn_insightsstorevirtualentityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_integratedsearchprovider": {
        "primary_keys": ["msdyn_integratedsearchproviderid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_iotalert": {
        "primary_keys": ["msdyn_iotalertid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_iotdevice": {
        "primary_keys": ["msdyn_iotdeviceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_iotdevicecategory": {
        "primary_keys": ["msdyn_iotdevicecategoryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_iotdevicecategorycommands": {
        "primary_keys": ["msdyn_iotdevicecategorycommandsid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_iotdevicecommand": {
        "primary_keys": ["msdyn_iotdevicecommandid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_iotdevicecommanddefinition": {
        "primary_keys": ["msdyn_iotdevicecommanddefinitionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_iotdevicecommandparameters": {
        "primary_keys": ["msdyn_iotdevicecommandparametersid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_iotdevicedatahistory": {
        "primary_keys": ["msdyn_iotdevicedatahistoryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_iotdeviceproperty": {
        "primary_keys": ["msdyn_iotdevicepropertyid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_iotdeviceregistrationhistory": {
        "primary_keys": ["msdyn_iotdeviceregistrationhistoryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_iotdevicevisualizationconfiguration": {
        "primary_keys": ["msdyn_iotdevicevisualizationconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_iotfieldmapping": {
        "primary_keys": ["msdyn_iotfieldmappingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_iotpropertydefinition": {
        "primary_keys": ["msdyn_iotpropertydefinitionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_iotprovider": {
        "primary_keys": ["msdyn_iotproviderid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_iotproviderinstance": {
        "primary_keys": ["msdyn_iotproviderinstanceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_iotsettings": {
        "primary_keys": ["msdyn_iotsettingsid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_iottocaseprocess": {
        "primary_keys": ["businessprocessflowinstanceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_kalanguagesetting": {
        "primary_keys": ["msdyn_kalanguagesettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_kbattachment": {
        "primary_keys": ["msdyn_kbattachmentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_kbenrichment": {
        "primary_keys": ["msdyn_kbenrichmentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_kbkeywordsdescsuggestionsetting": {
        "primary_keys": ["msdyn_kbkeywordsdescsuggestionsettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_kmfederatedsearchconfig": {
        "primary_keys": ["msdyn_kmfederatedsearchconfigid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_kmpersonalizationsetting": {
        "primary_keys": ["msdyn_kmpersonalizationsettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_knowledgearticleimage": {
        "primary_keys": ["msdyn_knowledgearticleimageid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_knowledgearticlesuggestiondatasource": {
        "primary_keys": ["msdyn_knowledgearticlesuggestiondatasourceid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_knowledgearticletemplate": {
        "primary_keys": ["msdyn_knowledgearticletemplateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_knowledgeinteractioninsight": {
        "primary_keys": ["msdyn_knowledgeinteractioninsightid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_knowledgemanagementsetting": {
        "primary_keys": ["msdyn_knowledgemanagementsettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_knowledgepersonalfilter": {
        "primary_keys": ["msdyn_knowledgepersonalfilterid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_knowledgesearchfilter": {
        "primary_keys": ["msdyn_knowledgesearchfilterid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_knowledgesearchinsight": {
        "primary_keys": ["msdyn_knowledgesearchinsightid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_kpieventdata": {
        "primary_keys": ["msdyn_kpieventdataid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_kpieventdefinition": {
        "primary_keys": ["msdyn_kpieventdefinitionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_leadhygienesetting": {
        "primary_keys": ["msdyn_leadhygienesettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_leadkpiitem": {
        "primary_keys": ["msdyn_leadkpiitemid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_leadmodelconfig": {
        "primary_keys": ["msdyn_leadmodelconfigid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_linkedentityattributevalidity": {
        "primary_keys": ["msdyn_linkedentityattributevalidityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_liveconversation": {
        "primary_keys": ["msdyn_liveconversationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_liveworkitemevent": {
        "primary_keys": ["msdyn_liveworkitemeventid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_liveworkstream": {
        "primary_keys": ["msdyn_liveworkstreamid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_liveworkstreamcapacityprofile": {
        "primary_keys": ["msdyn_liveworkstreamcapacityprofileid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_macrosession": {
        "primary_keys": ["msdyn_macrosessionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_maskingrule": {
        "primary_keys": ["msdyn_maskingruleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_masterentityroutingconfiguration": {
        "primary_keys": ["msdyn_masterentityroutingconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_migrationtracker": {
        "primary_keys": ["msdyn_migrationtrackerid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_modelpreviewstatus": {
        "primary_keys": ["msdyn_modelpreviewstatusid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_msdyn_attributevalue_systemuser": {
        "primary_keys": ["msdyn_msdyn_attributevalue_systemuserid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_msdyn_cannedmessage_liveworkstream": {
        "primary_keys": ["msdyn_msdyn_cannedmessage_liveworkstreamid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_msdyn_cannedmessage_msdyn_octag": {
        "primary_keys": ["msdyn_msdyn_cannedmessage_msdyn_octagid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_msdyn_customerasset_knowledgearticl": {
        "primary_keys": ["msdyn_msdyn_customerasset_knowledgearticlid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_msdyn_customerasset_knowledgebasere": {
        "primary_keys": ["msdyn_msdyn_customerasset_knowledgebasereid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_msdyn_functionallocation_account": {
        "primary_keys": ["msdyn_msdyn_functionallocation_accountid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_msdyn_kbattachment_knowledgearticle": {
        "primary_keys": ["msdyn_msdyn_kbattachment_knowledgearticleid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_msdyn_ocliveworkitem_knowledgeartic": {
        "primary_keys": ["msdyn_msdyn_ocliveworkitem_knowledgearticid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_msdyn_ocliveworkitem_knowledgebaser": {
        "primary_keys": ["msdyn_msdyn_ocliveworkitem_knowledgebaserid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_msdyn_ocrichobject_liveworkstream": {
        "primary_keys": ["msdyn_msdyn_ocrichobject_liveworkstreamid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_msdyn_ocrichobject_msdyn_octag": {
        "primary_keys": ["msdyn_msdyn_ocrichobject_msdyn_octagid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_msdyn_paneconfig_msdyn_appconfig": {
        "primary_keys": ["msdyn_msdyn_paneconfig_msdyn_appconfigid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_msdyn_personalmessage_msdyn_octag": {
        "primary_keys": ["msdyn_msdyn_personalmessage_msdyn_octagid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_msdyn_prod_actioninputparameter_msdyn_par": {
        "primary_keys": ["msdyn_msdyn_prod_actioninputparameter_msdyn_parid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_msdyn_prod_actionoutputparameter_msdyn_pa": {
        "primary_keys": ["msdyn_msdyn_prod_actionoutputparameter_msdyn_paid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_msdyn_prod_agentscript_msdyn_sessiontempl": {
        "primary_keys": ["msdyn_msdyn_prod_agentscript_msdyn_sessiontemplid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_msteamssetting": {
        "primary_keys": ["msdyn_msteamssettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_msteamssettingsv2": {
        "primary_keys": ["msdyn_msteamssettingsv2id"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_notesanalysisconfig": {
        "primary_keys": ["msdyn_notesanalysisconfigid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_notificationfield": {
        "primary_keys": ["msdyn_notificationfieldid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_notificationtemplate": {
        "primary_keys": ["msdyn_notificationtemplateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_notificationtemplate_notificationfield": {
        "primary_keys": ["msdyn_notificationtemplate_notificationfieldid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_oc_geolocationprovider": {
        "primary_keys": ["msdyn_oc_geolocationproviderid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocautoblockrule": {
        "primary_keys": ["msdyn_ocautoblockruleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocbotchannelregistration": {
        "primary_keys": ["msdyn_ocbotchannelregistrationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocbotchannelregistrationsecret": {
        "primary_keys": ["msdyn_ocbotchannelregistrationsecretid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_occhannelapiconversationprivilege": {
        "primary_keys": ["msdyn_occhannelapiconversationprivilegeid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_occhannelapimessageprivilege": {
        "primary_keys": ["msdyn_occhannelapimessageprivilegeid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_occhannelapimethodmapping": {
        "primary_keys": ["msdyn_occhannelapimethodmappingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_occhannelconfiguration": {
        "primary_keys": ["msdyn_occhannelconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_occhannelstateconfiguration": {
        "primary_keys": ["msdyn_occhannelstateconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocexternalcontext": {
        "primary_keys": ["msdyn_ocexternalcontextid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocflaggedspam": {
        "primary_keys": ["msdyn_ocflaggedspamid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_oclanguage": {
        "primary_keys": ["msdyn_oclanguageid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocliveworkitem": {
        "primary_keys": ["activityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocliveworkitemcapacityprofile": {
        "primary_keys": ["msdyn_ocliveworkitemcapacityprofileid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocliveworkitemcharacteristic": {
        "primary_keys": ["msdyn_ocliveworkitemcharacteristicid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocliveworkitemcontextitem": {
        "primary_keys": ["msdyn_ocliveworkitemcontextitemid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocliveworkitemparticipant": {
        "primary_keys": ["msdyn_ocliveworkitemparticipantid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocliveworkitemsentiment": {
        "primary_keys": ["msdyn_ocliveworkitemsentimentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocliveworkstreamcontextvariable": {
        "primary_keys": ["msdyn_ocliveworkstreamcontextvariableid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_oclocalizationdata": {
        "primary_keys": ["msdyn_oclocalizationdataid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocpaymentprofile": {
        "primary_keys": ["msdyn_ocpaymentprofileid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocprovisioningstate": {
        "primary_keys": ["msdyn_ocprovisioningstateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocrecording": {
        "primary_keys": ["msdyn_ocrecordingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocrequest": {
        "primary_keys": ["msdyn_ocrequestid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocrichobject": {
        "primary_keys": ["msdyn_ocrichobjectid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocrichobjectmap": {
        "primary_keys": ["msdyn_ocrichobjectmapid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocruleitem": {
        "primary_keys": ["msdyn_ocruleitemid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocsentimentdailytopic": {
        "primary_keys": ["msdyn_ocsentimentdailytopicid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocsentimentdailytopickeyword": {
        "primary_keys": ["msdyn_ocsentimentdailytopickeywordid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocsentimentdailytopictrending": {
        "primary_keys": ["msdyn_ocsentimentdailytopictrendingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocsession": {
        "primary_keys": ["activityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocsessioncharacteristic": {
        "primary_keys": ["msdyn_ocsessioncharacteristicid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocsessionparticipantevent": {
        "primary_keys": ["msdyn_ocsessionparticipanteventid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocsessionsentiment": {
        "primary_keys": ["msdyn_ocsessionsentimentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocsimltraining": {
        "primary_keys": ["msdyn_ocsimltrainingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocsitdimportconfig": {
        "primary_keys": ["msdyn_ocsitdimportconfigid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocsitdskill": {
        "primary_keys": ["msdyn_ocsitdskillid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocsitrainingdata": {
        "primary_keys": ["msdyn_ocsitrainingdataid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocskillidentmlmodel": {
        "primary_keys": ["msdyn_ocskillidentmlmodelid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocsystemmessage": {
        "primary_keys": ["msdyn_ocsystemmessageid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_octag": {
        "primary_keys": ["msdyn_octagid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_odatav4ds": {
        "primary_keys": ["msdyn_odatav4dsid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_omnichannelconfiguration": {
        "primary_keys": ["msdyn_omnichannelconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_omnichannelpersonalization": {
        "primary_keys": ["msdyn_omnichannelpersonalizationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_omnichannelqueue": {
        "primary_keys": ["msdyn_omnichannelqueueid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_omnichannelsyncconfig": {
        "primary_keys": ["msdyn_omnichannelsyncconfigid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_operatinghour": {
        "primary_keys": ["msdyn_operatinghourid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_opportunitykpiitem": {
        "primary_keys": ["msdyn_opportunitykpiitemid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_opportunitymodelconfig": {
        "primary_keys": ["msdyn_opportunitymodelconfigid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_overflowactionconfig": {
        "primary_keys": ["msdyn_overflowactionconfigid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_paneconfiguration": {
        "primary_keys": ["msdyn_paneconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_panetabconfiguration": {
        "primary_keys": ["msdyn_panetabconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_panetoolconfiguration": {
        "primary_keys": ["msdyn_panetoolconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_personalmessage": {
        "primary_keys": ["msdyn_personalmessageid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_personalsoundsetting": {
        "primary_keys": ["msdyn_personalsoundsettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_personasecurityrolemapping": {
        "primary_keys": ["msdyn_personasecurityrolemappingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_playbookactivity": {
        "primary_keys": ["msdyn_playbookactivityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_playbookactivityattribute": {
        "primary_keys": ["msdyn_playbookactivityattributeid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_playbookcategory": {
        "primary_keys": ["msdyn_playbookcategoryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_playbookinstance": {
        "primary_keys": ["msdyn_playbookinstanceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_playbooktemplate": {
        "primary_keys": ["msdyn_playbooktemplateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_pmanalysishistory": {
        "primary_keys": ["msdyn_pmanalysishistoryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_pmcalendar": {
        "primary_keys": ["msdyn_pmcalendarid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_pmcalendarversion": {
        "primary_keys": ["msdyn_pmcalendarversionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_pminferredtask": {
        "primary_keys": ["msdyn_pminferredtaskid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_pmprocessextendedmetadataversion": {
        "primary_keys": ["msdyn_pmprocessextendedmetadataversionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_pmprocessusersettings": {
        "primary_keys": ["msdyn_pmprocessusersettingsid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_pmprocessversion": {
        "primary_keys": ["msdyn_pmprocessversionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_pmrecording": {
        "primary_keys": ["msdyn_pmrecordingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_pmtemplate": {
        "primary_keys": ["msdyn_pmtemplateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_pmview": {
        "primary_keys": ["msdyn_pmviewid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_postalbum": {
        "primary_keys": ["msdyn_postalbumid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_postconfig": {
        "primary_keys": ["msdyn_postconfigid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_postruleconfig": {
        "primary_keys": ["msdyn_postruleconfigid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_preferredagent": {
        "primary_keys": ["msdyn_preferredagentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_preferredagentcustomeridentity": {
        "primary_keys": ["msdyn_preferredagentcustomeridentityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_preferredagentroutedentity": {
        "primary_keys": ["msdyn_preferredagentroutedentityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_presence": {
        "primary_keys": ["msdyn_presenceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_product_knowledgearticle": {
        "primary_keys": ["msdyn_product_knowledgearticleid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_product_knowledgebaserecord": {
        "primary_keys": ["msdyn_product_knowledgebaserecordid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_productivityactioninputparameter": {
        "primary_keys": ["msdyn_productivityactioninputparameterid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_productivityactionoutputparameter": {
        "primary_keys": ["msdyn_productivityactionoutputparameterid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_productivityagentscript": {
        "primary_keys": ["msdyn_productivityagentscriptid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_productivityagentscriptstep": {
        "primary_keys": ["msdyn_productivityagentscriptstepid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_productivitymacroactiontemplate": {
        "primary_keys": ["msdyn_productivitymacroactiontemplateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_productivitymacroconnector": {
        "primary_keys": ["msdyn_productivitymacroconnectorid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_productivitymacrosolutionconfiguration": {
        "primary_keys": ["msdyn_productivitymacrosolutionconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_productivityparameterdefinition": {
        "primary_keys": ["msdyn_productivityparameterdefinitionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_property": {
        "primary_keys": ["msdyn_propertyid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_propertyassetassociation": {
        "primary_keys": ["msdyn_propertyassetassociationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_propertylog": {
        "primary_keys": ["msdyn_propertylogid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_propertytemplateassociation": {
        "primary_keys": ["msdyn_propertytemplateassociationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_provider": {
        "primary_keys": ["msdyn_providerid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_recomputetracker": {
        "primary_keys": ["msdyn_recomputetrackerid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_recording": {
        "primary_keys": ["msdyn_recordingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_recurrence": {
        "primary_keys": ["msdyn_recurrenceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_relationshipinsightsunifiedconfig": {
        "primary_keys": ["msdyn_relationshipinsightsunifiedconfigid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_reportbookmark": {
        "primary_keys": ["msdyn_reportbookmarkid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_richtextfile": {
        "primary_keys": ["msdyn_richtextfileid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_routingconfiguration": {
        "primary_keys": ["msdyn_routingconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_routingconfigurationstep": {
        "primary_keys": ["msdyn_routingconfigurationstepid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_routingrequest": {
        "primary_keys": ["msdyn_routingrequestid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_routingrulesetsetting": {
        "primary_keys": ["msdyn_routingrulesetsettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_rulesetdependencymapping": {
        "primary_keys": ["msdyn_rulesetdependencymappingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_sabackupdiagnostic": {
        "primary_keys": ["msdyn_sabackupdiagnosticid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_sabatchruninstance": {
        "primary_keys": ["msdyn_sabatchruninstanceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_salesaccelerationinsight": {
        "primary_keys": ["msdyn_salesaccelerationinsightid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_salesaccelerationsettings": {
        "primary_keys": ["msdyn_salesaccelerationsettingsid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_salesassignmentsetting": {
        "primary_keys": ["msdyn_salesassignmentsettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_salesinsightssettings": {
        "primary_keys": ["msdyn_salesinsightssettingsid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_salesroutingdiagnostic": {
        "primary_keys": ["msdyn_salesroutingdiagnosticid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_salesroutingrun": {
        "primary_keys": ["msdyn_salesroutingrunid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_salessuggestion": {
        "primary_keys": ["msdyn_salessuggestionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_salestag": {
        "primary_keys": ["msdyn_salestagid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_salestag_msdyn_sequence": {
        "primary_keys": ["msdyn_salestag_msdyn_sequenceid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_saruninstance": {
        "primary_keys": ["msdyn_saruninstanceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_searchconfiguration": {
        "primary_keys": ["msdyn_searchconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_segmentationsetting": {
        "primary_keys": ["msdyn_segmentationsettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_segmentattribute": {
        "primary_keys": ["msdyn_segmentattributeid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_segmentcatalogue": {
        "primary_keys": ["msdyn_segmentcatalogueid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_sentimentanalysis": {
        "primary_keys": ["msdyn_sentimentanalysisid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_sequence": {
        "primary_keys": ["msdyn_sequenceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_sequencestat": {
        "primary_keys": ["msdyn_sequencestatid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_sequencetarget": {
        "primary_keys": ["msdyn_sequencetargetid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_sequencetargetstep": {
        "primary_keys": ["msdyn_sequencetargetstepid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_sequencetemplate": {
        "primary_keys": ["msdyn_sequencetemplateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_serviceconfiguration": {
        "primary_keys": ["msdyn_serviceconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_sessiondata": {
        "primary_keys": ["msdyn_sessiondataid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_sessionevent": {
        "primary_keys": ["msdyn_sessioneventid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_sessionparticipant": {
        "primary_keys": ["msdyn_sessionparticipantid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_sessionparticipantdata": {
        "primary_keys": ["msdyn_sessionparticipantdataid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_sessiontemplate": {
        "primary_keys": ["msdyn_sessiontemplateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_sessiontemplate_applicationtab": {
        "primary_keys": ["msdyn_sessiontemplate_applicationtabid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_shareasconfiguration": {
        "primary_keys": ["msdyn_shareasconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_siconfig": {
        "primary_keys": ["msdyn_siconfigid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_similarentitiesfeatureimportance": {
        "primary_keys": ["msdyn_similarentitiesfeatureimportanceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_skillattachmentruleitem": {
        "primary_keys": ["msdyn_skillattachmentruleitemid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_skillattachmenttarget": {
        "primary_keys": ["msdyn_skillattachmenttargetid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_smartassistconfig": {
        "primary_keys": ["msdyn_smartassistconfigid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_smartassistconfig_msdyn_appconfig": {
        "primary_keys": ["msdyn_smartassistconfig_msdyn_appconfigid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_solutionhealthrule": {
        "primary_keys": ["msdyn_solutionhealthruleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_solutionhealthruleargument": {
        "primary_keys": ["msdyn_solutionhealthruleargumentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_solutionhealthruleset": {
        "primary_keys": ["msdyn_solutionhealthrulesetid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_solutionhistory": {
        "primary_keys": ["msdyn_solutionhistoryid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_soundfile": {
        "primary_keys": ["msdyn_soundfileid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_soundnotificationsetting": {
        "primary_keys": ["msdyn_soundnotificationsettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_suggestedactivitydatasource": {
        "primary_keys": ["msdyn_suggestedactivitydatasourceid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_suggestedcontactsdatasource": {
        "primary_keys": ["msdyn_suggestedcontactsdatasourceid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_suggestioninteraction": {
        "primary_keys": ["msdyn_suggestioninteractionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_suggestionrequestpayload": {
        "primary_keys": ["msdyn_suggestionrequestpayloadid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_suggestionsmodelsummary": {
        "primary_keys": ["msdyn_suggestionsmodelsummaryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_suggestionssetting": {
        "primary_keys": ["msdyn_suggestionssettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_swarm": {
        "primary_keys": ["msdyn_swarmid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_swarmparticipant": {
        "primary_keys": ["msdyn_swarmparticipantid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_swarmparticipantrule": {
        "primary_keys": ["msdyn_swarmparticipantruleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_swarmrole": {
        "primary_keys": ["msdyn_swarmroleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_swarmskill": {
        "primary_keys": ["msdyn_swarmskillid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_swarmtemplate": {
        "primary_keys": ["msdyn_swarmtemplateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_systemuser_msdyn_omnichannelqueue": {
        "primary_keys": ["msdyn_systemuser_msdyn_omnichannelqueueid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_taggedrecord": {
        "primary_keys": ["msdyn_taggedrecordid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_teamschatassociation": {
        "primary_keys": ["msdyn_teamschatassociationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_teamschatsuggestion": {
        "primary_keys": ["msdyn_teamschatsuggestionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_teamscollaboration": {
        "primary_keys": ["msdyn_teamscollaborationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_teamsdialeradminsettings": {
        "primary_keys": ["msdyn_teamsdialeradminsettingsid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_templateforproperties": {
        "primary_keys": ["msdyn_templateforpropertiesid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_templateparameter": {
        "primary_keys": ["msdyn_templateparameterid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_timespent": {
        "primary_keys": ["msdyn_timespentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_tour": {
        "primary_keys": ["msdyn_tourid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_transcript": {
        "primary_keys": ["msdyn_transcriptid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_unifiedroutingdiagnostic": {
        "primary_keys": ["msdyn_unifiedroutingdiagnosticid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_unifiedroutingrun": {
        "primary_keys": ["msdyn_unifiedroutingrunid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_unifiedroutingsetuptracker": {
        "primary_keys": ["msdyn_unifiedroutingsetuptrackerid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_untrackedappointment": {
        "primary_keys": ["msdyn_untrackedappointmentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_upgraderun": {
        "primary_keys": ["msdyn_upgraderunid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_upgradestep": {
        "primary_keys": ["msdyn_upgradestepid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_upgradeversion": {
        "primary_keys": ["msdyn_upgradeversionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_urnotificationtemplate": {
        "primary_keys": ["msdyn_urnotificationtemplateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_urnotificationtemplatemapping": {
        "primary_keys": ["msdyn_urnotificationtemplatemappingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_usagemetric": {
        "primary_keys": ["msdyn_usagemetricid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_usersetting": {
        "primary_keys": ["msdyn_usersettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_virtualtablecolumncandidate": {
        "primary_keys": ["msdyn_virtualtablecolumncandidateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_visitorjourney": {
        "primary_keys": ["msdyn_visitorjourneyid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_wallsavedquery": {
        "primary_keys": ["msdyn_wallsavedqueryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_wallsavedqueryusersettings": {
        "primary_keys": ["msdyn_wallsavedqueryusersettingsid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_wkwcolleaguesforcompany": {
        "primary_keys": ["msdyn_wkwcolleaguesforcompanyid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_wkwcolleaguesforcontact": {
        "primary_keys": ["msdyn_wkwcolleaguesforcontactid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_wkwconfig": {
        "primary_keys": ["msdyn_wkwconfigid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_workflowactionstatus": {
        "primary_keys": ["msdyn_workflowactionstatusid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_worklistsuggestion": {
        "primary_keys": ["msdyn_worklistsuggestionid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_worklistsuggestionsource": {
        "primary_keys": ["msdyn_worklistsuggestionsourceid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_worklistviewconfiguration": {
        "primary_keys": ["msdyn_worklistviewconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_workqueuerecord": {
        "primary_keys": ["msdyn_workqueuerecordid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_workqueuestate": {
        "primary_keys": ["msdyn_workqueuestateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_workqueueusersetting": {
        "primary_keys": ["msdyn_workqueueusersettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_wqdatasource": {
        "primary_keys": ["msdyn_wqdatasourceid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdynce_botcontent": {
        "primary_keys": ["msdynce_botcontentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyncrm_addtocalendarstyle": {
        "primary_keys": ["msdyncrm_addtocalendarstyleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyncrm_basestyle": {
        "primary_keys": ["msdyncrm_basestyleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyncrm_buttonstyle": {
        "primary_keys": ["msdyncrm_buttonstyleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyncrm_codestyle": {
        "primary_keys": ["msdyncrm_codestyleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyncrm_columnstyle": {
        "primary_keys": ["msdyncrm_columnstyleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyncrm_contentblockstyle": {
        "primary_keys": ["msdyncrm_contentblockstyleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyncrm_dividerstyle": {
        "primary_keys": ["msdyncrm_dividerstyleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyncrm_generalstyles": {
        "primary_keys": ["msdyncrm_generalstylesid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyncrm_imagestyle": {
        "primary_keys": ["msdyncrm_imagestyleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyncrm_layoutstyle": {
        "primary_keys": ["msdyncrm_layoutstyleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyncrm_qrcodestyle": {
        "primary_keys": ["msdyncrm_qrcodestyleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyncrm_textstyle": {
        "primary_keys": ["msdyncrm_textstyleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyncrm_videostyle": {
        "primary_keys": ["msdyncrm_videostyleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msfp_alert": {
        "primary_keys": ["activityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msfp_alertrule": {
        "primary_keys": ["msfp_alertruleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msfp_emailtemplate": {
        "primary_keys": ["msfp_emailtemplateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msfp_fileresponse": {
        "primary_keys": ["msfp_fileresponseid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msfp_localizedemailtemplate": {
        "primary_keys": ["msfp_localizedemailtemplateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msfp_project": {
        "primary_keys": ["msfp_projectid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msfp_satisfactionmetric": {
        "primary_keys": ["msfp_satisfactionmetricid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msfp_surveyreminder": {
        "primary_keys": ["msfp_surveyreminderid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msfp_unsubscribedrecipient": {
        "primary_keys": ["msfp_unsubscribedrecipientid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msgraphresourcetosubscription": {
        "primary_keys": ["msgraphresourcetosubscriptionid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "navigationsetting": {
        "primary_keys": ["navigationsettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "newprocess": {
        "primary_keys": ["businessprocessflowinstanceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "organization": {
        "primary_keys": ["organizationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "organizationdatasyncstate": {
        "primary_keys": ["organizationdatasyncstateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "organizationdatasyncsubscriptionentity": {
        "primary_keys": ["organizationdatasyncsubscriptionentityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "ownermapping": {
        "primary_keys": ["ownermappingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "package": {
        "primary_keys": ["packageid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "package_solution": {
        "primary_keys": ["package_solutionid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "personaldocumenttemplate": {
        "primary_keys": ["personaldocumenttemplateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "picklistmapping": {
        "primary_keys": ["picklistmappingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "pluginassembly": {
        "primary_keys": ["pluginassemblyid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "pluginpackage": {
        "primary_keys": ["pluginpackageid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "plugintracelog": {
        "primary_keys": ["plugintracelogid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "plugintype": {
        "primary_keys": ["plugintypeid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "plugintypestatistic": {
        "primary_keys": ["plugintypestatisticid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "position": {
        "primary_keys": ["positionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "post": {
        "primary_keys": ["postid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "postcomment": {
        "primary_keys": ["postcommentid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "postfollow": {
        "primary_keys": ["postfollowid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "postlike": {
        "primary_keys": ["postlikeid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "powerbidataset": {
        "primary_keys": ["powerbidatasetid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "powerbimashupparameter": {
        "primary_keys": ["powerbimashupparameterid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "powerbireport": {
        "primary_keys": ["powerbireportid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "powerfxrule": {
        "primary_keys": ["powerfxruleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "principalentitymap": {
        "primary_keys": ["principalentitymapid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "principalobjectaccess": {
        "primary_keys": ["principalobjectaccessid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "principalobjectattributeaccess": {
        "primary_keys": ["principalobjectattributeaccessid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "privilege": {
        "primary_keys": ["privilegeid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "privilegesremovalsetting": {
        "primary_keys": ["privilegesremovalsettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "processsession": {
        "primary_keys": ["processsessionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "processstage": {
        "primary_keys": ["processstageid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "processstageparameter": {
        "primary_keys": ["processstageparameterid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "processtrigger": {
        "primary_keys": ["processtriggerid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "productassociation": {
        "primary_keys": ["productassociationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "productsalesliterature": {
        "primary_keys": ["productsalesliteratureid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "productsubstitute": {
        "primary_keys": ["productsubstituteid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "provisionlanguageforuser": {
        "primary_keys": ["provisionlanguageforuserid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "publisher": {
        "primary_keys": ["publisherid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "publisheraddress": {
        "primary_keys": ["publisheraddressid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "quarterlyfiscalcalendar": {
        "primary_keys": ["userfiscalcalendarid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "ratingmodel": {
        "primary_keys": ["ratingmodelid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "ratingvalue": {
        "primary_keys": ["ratingvalueid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "recommendeddocument": {
        "primary_keys": ["recommendeddocumentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "recurrencerule": {
        "primary_keys": ["ruleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "relationship": {
        "primary_keys": ["relationshipid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "relationshipattribute": {
        "primary_keys": ["relationshipattributeid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "report": {
        "primary_keys": ["reportid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "reportcategory": {
        "primary_keys": ["reportcategoryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "resource": {
        "primary_keys": ["resourceid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "resourcegroup": {
        "primary_keys": ["resourcegroupid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "resourcegroupdatasource": {
        "primary_keys": ["resourcegroupdatasourceid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "resourcespec": {
        "primary_keys": ["resourcespecid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "role": {
        "primary_keys": ["roleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "roleeditorlayout": {
        "primary_keys": ["roleeditorlayoutid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "roleprivileges": {
        "primary_keys": ["roleprivilegeid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "roletemplate": {
        "primary_keys": ["roletemplateid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "roletemplateprivileges": {
        "primary_keys": ["roletemplateprivilegeid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "rollupfield": {
        "primary_keys": ["rollupfieldid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "savedquery": {
        "primary_keys": ["savedqueryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "savedqueryvisualization": {
        "primary_keys": ["savedqueryvisualizationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "sdkmessage": {
        "primary_keys": ["sdkmessageid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "sdkmessagefilter": {
        "primary_keys": ["sdkmessagefilterid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "sdkmessageprocessingstep": {
        "primary_keys": ["sdkmessageprocessingstepid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "sdkmessageprocessingstepimage": {
        "primary_keys": ["sdkmessageprocessingstepimageid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "sdkmessageprocessingstepsecureconfig": {
        "primary_keys": ["sdkmessageprocessingstepsecureconfigid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "searchrelationshipsettings": {
        "primary_keys": ["searchrelationshipsettingsid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "searchtelemetry": {
        "primary_keys": ["searchtelemetryid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "semiannualfiscalcalendar": {
        "primary_keys": ["userfiscalcalendarid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "service": {
        "primary_keys": ["serviceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "servicecontractcontacts": {
        "primary_keys": ["servicecontractcontactid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "serviceendpoint": {
        "primary_keys": ["serviceendpointid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "serviceplan": {
        "primary_keys": ["serviceplanid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "serviceplanappmodules": {
        "primary_keys": ["serviceplanappmodulesid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "serviceplanmapping": {
        "primary_keys": ["serviceplanmappingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "sharedlinksetting": {
        "primary_keys": ["sharedlinksettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "sharedobject": {
        "primary_keys": ["sharedobjectid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "sharedworkspace": {
        "primary_keys": ["sharedworkspaceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "sharepointdocumentlocation": {
        "primary_keys": ["sharepointdocumentlocationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "sharepointsite": {
        "primary_keys": ["sharepointsiteid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "site": {
        "primary_keys": ["siteid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "sitemap": {
        "primary_keys": ["sitemapid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "socialactivity": {
        "primary_keys": ["activityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "socialprofile": {
        "primary_keys": ["socialprofileid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "solution": {
        "primary_keys": ["solutionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "solutioncomponent": {
        "primary_keys": ["solutioncomponentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "solutioncomponentattributeconfiguration": {
        "primary_keys": ["solutioncomponentattributeconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "solutioncomponentbatchconfiguration": {
        "primary_keys": ["solutioncomponentbatchconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "solutioncomponentconfiguration": {
        "primary_keys": ["solutioncomponentconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "solutioncomponentrelationshipconfiguration": {
        "primary_keys": ["solutioncomponentrelationshipconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "stagesolutionupload": {
        "primary_keys": ["stagesolutionuploadid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "subject": {
        "primary_keys": ["subjectid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "synapsedatabase": {
        "primary_keys": ["synapsedatabaseid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "synapselinkexternaltablestate": {
        "primary_keys": ["synapselinkexternaltablestateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "synapselinkprofile": {
        "primary_keys": ["synapselinkprofileid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "synapselinkprofileentity": {
        "primary_keys": ["synapselinkprofileentityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "synapselinkprofileentitystate": {
        "primary_keys": ["synapselinkprofileentitystateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "synapselinkschedule": {
        "primary_keys": ["synapselinkscheduleid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "syncerror": {
        "primary_keys": ["syncerrorid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "systemform": {
        "primary_keys": ["formid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "systemuserauthorizationchangetracker": {
        "primary_keys": ["systemuserid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "systemuserlicenses": {
        "primary_keys": ["systemuserlicenseid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "systemuserprofiles": {
        "primary_keys": ["systemuserprofileid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "systemuserroles": {
        "primary_keys": ["systemuserroleid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "teammobileofflineprofilemembership": {
        "primary_keys": ["teammobileofflineprofilemembershipid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "teamprofiles": {
        "primary_keys": ["teamprofileid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "teamroles": {
        "primary_keys": ["teamroleid"],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "teamtemplate": {
        "primary_keys": ["teamtemplateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "template": {
        "primary_keys": ["templateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "theme": {
        "primary_keys": ["themeid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "timezonelocalizedname": {
        "primary_keys": ["timezonelocalizednameid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "tracelog": {
        "primary_keys": ["tracelogid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "transformationmapping": {
        "primary_keys": ["transformationmappingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "transformationparametermapping": {
        "primary_keys": ["transformationparametermappingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "translationprocess": {
        "primary_keys": ["businessprocessflowinstanceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "userform": {
        "primary_keys": ["userformid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "usermapping": {
        "primary_keys": ["usermappingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "usermobileofflineprofilemembership": {
        "primary_keys": ["usermobileofflineprofilemembershipid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "userquery": {
        "primary_keys": ["userqueryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "userqueryvisualization": {
        "primary_keys": ["userqueryvisualizationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "userrating": {
        "primary_keys": ["userratingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "usersettings": {
        "primary_keys": ["systemuserid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "virtualentitymetadata": {
        "primary_keys": ["virtualentitymetadataid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "webresource": {
        "primary_keys": ["webresourceid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "webwizard": {
        "primary_keys": ["webwizardid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "workflow": {
        "primary_keys": ["workflowid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "workflowbinary": {
        "primary_keys": ["workflowbinaryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "workflowlog": {
        "primary_keys": ["workflowlogid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msfp_surveyinvitesummary": {
        "primary_keys": ["msfp_surveyinvitesummaryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "agenticscenario": {
        "primary_keys": ["agenticscenarioid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdynmkt_consentprovider": {
        "primary_keys": ["msdynmkt_consentproviderid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "agentprompt": {
        "primary_keys": ["agentpromptid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "adx_webformsession": {
        "primary_keys": ["adx_webformsessionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "retentionsuccessdetail": {
        "primary_keys": ["retentionsuccessdetailid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msfp_satisfactionmetricaggregate": {
        "primary_keys": ["msfp_satisfactionmetricaggregateid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdynmkt_quiettimesetting": {
        "primary_keys": ["msdynmkt_quiettimesettingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "retentionoperationdetail": {
        "primary_keys": ["retentionoperationdetailid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "sharepointmanagedidentity": {
        "primary_keys": ["sharepointmanagedidentityid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_knowledgeconfiguration": {
        "primary_keys": ["msdyn_knowledgeconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdynmkt_preferencecenterlink": {
        "primary_keys": ["msdynmkt_preferencecenterlinkid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "aiinsightcard": {
        "primary_keys": ["aiinsightcardid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_knowledgeassetconfiguration": {
        "primary_keys": ["msdyn_knowledgeassetconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_ocliveworkitemextension": {
        "primary_keys": ["msdyn_ocliveworkitemextensionid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_workordercharacteristic": {
        "primary_keys": ["msdyn_workordercharacteristicid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "agentmemory": {
        "primary_keys": ["agentmemoryid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdynmkt_consent": {
        "primary_keys": ["msdynmkt_consentid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "workflowmetadata": {
        "primary_keys": ["workflowmetadataid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "retentionfailuredetail": {
        "primary_keys": ["retentionfailuredetailid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "agenttask": {
        "primary_keys": ["agenttaskid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "aicopilot": {
        "primary_keys": ["aicopilotid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "adx_setting": {
        "primary_keys": ["adx_settingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "retentionoperation": {
        "primary_keys": ["retentionoperationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdynmkt_consentproviderdefaultpurpose": {
        "primary_keys": ["msdynmkt_consentproviderdefaultpurposeid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msfp_satisfactionmetricsurveymapping": {
        "primary_keys": ["msfp_satisfactionmetricsurveymappingid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_requirementorganizationunit": {
        "primary_keys": ["msdyn_requirementorganizationunitid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdynmkt_consentcenterconfiguration": {
        "primary_keys": ["msdynmkt_consentcenterconfigurationid"],
        "replication_method": "INCREMENTAL",
        "replication_keys": ["modifiedon"],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "adx_externalidentity": {
        "primary_keys": [
            "adx_externalidentityid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "adx_invitation": {
        "primary_keys": [
            "adx_invitationid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "adx_inviteredemption": {
        "primary_keys": [
            "activityid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "agentrule": {
        "primary_keys": [
            "agentruleid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "aicopilot_aiplugin": {
        "primary_keys": [
            "aicopilot_aipluginid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "aiplugin": {
        "primary_keys": [
            "aipluginid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "aipluginauth": {
        "primary_keys": [
            "aipluginauthid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "aipluginconversationstarter": {
        "primary_keys": [
            "aipluginconversationstarterid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "aipluginconversationstartermapping": {
        "primary_keys": [
            "aipluginconversationstartermappingid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "aipluginexternalschema": {
        "primary_keys": [
            "aipluginexternalschemaid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "aipluginexternalschemaproperty": {
        "primary_keys": [
            "aipluginexternalschemapropertyid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "aiplugingovernance": {
        "primary_keys": [
            "aiplugingovernanceid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "aiplugingovernanceext": {
        "primary_keys": [
            "aiplugingovernanceextid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "aiplugininstance": {
        "primary_keys": [
            "aiplugininstanceid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "aipluginoperation": {
        "primary_keys": [
            "aipluginoperationid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "aipluginoperationparameter": {
        "primary_keys": [
            "aipluginoperationparameterid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "aipluginoperationresponsetemplate": {
        "primary_keys": [
            "aipluginoperationresponsetemplateid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "aiplugintitle": {
        "primary_keys": [
            "aiplugintitleid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "aipluginusersetting": {
        "primary_keys": [
            "aipluginusersettingid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "allowedmcpclient": {
        "primary_keys": [
            "allowedmcpclientid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "anyprivilegeentity": {
        "primary_keys": [
            "anyprivilegeentityid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "application": {
        "primary_keys": [
            "applicationid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "applicationroles": {
        "primary_keys": [
            "applicationrolesid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "appnotificationsignal": {
        "primary_keys": [
            "appnotificationsignalid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "approvalprocess": {
        "primary_keys": [
            "approvalprocessid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "approvalstageapproval": {
        "primary_keys": [
            "approvalstageapprovalid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "approvalstagecondition": {
        "primary_keys": [
            "approvalstageconditionid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "approvalstageintelligent": {
        "primary_keys": [
            "approvalstageintelligentid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "approvalstageorder": {
        "primary_keys": [
            "approvalstageorderid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "athenareconciliationinfo": {
        "primary_keys": [
            "athenareconciliationinfoid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "attributeclusterconfig": {
        "primary_keys": [
            "attributeclusterconfigid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "attributemaskingrule": {
        "primary_keys": [
            "attributemaskingruleid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "backgroundoperation": {
        "primary_keys": [
            "backgroundoperationid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "bot_botcomponentcollection": {
        "primary_keys": [
            "bot_botcomponentcollectionid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "botcomponent_aipluginoperation": {
        "primary_keys": [
            "botcomponent_aipluginoperationid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "botcomponent_connectionreference": {
        "primary_keys": [
            "botcomponent_connectionreferenceid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "botcomponent_dvtablesearch": {
        "primary_keys": [
            "botcomponent_dvtablesearchid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "botcomponent_msdyn_aimodel": {
        "primary_keys": [
            "botcomponent_msdyn_aimodelid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "botcomponentcollection": {
        "primary_keys": [
            "botcomponentcollectionid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "businessprocess": {
        "primary_keys": [
            "businessprocessid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "businessprocesslinkedartifact": {
        "primary_keys": [
            "businessprocesslinkedartifactid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "cardentityconnections": {
        "primary_keys": [
            "cardentityconnectionsid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "cardstateitem": {
        "primary_keys": [
            "cardstateitemid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "certificatecredential": {
        "primary_keys": [
            "certificatecredentialid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "componentversiondatasource": {
        "primary_keys": [
            "componentversiondatasourceid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "computeruseagent": {
        "primary_keys": [
            "computeruseagentid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "controlconfiguration": {
        "primary_keys": [
            "controlconfigurationid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "copilotexamplequestion": {
        "primary_keys": [
            "copilotexamplequestionid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "copilotglossaryterm": {
        "primary_keys": [
            "copilotglossarytermid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "copilotsynonyms": {
        "primary_keys": [
            "copilotsynonymsid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "credential": {
        "primary_keys": [
            "credentialid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "deleteditemreference": {
        "primary_keys": [
            "deleteditemreferenceid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "dependency": {
        "primary_keys": [
            "dependencyid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "desktopflowmodule": {
        "primary_keys": [
            "desktopflowmoduleid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "dvfilesearch": {
        "primary_keys": [
            "dvfilesearchid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "dvfilesearchattribute": {
        "primary_keys": [
            "dvfilesearchattributeid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "dvfilesearchentity": {
        "primary_keys": [
            "dvfilesearchentityid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "dvtablesearch": {
        "primary_keys": [
            "dvtablesearchid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "dvtablesearchattribute": {
        "primary_keys": [
            "dvtablesearchattributeid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "dvtablesearchentity": {
        "primary_keys": [
            "dvtablesearchentityid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "elasticfileattachment": {
        "primary_keys": [
            "elasticfileattachmentid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "emailaddressconfiguration": {
        "primary_keys": [
            "emailaddressconfigurationid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "entityclusterconfig": {
        "primary_keys": [
            "entityclusterconfigid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "entityrecordfilter": {
        "primary_keys": [
            "entityrecordfilterid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "eventexpanderbreadcrumb": {
        "primary_keys": [
            "eventexpanderbreadcrumbid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "exportedexcel": {
        "primary_keys": [
            "exportedexcelid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "fabricaiskill": {
        "primary_keys": [
            "fabricaiskillid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "federatedknowledgeconfiguration": {
        "primary_keys": [
            "federatedknowledgeconfigurationid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "federatedknowledgeentityconfiguration": {
        "primary_keys": [
            "federatedknowledgeentityconfigurationid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "flowaggregation": {
        "primary_keys": [
            "flowaggregationid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "flowcapacityassignment": {
        "primary_keys": [
            "flowcapacityassignmentid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "flowcredentialapplication": {
        "primary_keys": [
            "flowcredentialapplicationid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "flowevent": {
        "primary_keys": [
            "floweventid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "flowgroup": {
        "primary_keys": [
            "flowgroupid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "flowrun": {
        "primary_keys": [
            "flowrunid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "flowsessionbinary": {
        "primary_keys": [
            "flowsessionbinaryid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "flowtestsession": {
        "primary_keys": [
            "flowtestsessionid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "flowtrigger": {
        "primary_keys": [
            "flowtriggerid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "flowtriggerinstance": {
        "primary_keys": [
            "flowtriggerinstanceid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "fxexpression": {
        "primary_keys": [
            "fxexpressionid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "gitconfigurationretrievaldatasource": {
        "primary_keys": [
            "gitconfigurationretrievaldatasourceid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "githubappconfig": {
        "primary_keys": [
            "githubappconfigid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "indexedtrait": {
        "primary_keys": [
            "indexedtraitid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "invaliddependency": {
        "primary_keys": [
            "invaliddependencyid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "knowledgefaq": {
        "primary_keys": [
            "knowledgefaqid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "mainfewshot": {
        "primary_keys": [
            "mainfewshotid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "makerfewshot": {
        "primary_keys": [
            "makerfewshotid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "maskingrule": {
        "primary_keys": [
            "maskingruleid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "mcpprompt": {
        "primary_keys": [
            "mcppromptid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "mcpresource": {
        "primary_keys": [
            "mcpresourceid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "mcpresourcecontent": {
        "primary_keys": [
            "mcpresourcecontentid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "mcpserver": {
        "primary_keys": [
            "mcpserverid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "mcptool": {
        "primary_keys": [
            "mcptoolid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "metadataforarchival": {
        "primary_keys": [
            "metadataforarchivalid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "mobileofflineprofileextension": {
        "primary_keys": [
            "mobileofflineprofileextensionid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "mos3management": {
        "primary_keys": [
            "mos3managementid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aiconfiguration_documenttemplate": {
        "primary_keys": [
            "msdyn_aiconfiguration_documenttemplateid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_aidataprocessingevent": {
        "primary_keys": [
            "msdyn_aidataprocessingeventid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aidocumenttemplate": {
        "primary_keys": [
            "msdyn_aidocumenttemplateid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aievaluationconfiguration": {
        "primary_keys": [
            "msdyn_aievaluationconfigurationid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aievaluationrun": {
        "primary_keys": [
            "msdyn_aievaluationrunid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aievent": {
        "primary_keys": [
            "msdyn_aieventid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aitestcase": {
        "primary_keys": [
            "msdyn_aitestcaseid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aitestcasedocument": {
        "primary_keys": [
            "msdyn_aitestcasedocumentid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aitestcaseinput": {
        "primary_keys": [
            "msdyn_aitestcaseinputid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aitestrun": {
        "primary_keys": [
            "msdyn_aitestrunid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_aitestrunbatch": {
        "primary_keys": [
            "msdyn_aitestrunbatchid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_analysisoverride": {
        "primary_keys": [
            "msdyn_analysisoverrideid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_bulkharvestrunlog": {
        "primary_keys": [
            "msdyn_bulkharvestrunlogid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_copilotinteractions": {
        "primary_keys": [
            "msdyn_copilotinteractionsid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_dataflow_datalakefolder": {
        "primary_keys": [
            "msdyn_dataflow_datalakefolderid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_dataflowconnectionreference": {
        "primary_keys": [
            "msdyn_dataflowconnectionreferenceid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_dataflowtemplate": {
        "primary_keys": [
            "msdyn_dataflowtemplateid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_dmsrequest": {
        "primary_keys": [
            "msdyn_dmsrequestid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_dmsrequeststatus": {
        "primary_keys": [
            "msdyn_dmsrequeststatusid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_dmssyncrequest": {
        "primary_keys": [
            "msdyn_dmssyncrequestid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_dmssyncstatus": {
        "primary_keys": [
            "msdyn_dmssyncstatusid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_evalassertion": {
        "primary_keys": [
            "msdyn_evalassertionid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_evaldataset": {
        "primary_keys": [
            "msdyn_evaldatasetid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_evalprompt": {
        "primary_keys": [
            "msdyn_evalpromptid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_evalresult": {
        "primary_keys": [
            "msdyn_evalresultid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_evalrun": {
        "primary_keys": [
            "msdyn_evalrunid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_favoriteknowledgearticle": {
        "primary_keys": [
            "msdyn_favoriteknowledgearticleid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_fileupload": {
        "primary_keys": [
            "msdyn_fileuploadid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_flow_actionapprovalmodel": {
        "primary_keys": [
            "msdyn_flow_actionapprovalmodelid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_flow_approval": {
        "primary_keys": [
            "msdyn_flow_approvalid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_flow_approvalrequest": {
        "primary_keys": [
            "msdyn_flow_approvalrequestid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_flow_approvalresponse": {
        "primary_keys": [
            "msdyn_flow_approvalresponseid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_flow_approvalstep": {
        "primary_keys": [
            "msdyn_flow_approvalstepid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_flow_awaitallactionapprovalmodel": {
        "primary_keys": [
            "msdyn_flow_awaitallactionapprovalmodelid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_flow_awaitallapprovalmodel": {
        "primary_keys": [
            "msdyn_flow_awaitallapprovalmodelid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_flow_basicapprovalmodel": {
        "primary_keys": [
            "msdyn_flow_basicapprovalmodelid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_flow_flowapproval": {
        "primary_keys": [
            "msdyn_flow_flowapprovalid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_formmapping": {
        "primary_keys": [
            "msdyn_formmappingid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_function": {
        "primary_keys": [
            "msdyn_functionid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_harvesteligibilitycondition": {
        "primary_keys": [
            "msdyn_harvesteligibilityconditionid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_harvestworkitem": {
        "primary_keys": [
            "msdyn_harvestworkitemid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_historicalcaseharvestbatch": {
        "primary_keys": [
            "msdyn_historicalcaseharvestbatchid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_historicalcaseharvestrun": {
        "primary_keys": [
            "msdyn_historicalcaseharvestrunid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_historicalcaseharvestrunlog": {
        "primary_keys": [
            "msdyn_historicalcaseharvestrunlogid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_knowledgeharvestjobrecord": {
        "primary_keys": [
            "msdyn_knowledgeharvestjobrecordid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_knowledgeharvestplan": {
        "primary_keys": [
            "msdyn_knowledgeharvestplanid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_mobileapp": {
        "primary_keys": [
            "msdyn_mobileappid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_modulerundetail": {
        "primary_keys": [
            "msdyn_modulerundetailid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_nativeextension": {
        "primary_keys": [
            "msdyn_nativeextensionid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_pmbusinessruleautomationconfig": {
        "primary_keys": [
            "msdyn_pmbusinessruleautomationconfigid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_pmprocesstemplate": {
        "primary_keys": [
            "msdyn_pmprocesstemplateid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_pmsimulation": {
        "primary_keys": [
            "msdyn_pmsimulationid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_pmtab": {
        "primary_keys": [
            "msdyn_pmtabid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_powerappswrapbuild": {
        "primary_keys": [
            "msdyn_powerappswrapbuildid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_qna": {
        "primary_keys": [
            "msdyn_qnaid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_rtestructuredtemplate": {
        "primary_keys": [
            "msdyn_rtestructuredtemplateid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_rtestructuredtemplateconfig": {
        "primary_keys": [
            "msdyn_rtestructuredtemplateconfigid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_rtetemplatemapping": {
        "primary_keys": [
            "msdyn_rtetemplatemappingid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_salesforcestructuredobject": {
        "primary_keys": [
            "msdyn_salesforcestructuredobjectid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_salesforcestructuredqnaconfig": {
        "primary_keys": [
            "msdyn_salesforcestructuredqnaconfigid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_schedule": {
        "primary_keys": [
            "msdyn_scheduleid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "msdyn_solutionhistorydatasource": {
        "primary_keys": [
            "msdyn_solutionhistorydatasourceid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "msdyn_timelinepin": {
        "primary_keys": [
            "msdyn_timelinepinid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "mspcat_catalogsubmissionfiles": {
        "primary_keys": [
            "mspcat_catalogsubmissionfilesid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "mspcat_packagestore": {
        "primary_keys": [
            "mspcat_packagestoreid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "mspp_adplacement": {
        "primary_keys": [
            "mspp_adplacementid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_columnpermission": {
        "primary_keys": [
            "mspp_columnpermissionid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_columnpermissionprofile": {
        "primary_keys": [
            "mspp_columnpermissionprofileid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_contentsnippet": {
        "primary_keys": [
            "mspp_contentsnippetid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_entityform": {
        "primary_keys": [
            "mspp_entityformid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_entityformmetadata": {
        "primary_keys": [
            "mspp_entityformmetadataid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_entitylist": {
        "primary_keys": [
            "mspp_entitylistid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_entitypermission": {
        "primary_keys": [
            "mspp_entitypermissionid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_pagetemplate": {
        "primary_keys": [
            "mspp_pagetemplateid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_pollplacement": {
        "primary_keys": [
            "mspp_pollplacementid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_powerpagescoreentityds": {
        "primary_keys": [
            "mspp_powerpagescoreentitydsid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_publishingstate": {
        "primary_keys": [
            "mspp_publishingstateid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_publishingstatetransitionrule": {
        "primary_keys": [
            "mspp_publishingstatetransitionruleid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_redirect": {
        "primary_keys": [
            "mspp_redirectid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_shortcut": {
        "primary_keys": [
            "mspp_shortcutid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_sitemarker": {
        "primary_keys": [
            "mspp_sitemarkerid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_sitesetting": {
        "primary_keys": [
            "mspp_sitesettingid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_webfile": {
        "primary_keys": [
            "mspp_webfileid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_webform": {
        "primary_keys": [
            "mspp_webformid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_webformmetadata": {
        "primary_keys": [
            "mspp_webformmetadataid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_webformstep": {
        "primary_keys": [
            "mspp_webformstepid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_weblink": {
        "primary_keys": [
            "mspp_weblinkid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_weblinkset": {
        "primary_keys": [
            "mspp_weblinksetid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_webpage": {
        "primary_keys": [
            "mspp_webpageid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_webpageaccesscontrolrule": {
        "primary_keys": [
            "mspp_webpageaccesscontrolruleid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_webrole": {
        "primary_keys": [
            "mspp_webroleid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_website": {
        "primary_keys": [
            "mspp_websiteid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_websiteaccess": {
        "primary_keys": [
            "mspp_websiteaccessid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_websitelanguage": {
        "primary_keys": [
            "mspp_websitelanguageid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "mspp_webtemplate": {
        "primary_keys": [
            "mspp_webtemplateid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "nlsqregistration": {
        "primary_keys": [
            "nlsqregistrationid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "organizationdatasyncfnostate": {
        "primary_keys": [
            "organizationdatasyncfnostateid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "organizationdatasyncsubscriptionfnotable": {
        "primary_keys": [
            "organizationdatasyncsubscriptionfnotableid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "packagehistory": {
        "primary_keys": [
            "packagehistoryid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "plannerbusinessscenario": {
        "primary_keys": [
            "plannerbusinessscenarioid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "plannersyncaction": {
        "primary_keys": [
            "plannersyncactionid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "plugin": {
        "primary_keys": [
            "pluginid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "powerpagecomponent": {
        "primary_keys": [
            "powerpagecomponentid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "powerpagecomponent_powerpagecomponent": {
        "primary_keys": [
            "powerpagecomponent_powerpagecomponentid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "powerpagesddosalert": {
        "primary_keys": [
            "powerpagesddosalertid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "powerpagesite": {
        "primary_keys": [
            "powerpagesiteid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "powerpagesite_dvfilesearch": {
        "primary_keys": [
            "powerpagesite_dvfilesearchid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "powerpagesite_dvtablesearch": {
        "primary_keys": [
            "powerpagesite_dvtablesearchid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "powerpagesitelanguage": {
        "primary_keys": [
            "powerpagesitelanguageid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "powerpagesitepublished": {
        "primary_keys": [
            "powerpagesitepublishedid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "powerpageslog": {
        "primary_keys": [
            "powerpageslogid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "powerpagesmanagedidentity": {
        "primary_keys": [
            "powerpagesmanagedidentityid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "powerpagesscanreport": {
        "primary_keys": [
            "powerpagesscanreportid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "powerpagessiteaifeedback": {
        "primary_keys": [
            "powerpagessiteaifeedbackid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "powerpagessourcefile": {
        "primary_keys": [
            "powerpagessourcefileid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "powerpagesusermapping": {
        "primary_keys": [
            "powerpagesusermappingid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "privilegecheckerlog": {
        "primary_keys": [
            "privilegecheckerlogid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "privilegecheckerrun": {
        "primary_keys": [
            "privilegecheckerrunid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "recentlyused": {
        "primary_keys": [
            "recentlyusedid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "recordfilter": {
        "primary_keys": [
            "recordfilterid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "recyclebinconfig": {
        "primary_keys": [
            "recyclebinconfigid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "reportparameter": {
        "primary_keys": [
            "reportparameterid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "retaineddataexcel": {
        "primary_keys": [
            "retaineddataexcelid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "retentionconfig": {
        "primary_keys": [
            "retentionconfigid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "sa_suggestedaction": {
        "primary_keys": [
            "sa_suggestedactionid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "sa_suggestedactioncriteria": {
        "primary_keys": [
            "sa_suggestedactioncriteriaid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "savingrule": {
        "primary_keys": [
            "savingruleid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "searchattributesettings": {
        "primary_keys": [
            "searchattributesettingsid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "searchcustomanalyzer": {
        "primary_keys": [
            "searchcustomanalyzerid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "searchresultscache": {
        "primary_keys": [
            "searchresultscacheid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "sensitivitylabelattributemapping": {
        "primary_keys": [
            "sensitivitylabelattributemappingid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "sharedworkspacepool": {
        "primary_keys": [
            "sharedworkspacepoolid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "sideloadedaiplugin": {
        "primary_keys": [
            "sideloadedaipluginid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "signal": {
        "primary_keys": [
            "signalid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "skill": {
        "primary_keys": [
            "skillid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "skilldvtablesearch": {
        "primary_keys": [
            "skilldvtablesearchid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "skillmetadata": {
        "primary_keys": [
            "skillmetadataid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "skillresource": {
        "primary_keys": [
            "skillresourceid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "skillrolemapping": {
        "primary_keys": [
            "skillrolemappingid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "sourcecontrolbranchconfiguration": {
        "primary_keys": [
            "sourcecontrolbranchconfigurationid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "sourcecontrolcomponent": {
        "primary_keys": [
            "sourcecontrolcomponentid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "sourcecontrolconfiguration": {
        "primary_keys": [
            "sourcecontrolconfigurationid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "sourcecontroloperationtracking": {
        "primary_keys": [
            "sourcecontroloperationtrackingid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "stagedentity": {
        "primary_keys": [
            "stagedentityid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "stagedentityattribute": {
        "primary_keys": [
            "stagedentityattributeid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "stagedmetadataasyncoperation": {
        "primary_keys": [
            "stagedmetadataasyncoperationid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "stagedsourcecontrolcomponent": {
        "primary_keys": [
            "stagedsourcecontrolcomponentid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "tag": {
        "primary_keys": [
            "tagid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "taggedflowsession": {
        "primary_keys": [
            "taggedflowsessionid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "taggedprocess": {
        "primary_keys": [
            "taggedprocessid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "textanalyticsentitymapping": {
        "primary_keys": [
            "textanalyticsentitymappingid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "textdatarecordsindexingstatus": {
        "primary_keys": [
            "textdatarecordsindexingstatusid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "timezonedefinition": {
        "primary_keys": [
            "timezonedefinitionid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "timezonerule": {
        "primary_keys": [
            "timezoneruleid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "trait": {
        "primary_keys": [
            "traitid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "viewasexamplequestion": {
        "primary_keys": [
            "viewasexamplequestionid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "workflowcardconnections": {
        "primary_keys": [
            "workflowcardconnectionsid"
        ],
        "replication_method": "FULL_TABLE",
        "replication_keys": [],
        "obeys_start_date": false,
        "api_limit": 100
    },
    "workqueue": {
        "primary_keys": [
            "workqueueid"
        ],
        "replication_method": "INCREMENTAL",
        "replication_keys": [
            "modifiedon"
        ],
        "obeys_start_date": true,
        "api_limit": 100
    },
    "workqueueitem": {
        "primary_keys": [
            "workqueueitemid"
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

    # Org-specific custom entities (created ad-hoc in the test sandbox using the
    # default "new_" customization prefix) that are not part of the tap's
    # standard expected metadata. These are always excluded from discovery
    # test comparisons so the test suite doesn't break when the sandbox's
    # custom entities change.
    CUSTOM_STREAMS_TO_SKIP = {
        "new_testcustomactivity",
        "new_testelastic",
        "new_testequipmentlog",
        "new_testproject",
        "new_testrichtype",
        "new_testsurveyresponse",
    }

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

    def run_and_verify_check_mode(self, conn_id):
        """
        Run check mode and verify it succeeds, excluding the org-specific
        custom entities in CUSTOM_STREAMS_TO_SKIP from the discovered catalog
        before comparing against expected streams.

        Return the found catalogs from menagerie.
        """
        check_job_name = runner.run_check_mode(self, conn_id)

        exit_status = menagerie.get_exit_status(conn_id, check_job_name)
        menagerie.verify_check_exit_status(self, exit_status, check_job_name)

        found_catalogs = [
            catalog for catalog in menagerie.get_catalogs(conn_id)
            if catalog['stream_name'] not in self.CUSTOM_STREAMS_TO_SKIP
        ]
        self.assertGreater(len(found_catalogs), 0,
                           logging="A catalog was produced by discovery.")

        found_stream_names = {catalog['stream_name'] for catalog in found_catalogs}
        self.assertSetEqual(self.expected_stream_names(), found_stream_names,
                            logging="Expected streams are present in catalog.")

        return found_catalogs


    @staticmethod
    def get_credentials():
        """Authentication information for the test account."""
        credentials_dict = {}
        creds = {
            'auth_method': 'client_credentials',
            'client_id': 'TAP_MS_DYNAMICS_365_CRM_CLIENT_ID',
            'client_secret': 'TAP_MS_DYNAMICS_365_CRM_CLIENT_SECRET',
            'organization_uri': 'TAP_MS_DYNAMICS_365_CRM_ORGANIZATION_URI',
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
