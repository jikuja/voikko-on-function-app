import json
import logging
import os

import azure.functions as func
from libvoikko import Voikko
import spacy

def _is_running_in_docker():
    return os.path.exists('/.dockerenv') or ('RUNNING_IN_DOCKER' in os.environ and os.environ['RUNNING_IN_DOCKER'] == 'true')

def _is_running_on_azure():
    return os.environ.get('WEBSITE_SITE_NAME') is not None and os.environ.get('WEBSITE_INSTANCE_ID') is not None

def _is_running_on_windows():
    return os.name == 'nt'

# Running on code-based Azure function app instance
if not _is_running_in_docker() and _is_running_on_azure():
    # load native dependencies manually from voikko directory
    from ctypes import CDLL
    CDLL('voikko/libarchive.so.13')
    CDLL('voikko/libhfstospell.so.11')

    # Setup libvoikko to load native libvoikko.so.1 from voikko directory
    Voikko.setLibrarySearchPath('voikko')

    # Setup libvoikko.so.1 to load dictionary files from /home/site/wwwroot/voikko
    # TODO: text on Azure
    os.environ['VOIKKO_DICTIONARY_PATH'] = '/home/site/wwwroot/voikko'

# running on Windows
if _is_running_on_windows() and not _is_running_in_docker():
    # Setup libvoikko to load native libvoikko-1.dll from voikko directory
    Voikko.setLibrarySearchPath('voikko')

    # Setup libvoikko-1.dll load dictionary files from /home/site/wwwroot/voikko
    # TODO: test
    # os.environ['VOIKKO_DICTIONARY_PATH'] = os.path.dirname(__file__) + os.pathsep + 'voikko'

app = func.FunctionApp()

@app.route(route="function", auth_level=func.AuthLevel.FUNCTION)
def function(req: func.HttpRequest) -> func.HttpResponse:
    nlp = spacy.load('spacy_fi_experimental_web_md')
    doc = nlp(req.get_body().decode("utf-8") or 'Hän ajoi punaisella autolla.')

    # collect verbs
    verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
    logging.info(verbs)

    # collect entities
    entities = [{ 'text': entity.text, 'label': entity.label_ } for entity in doc.ents]
    logging.info(entities)

    result = {
        'verbs': verbs,
        'entities': entities
    }
    logging.info(result)
    return func.HttpResponse(json.dumps(result))
