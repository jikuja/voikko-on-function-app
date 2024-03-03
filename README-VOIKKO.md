# How to add native dependencies conditionally

Python libvoikko module haas depdendcy to native libvoikko.so file, so files dependencies and dictionary files

## Containerized version

Dockerfile installs `libvoikko1` `voikko-fi` debian packages. No other dependency downloads are needed for containerized version.

.dockerignore has entry for `voikko`. It is used to ignore all files needed for code-based deployments.

The function app code itself will work without any modifications

## Non-containerized version

To make running function app as code-based function app on a service on Windows development machines
project has voikko/download-libraries.sh file. It will do following:

* Download and extract .so files from debian packages
* Download libvoikko-1.dll for Windows development
* Download standard dictionary

## Function app core tools version on Windows machine

Conditional code will do following extra steps:

* Setup libvoikko Python module correctly to find libraries and dictionaries

## Function app on code-based Azure function app service

Contitional code on function app will setup voikko to be used with libvoikko Python module on :

* load native dependencies of libvoikko1 with CDLL
* Setup libvoikko Python module correctly to find libvoikko1
* Do extra setup for spacy_fi_experimental_web_md to find standard finnish dictionary