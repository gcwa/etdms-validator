"""TC ETDMS Validator
super duper ultra basic web page for internal use by non dev
"""
from bottle import get, post, request, run
from validate import *
import sys, io

@get('/')
def home():
    """barebone form to ask user for information"""
    return '''
        <form action="/" method="post">
            OAI url: <input name="url" type="text" /> *required<br> 
            Metadata format: <input name="metadataformat" type="text" /><br>
            Set: <input name="dataset" type="text" /><br>
            <input value="Validate" type="submit" />
        </form>
    '''


@post('/')
def validate_feed():
    """run cli script and print output"""
    url = request.forms.get('url')
    metadata_format = request.forms.get('metadataformat')
    dataset = request.forms.get('dataset')
    # Hacking stdout, this is how you use a non-library as a library
    #  when in a rush
    stdout = sys.stdout
    sys.stdout = io.StringIO()

    if (check_url(url)
            and check_identify(url)
            and check_metadata_formats(url, metadata_format)
            and check_these(url, metadata_format, dataset)):
        print("Validation completed successfuly, metadata can be harvested")

    output = sys.stdout.getvalue()
    sys.stdout = stdout
    return output.replace('<', '[').replace('>', ']').replace('\n', '<br>')


run(host='localhost', port=8080, debug=True, server='gunicorn')