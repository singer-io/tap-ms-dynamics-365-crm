from xml.etree import ElementTree as ET

NS = {
    "edmx": "http://docs.oasis-open.org/odata/ns/edmx",
    "edm": "http://docs.oasis-open.org/odata/ns/edm"
}

def flatten_entity_attributes(attributes: list) -> dict:
    flat_attributes = {}

    for attr in attributes:
        logical_name = attr.get('LogicalName')
        dynamics_type = attr.get('PropertyType')

        flat_attributes.update({logical_name: {'type': dynamics_type}})

    return flat_attributes

def transform_metadata_xml(xml: str) -> dict:
    tree = ET.fromstring(xml)

    data_service = tree.find("edmx:DataServices", NS)
    entities = data_service.find("edm:Schema", NS)

    entity_def = {}
    for elem in entities.findall("edm:EntityType", NS):
        # Only process entities that have child elements and a Key element
        if len(elem) > 0 and elem.find("edm:Key", NS) is not None:
            entity_key = elem.find("edm:Key", NS).find("edm:PropertyRef", NS).get("Name")
            entity_name = elem.get("Name")
            base_type = elem.get("BaseType")

            props = []
            for prop in elem.findall("edm:Property", NS):
                prop_name = prop.get("Name")
                prop_type = prop.get("Type")
                props.append({"LogicalName": prop_name, "PropertyType": prop_type})

            entity_def.update({entity_name: {
                "Key": entity_key,
                "Properties": props,
                "BaseType": _strip_namespace(base_type),
            }})

    _resolve_inherited_properties(entity_def)

    return entity_def

def _strip_namespace(qualified_name: str) -> str:
    """Strips the leading namespace (e.g. `Microsoft.Dynamics.CRM.`) from a
    fully-qualified EDM type name, returning just the local entity name."""
    if not qualified_name:
        return None
    return qualified_name.rsplit(".", 1)[-1]

def _resolve_inherited_properties(entity_def: dict) -> None:
    """Merges properties declared on `BaseType` entities into every derived
    entity, in-place.

    Dynamics' `$metadata` XML declares common fields (e.g. `subject`,
    `createdon`, `modifiedon`) only once on a base entity type such as
    `activitypointer`, and derived activity entity types (e.g. `email`,
    `task`, `appointment`) only list their own additional properties. Without
    resolving `BaseType`, those inherited fields are invisible to callers,
    causing `modifiedon` to appear missing and streams to be incorrectly
    built as FULL_TABLE instead of INCREMENTAL.
    """
    resolved = set()

    def resolve(entity_name, visiting):
        if entity_name in resolved or entity_name not in entity_def:
            return
        if entity_name in visiting:
            return  # guard against circular BaseType references
        visiting.add(entity_name)

        entity = entity_def[entity_name]
        base_type = entity.get("BaseType")
        if base_type:
            resolve(base_type, visiting)
            if base_type in entity_def:
                existing_props = {prop["LogicalName"] for prop in entity["Properties"]}
                inherited_props = [
                    prop for prop in entity_def[base_type]["Properties"]
                    if prop["LogicalName"] not in existing_props
                ]
                entity["Properties"] = entity["Properties"] + inherited_props

        resolved.add(entity_name)

    for name in list(entity_def.keys()):
        resolve(name, set())
