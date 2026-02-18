"""
Entity Templates for MS Dynamics 365 CRM Test Data Generator

Defines field mappings and data generation functions for different entity types.
"""
import random
from datetime import datetime, timedelta


ENTITY_TEMPLATES = {
    # ===== SALES ENTITIES =====
    'account': {
        'name': lambda f: f.company(),
        'telephone1': lambda f: f.phone_number(),
        'emailaddress1': lambda f: f.company_email(),
        'websiteurl': lambda f: f.url(),
        'revenue': lambda f: random.randint(100000, 10000000),
        'numberofemployees': lambda f: random.randint(10, 5000)
    },
    'contact': {
        'firstname': lambda f: f.first_name(),
        'lastname': lambda f: f.last_name(),
        'emailaddress1': lambda f: f.email(),
        'telephone1': lambda f: f.phone_number(),
        'jobtitle': lambda f: f.job()
    },
    'lead': {
        'firstname': lambda f: f.first_name(),
        'lastname': lambda f: f.last_name(),
        'companyname': lambda f: f.company(),
        'subject': lambda f: f"Lead - {f.bs().title()}",
        'emailaddress1': lambda f: f.email(),
        'telephone1': lambda f: f.phone_number()
    },
    'opportunity': {
        'name': lambda f: f"Opportunity - {f.bs().title()}",
        'estimatedvalue': lambda f: round(random.uniform(10000, 1000000), 2),
        'estimatedclosedate': lambda f: (datetime.now() + timedelta(days=random.randint(30, 180))).isoformat(),
        'closeprobability': lambda f: random.randint(10, 90)
    },
    'quote': {
        'name': lambda f: f"Quote {random.randint(10000, 99999)}",
        'effectivefrom': lambda f: datetime.now().isoformat(),
        'effectiveto': lambda f: (datetime.now() + timedelta(days=30)).isoformat()
    },
    'invoice': {
        'name': lambda f: f"Invoice {random.randint(10000, 99999)}",
        'datedelivered': lambda f: datetime.now().isoformat(),
        'duedate': lambda f: (datetime.now() + timedelta(days=30)).isoformat()
    },
    'salesorder': {
        'name': lambda f: f"Sales Order {random.randint(10000, 99999)}",
        'requestdeliveryby': lambda f: (datetime.now() + timedelta(days=30)).isoformat()
    },
    'product': {
        'name': lambda f: f"{f.word().title()} {random.choice(['Pro', 'Plus', 'Premium'])}",
        'productnumber': lambda f: f"PROD-{random.randint(1000, 9999)}",
        'productstructure': lambda f: 1
    },
    'pricelevel': {
        'name': lambda f: f"{f.word().title()} Price List",
        'begindate': lambda f: datetime.now().isoformat()
    },
    'competitor': {
        'name': lambda f: f.company(),
        'websiteurl': lambda f: f.url()
    },

    # ===== CUSTOMER SERVICE ENTITIES =====
    'incident': {
        'title': lambda f: f"Case: {f.bs().title()}",
        'description': lambda f: f.text(max_nb_chars=200),
        'prioritycode': lambda f: random.randint(1, 3)
    },
    'contract': {
        'title': lambda f: f"Contract - {f.company()}",
        'contractnumber': lambda f: f"CNT-{random.randint(1000, 9999)}",
        'billingfrequencycode': lambda f: 1
    },
    'entitlement': {
        'name': lambda f: f"Entitlement - {f.word().title()}",
        'allocationtypecode': lambda f: 1
    },
    'knowledgearticle': {
        'title': lambda f: f.sentence(nb_words=6),
        'articlepublicnumber': lambda f: f"KB{random.randint(1000, 9999)}"
    },
    'queue': {
        'name': lambda f: f"{f.word().title()} Support Queue",
        'queueviewtype': lambda f: 0
    },
    'serviceappointment': {
        'subject': lambda f: f"Service - {f.bs().title()}",
        'scheduledstart': lambda f: (datetime.now() + timedelta(days=1)).isoformat(),
        'scheduledend': lambda f: (datetime.now() + timedelta(days=1, hours=2)).isoformat()
    },
    'equipment': {
        'name': lambda f: f"Equipment - {f.word().title()}"
    },
    'bookableresource': {
        'name': lambda f: f"{f.first_name()} {f.last_name()}",
        'resourcetype': lambda f: 3
    },

    # ===== FIELD SERVICE ENTITIES =====
    'msdyn_workorder': {
        'msdyn_name': lambda f: f"WO-{random.randint(1000, 9999)}",
        'msdyn_systemstatus': lambda f: 690970000,
        'msdyn_priority': lambda f: f"Priority {random.randint(1, 5)}"
    },
    'msdyn_agreement': {
        'msdyn_name': lambda f: f"Agreement - {f.company()}",
        'msdyn_systemstatus': lambda f: 690970000
    },
    'msdyn_actual': {
        'msdyn_description': lambda f: f.text(max_nb_chars=100),
        'msdyn_quantity': lambda f: round(random.uniform(1, 100), 2)
    },
    'msdyn_priority': {
        'msdyn_name': lambda f: f"Priority {random.randint(1, 10)}",
        'msdyn_levelofimportance': lambda f: random.randint(1, 10)
    },
    'msdyn_warehouse': {
        'msdyn_name': lambda f: f"Warehouse - {f.city()}",
        'msdyn_description': lambda f: f.text(max_nb_chars=100)
    },
    'msdyn_purchaseorder': {
        'msdyn_name': lambda f: f"PO-{random.randint(10000, 99999)}",
        'msdyn_orderedbyname': lambda f: f.name()
    },
    'msdyn_productinventory': {
        'msdyn_name': lambda f: f"Inventory - {f.word().title()}",
        'msdyn_qtyonhand': lambda f: random.randint(0, 1000)
    }
}
