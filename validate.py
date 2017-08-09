"""TC ETDMS Validator
Validates etdms for usage at Library and Archives Canada
(mandatory fields, non-repeatable fields, desired fields)
"""
import sys

import requests
import bs4


def check_url(base_url: str) -> bool:
    """Verify that url exist and gives us a status code 200"""
    try:
        res = requests.get(base_url)
        res.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        return False
    except requests.exceptions.Timeout as err:
        print("Request timeout for " + base_url)
        return False
    except requests.exceptions.TooManyRedirects as err:
        print("Too many redirects for " + base_url)
        return False
    except requests.exceptions.RequestException as err:
        print(err)
        return False
    print("INFO: url is valid")
    return True

def check_metadata_formats(base_url: str, metadata_format: str = '') -> bool:
    """Check which metadata formats are supported by the server"""
    formats_url = base_url + '?verb=ListMetadataFormats'
    available_formats = []
    usable_formats = ( \
        '(http://www.ndltd.org/standards/metadata/etdms/1.1/)' \
        '(http://www.ndltd.org/standards/metadata/etdms/1-1/)' \
        '(http://www.ndltd.org/standards/metadata/etdms/1.0/)' \
        '(http://www.ndltd.org/standards/metadata/etdms/1-0/)' \
    )
    res = requests.get(formats_url)
    soup = bs4.BeautifulSoup(res.text, "xml")
    formats = soup.find_all('metadataFormat')
    print("Available metadata formats (*=harvestable)")
    print("-----------------")
    for frmt in formats:
        if frmt.metadataNamespace.text in usable_formats:
            star = "*"
        else:
            star = " "
        print(star + frmt.metadataPrefix.text + '  (' + frmt.metadataNamespace.text + ')')
        available_formats.append(frmt.metadataPrefix.text)
    print("-----------------")
    if metadata_format != '' and metadata_format in available_formats:
        print('INFO: using format -> ' + metadata_format)
    elif metadata_format != '' and metadata_format not in available_formats:
        print('INFO: requested format <' + metadata_format + '> is not available')
        return False
    elif metadata_format == '':
        print('INFO: no metadata format selected. Please specify a format to complete the validation.')
        return False
    return True


def check_identify(base_url: str) -> bool:
    """Check that the server is OAI-PMH version 2.0"""
    identify_url = base_url + '?verb=Identify'
    try:
        res = requests.get(identify_url)
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(err)
        return False

    soup = bs4.BeautifulSoup(res.text, "xml")
    if soup.protocolVersion is None:
        print("Invalid OAI-PMH")
        return False
    if soup.protocolVersion.text != "2.0":
        print("Unknown OAI-PMH version : " + soup.protocolVersion)
        return False
    print('INFO: Server is OAI-PMH 2.0')
    return True


def check_these(base_url: str, metadata_format: str, dataset: str = "") -> bool:
    """Check the first these for mandatory fields and validity"""
    records_url = base_url \
        + "?verb=ListRecords" \
        + "&metadataPrefix=" + metadata_format
    if dataset != "":
        records_url += "&set=" + dataset
        print('INFO: using set -> ' + dataset)

    print("INFO: requested url -> " + records_url)

    try:
        res = requests.get(records_url)
        res.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(err)
        return False

    soup = bs4.BeautifulSoup(res.text, "xml")
    if soup.error is not None:
        print('ERROR: ' + soup.error.text)
        return False
    is_valid = True

    print("INFO: completeListSize = " + soup.resumptionToken['completeListSize'])

    # Mandatory fields
    if soup.thesis is None:
        print("ERROR: Missing <thesis> root element, this repository can't be harvested")
        return False
    if soup.thesis.title is None or soup.thesis.title.text == '':
        print("ERROR: Missing mandatory <title> field")
        is_valid = False
    if soup.thesis.creator is None or soup.thesis.creator.text == '':
        print("ERROR: Missing mandatory <creator> field")
        is_valid = False
    if soup.thesis.publisher is None or soup.thesis.publisher.text == '':
        print("ERROR: Missing mandatory <publisher> field")
        is_valid = False
    if soup.thesis.date is None or soup.thesis.date.text == '':
        print("ERROR: Missing mandatory <date> field")
        is_valid = False
    if soup.thesis.identifier is None or soup.thesis.identifier.text == '':
        print("ERROR: Missing mandatory <identifier> field")
        is_valid = False
    if soup.thesis.language is None or soup.thesis.language.text == '':
        print("ERROR: Missing mandatory <language> field")
        is_valid = False

    #Non repeatable fields
    if soup.thesis.date is not None and len(soup.thesis.date) > 1:
        print("ERROR: <date> is a non-repeatable field and currently appears " + len(soup.thesis.date) + ' times.')
        is_valid = False

    # Desired field
    if soup.thesis.subject is None or soup.thesis.subject.text == '':
        print("WARNING: <subject> is a desired field that is not present")
    if soup.thesis.description is None or soup.thesis.description.text == '':
        print("WARNING: <description> is a desired field that is not present")
    if soup.thesis.contributor is None or soup.thesis.contributor.text == '':
        print("WARNING: <contributor> is a desired field that is not present")
    if (soup.thesis.degree is None 
            or soup.thesis.degree.name is None
            or soup.thesis.degree.name == ''):
        print("WARNING: <degree><name> is a desired field that is not present")

    if not is_valid:
        print("ERROR: data is not formated properly, this feed can't be harvested")

    return is_valid


def main():
    """main function that check cli arguments all start everything"""
    if len(sys.argv) == 1:
        print("Enter an URL as the first argument")
        sys.exit(2)

    #demo_url = "https://etheses-test01.canadaeast.cloudapp.azure.com/oai/request"
    url = sys.argv[1]

    if len(sys.argv) >= 3 and sys.argv[2]:
        metadata_format = sys.argv[2]
    else:
        metadata_format = ''

    if len(sys.argv) >= 4 and sys.argv[3]:
        dataset = sys.argv[3]
    else:
        dataset = ''

    if (check_url(url)
            and check_identify(url)
            and check_metadata_formats(url, metadata_format)
            and check_these(url, metadata_format, dataset)):
        print("Validation completed successfuly")


if __name__ == "__main__":
    main()
