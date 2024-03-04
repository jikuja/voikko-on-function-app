# How to run spacy-fi / Voikko on Azure Function apps

Native library libvoikko1 and dictionaries will cause issues on some environments.

## Containerized version

Dockerfile installs `libvoikko1` `voikko-fi` debian packages. No other dependency downloads are needed for containerized version.

`.dockerignore` file has entry for `voikko` directory. It is used to ignore all files needed for code-based deployments.

The function app code itself will work without any modifications or conditional code.

## Non-containerized version

Code-based Azure Function app does not allow installation of .deb files and therefore
native libraries and dictionary must be part of the function app source code.

### Script to download native libraries and dictionary

`voikko/download-libraries.sh` file:

* Download and extract `.so` files from debian packages
* Download `libvoikko-1.dll` for Windows development
* Download standard dictionary

### Conditional code for Windows development

Conditional code will do following extra steps:

* Setup libvoikko Python module correctly to find libraries and dictionaries

## Conditional code fpr code-based Azure function app service instance

Contitional code on function app will setup voikko to be used with libvoikko Python module on :

* load native dependencies of libvoikko1 with CDLL
* Setup libvoikko Python module correctly to find libvoikko1
* Set `VOIKKO_DICTIONARY_PATH` environment variable to control libvoikko1: needed for spacy-fi that does not support `Voikko.setLibrarySearchPath()`
