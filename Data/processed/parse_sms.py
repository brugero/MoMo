import xml.etree.ElementTree as ET
import json

# Path to your XML file
xml_file = "modified_sms_v2.xml"  # Make sure this file is in the same folder

def parse_xml_to_list(path):
    """
    Parse the XML file and convert each <sms> record into a dictionary.
    Returns a list of dictionaries.
    """
    tree = ET.parse(path)
    root = tree.getroot()
    transactions = []

    for sms in root.findall("sms"):
        record = {}
        for child in sms:
            record[child.tag] = child.text  # Each XML tag becomes a key
        # Convert id to integer for easier handling
        if "id" in record:
            record["id"] = int(record["id"])
        transactions.append(record)

    return transactions

if __name__ == "__main__":
    # Parse XML
    transactions = parse_xml_to_list(xml_file)

    # Print transactions as JSON (pretty)
    print(json.dumps(transactions, indent=2))