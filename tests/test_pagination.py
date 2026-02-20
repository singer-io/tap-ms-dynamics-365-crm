import unittest

from parameterized import parameterized_class
from tap_tester.base_suite_tests.pagination_test import PaginationTest
from base import MSDynamics365CRMBaseTest


DEFAULT_PAGE_SIZE = 20

PER_STREAM_PAGE_SIZES = {
    "account": 10,
    "contact": 10,
    "lead": 10,
    "opportunity": 10,
    'incident': 25,
    'knowledgearticle': 16,
    'phonetocaseprocess': 22,
    'product': 15,
    'queue': 200,
    'queuemembership': 200
}

STREAMS_TO_EXCLUDE = set({
    'bookableresource',
    'bookableresourcebooking',
    'bookableresourcebookingheader',
    'bookableresourcecategory',
    'bookableresourcecategoryassn',
    'bookableresourcecharacteristic',
    'bookableresourcegroup',
    'competitor',
    'contract',
    'contractdetail',
    'contracttemplate',
    'entitlement',
    'entitlementchannel',
    'entitlementcontacts',
    'entitlemententityallocationtypemapping',
    'entitlementproducts',
    'entitlementtemplate',
    'entitlementtemplatechannel',
    'entitlementtemplateproducts',
    'equipment',
    'feedback',
    'incidentknowledgebaserecord',
    'incidentresolution',
    'invoice',
    'invoicedetail',
    'knowledgearticleincident',
    'knowledgearticleviews',
    'knowledgebaserecord',
    'msdyn_actual',
    'msdyn_agreement',
    'msdyn_agreementbookingdate',
    'msdyn_agreementbookingincident',
    'msdyn_agreementbookingproduct',
    'msdyn_agreementbookingservice',
    'msdyn_bookableresourceassociation',
    'msdyn_bookingalert',
    'msdyn_bookingalertstatus',
    'msdyn_bookingjournal',
    'msdyn_bookingrule',
    'msdyn_bookingsetupmetadata',
    'msdyn_bookingtimestamp',
    'msdyn_entitlementapplication',
    'msdyn_fieldservicesetting',
    'msdyn_fieldserviceslaconfiguration',
    'msdyn_flwconfiguration',
    'msdyn_geofence',
    'msdyn_geofenceevent',
    'msdyn_geofencingsettings',
    'msdyn_geolocationsettings',
    'msdyn_geolocationtracking',
    'msdyn_incidenttype',
    'msdyn_incidenttypecharacteristic',
    'msdyn_incidenttypeproduct',
    'msdyn_incidenttyperesolution',
    'msdyn_incidenttypeservice',
    'msdyn_incidenttypeservicetask',
    'msdyn_incidenttypessetup',
    'msdyn_inspection',
    'msdyn_inspectionattachment',
    'msdyn_inspectiondefinition',
    'msdyn_inspectioninstance',
    'msdyn_inspectionresponse',
    'msdyn_inventoryadjustment',
    'msdyn_inventoryadjustmentproduct',
    'msdyn_inventoryjournal',
    'msdyn_inventorytransfer',
    'msdyn_nottoexceed',
    'msdyn_optimizationrequest',
    'msdyn_organizationalunit',
    'msdyn_postalcode',
    'msdyn_priority',
    'msdyn_productinventory',
    'msdyn_purchaseorder',
    'msdyn_purchaseorderbill',
    'msdyn_purchaseorderproduct',
    'msdyn_purchaseorderreceipt',
    'msdyn_purchaseorderreceiptproduct',
    'msdyn_purchaseordersubstatus',
    'msdyn_requirementchange',
    'msdyn_requirementcharacteristic',
    'msdyn_requirementdependency',
    'msdyn_requirementgroup',
    'msdyn_requirementresourcecategory',
    'msdyn_requirementresourcepreference',
    'msdyn_requirementstatus',
    'msdyn_resolution',
    'msdyn_resourcepaytype',
    'msdyn_resourcerequirement',
    'msdyn_resourcerequirementdetail',
    'msdyn_resourceterritory',
    'msdyn_rma',
    'msdyn_rmaproduct',
    'msdyn_rmareceipt',
    'msdyn_rmareceiptproduct',
    'msdyn_rmasubstatus',
    'msdyn_rtv',
    'msdyn_rtvproduct',
    'msdyn_rtvsubstatus',
    'msdyn_scheduleboardsetting',
    'msdyn_servicetasktype',
    'msdyn_shipvia',
    'msdyn_slakpi',
    'msdyn_systemuserschedulersetting',
    'msdyn_taxcode',
    'msdyn_taxcodedetail',
    'msdyn_timeentry',
    'msdyn_timeentrysetting',
    'msdyn_timegroupdetail',
    'msdyn_timeoffrequest',
    'msdyn_trade',
    'msdyn_tradecoverage',
    'msdyn_warehouse',
    'msdyn_workhourtemplate',
    'msdyn_workorder',
    'msdyn_workorderincident',
    'msdyn_workordernte',
    'msdyn_workorderproduct',
    'msdyn_workorderresolution',
    'msdyn_workorderservice',
    'msdyn_workorderservicetask',
    'msdyn_workordersubstatus',
    'msdyn_workordertype',
    'opportunityproduct',
    'pricelevel',
    'productpricelevel',
    'queueitem',
    'quote',
    'quotedetail',
    'salesliterature',
    'salesliteratureitem',
    'salesorder',
    'salesorderdetail',
    'serviceappointment',
    'sla',
    'slaitem',
    'slakpiinstance',
})


def _pagination_params():
    """Create one test class per stream with stream-specific page size."""
    streams = sorted(
        set(MSDynamics365CRMBaseTest.expected_metadata().keys()).difference(STREAMS_TO_EXCLUDE)
    )
    return [
        (stream, PER_STREAM_PAGE_SIZES.get(stream, DEFAULT_PAGE_SIZE))
        for stream in streams
    ]


@parameterized_class(("test_stream", "page_size_value"), _pagination_params())
class MSDynamics365CRMPaginationTest(PaginationTest, MSDynamics365CRMBaseTest):
    """
    Ensure tap can replicate multiple pages of data for streams that use pagination.
    """

    @classmethod
    def name(cls):
        return (
            "tap_tester_ms_dynamics_365_crm_pagination_test_"
            f"{cls.test_stream}_page_size_{cls.page_size_value}"
        )

    @classmethod
    def setUpClass(cls):
        # Parameterized template class can be collected by unittest; skip it.
        if cls.__name__ == "MSDynamics365CRMPaginationTest":
            raise unittest.SkipTest("Template class; run generated parameterized classes only")

        # Reset shared PaginationTest cache for each generated stream class.
        PaginationTest.synced_records = None
        PaginationTest.record_count_by_stream = None

        super().setUpClass()

    def get_properties(self, original: bool = True):
        props = super().get_properties(original=original)
        props["page_size"] = self.page_size_value
        return props

    def streams_to_test(self):
        return {self.test_stream}
