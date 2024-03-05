import json
import logging
import os

import azure.functions as func
from libvoikko import Voikko
import spacy

def _requires_voikko_setup_linux():
    return 'SETUP_VOIKKO_LINUX' in os.environ and os.environ['SETUP_VOIKKO_LINUX'] == 'true'

def _requires_voikko_setup_windows():
    return 'SETUP_VOIKKO_WINDOWS' in os.environ and os.environ['SETUP_VOIKKO_WINDOWS'] == 'true'

# TODO: OS X support. Or just use homebrew

# Turn on linux-specific extra native code/ dictionary config
if _requires_voikko_setup_linux():
    DIRECTORY = 'voikko'

    # load native dependencies manually from voikko directory
    from ctypes import CDLL
    CDLL(os.path.dirname(__file__) + os.sep + DIRECTORY + os.sep + 'libarchive.so.13')
    CDLL(os.path.dirname(__file__) + os.sep + DIRECTORY + os.sep + 'libhfstospell.so.11')

    # Setup libvoikko to load native libvoikko.so.1 from voikko directory
    Voikko.setLibrarySearchPath(os.path.dirname(__file__) + os.sep + DIRECTORY)

    # Setup libvoikko1.so.1 to load dictionary files from voikko
    if not 'VOIKKO_DICTIONARY_PATH' in os.environ:
        os.environ['VOIKKO_DICTIONARY_PATH'] = os.path.dirname(__file__) + os.sep + DIRECTORY

# Turn on windows-specific extra native code/ dictionary config
if _requires_voikko_setup_windows():
    DIRECTORY = 'voikko'
    # Setup libvoikko to load native libvoikko-1.dll from voikko directory
    Voikko.setLibrarySearchPath(os.path.dirname(__file__) + os.sep + DIRECTORY)

    # Setup libvoikko-1.dll load dictionary files from /home/site/wwwroot/voikko
    if not 'VOIKKO_DICTIONARY_PATH' in os.environ:
        os.environ['VOIKKO_DICTIONARY_PATH'] = os.path.dirname(__file__) + os.sep + DIRECTORY

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
