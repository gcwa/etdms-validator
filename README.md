# BAC-LAC etheses harvest-ability validator

Command line script to validate that a feed can be harvested by Library and Archives Canada for the Theses Canada Portal  https://www.bac-lac.gc.ca/eng/services/theses/Pages/theses-canada.aspx


## Installation

Install Python 3.5+ first. Using virtualenv is recommended

    python3 -m venv venv
    source ./venv/bin/activate

Install requiremets via PIP

    pip install -r requirements.txt


## Usage

Check valid OAI-PMH, list available/usable metatada formats, check ORE is available

    python3 validate.py https://etheses-test01.canadaeast.cloudapp.azure.com/oai/request

Check everything as in the previous example, and check metadata for `etdms11` format

    python3 validate.py https://etheses-test01.canadaeast.cloudapp.azure.com/oai/request etdms11
    
Same as before, but only check data set `col_20.500.11963_67`

    python3 validate.py https://etheses-test01.canadaeast.cloudapp.azure.com/oai/request etdms11 col_20.500.11963_67


## Sample output

    INFO: url is valid
    INFO: Server is OAI-PMH 2.0
    Available metadata formats (*=harvestable)
    -----------------
    *etdms11  (http://www.ndltd.org/standards/metadata/etdms/1.1/)
     didl  (urn:mpeg:mpeg21:2002:02-DIDL-NS)
     mods  (http://www.loc.gov/mods/v3)
     ore  (http://www.w3.org/2005/Atom)
     mets  (http://www.loc.gov/METS/)
     xoai  (http://www.lyncode.com/xoai)
     dim  (http://www.dspace.org/xmlns/dspace/dim)
     uketd_dc  (http://naca.central.cranfield.ac.uk/ethos-oai/2.0/)
     qdc  (http://purl.org/dc/terms/)
     oai_dc  (http://www.openarchives.org/OAI/2.0/oai_dc/)
     rdf  (http://www.openarchives.org/OAI/2.0/rdf/)
     marc  (http://www.loc.gov/MARC21/slim)
    *etdms  (http://www.ndltd.org/standards/metadata/etdms/1.0/)
    -----------------
    INFO: Server supports ORE
    INFO: using format -> etdms11
    INFO: requested url -> https://etheses-test01.canadaeast.cloudapp.azure.com/oai/request?verb=ListRecords&metadataPrefix=etdms11
    WARNING: <contributor> is a desired field that is not present
    Validation completed successfuly, metadata can be harvested
