# BAC-LAC etheses harvest-ability validator

Command line script to validate that a feed can be harvested by Library and Archives Canada for the Theses Canada Portal  https://www.bac-lac.gc.ca/eng/services/theses/Pages/theses-canada.aspx

## Installation

Using virtualenv is recommended

    pip install -r requirements.txt
    
## Usage

Check valid OAI-PMH, list available/usable metatada formats, check ORE is available

    python3 validate.py https://etheses-test01.canadaeast.cloudapp.azure.com/oai/request

Check everything as in the previous example, and check metadata for `etdms11` format

    python3 validate.py https://etheses-test01.canadaeast.cloudapp.azure.com/oai/request etdms11
    
Same as before, but only check data set `col_20.500.11963_67`

    python3 validate.py https://etheses-test01.canadaeast.cloudapp.azure.com/oai/request etdms11 col_20.500.11963_67
