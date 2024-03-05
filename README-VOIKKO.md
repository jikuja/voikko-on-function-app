# How to run spacy-fi / Voikko on Azure Function apps

Native library libvoikko1 and dictionaries will cause issues on some environments.

## Containerized version

Dockerfile installs `libvoikko1` `voikko-fi` debian packages. No other dependency downloads are needed for containerized version.

`.dockerignore` file has entry for `voikko` directory. It is used to ignore all files needed for code-based deployments.

The function app code itself will work without any modifications or conditional code.

See [README-DOCKER.md](README-DOCKER.md) for more details.

## Non-containerized version

Code-based Azure Function app does not allow installation of .deb files and therefore
native libraries and dictionary must be part of the function app source code and
libvoikko Python module and libvoikko1 requires some extra options

### Script to download native libraries and dictionary

`voikko/download-libraries.sh` file:

* Downloads and extract `.so` files from debian packages
* Downloads `libvoikko-1.dll` for Windows development
* Downloads standard dictionary

### Conditional code for Windows

Conditional code will do following extra steps:

* Setup libvoikko Python module correctly to find libraries and dictionaries
* Setup `VOIKKO_DICTIONARY_PATH` environment variable

Conditional code is turned on by setting `SETUP_VOIKKO_WINDOWS` environment variable to `true`

### Conditional code for Linux

Contitional code on function app will setup voikko to be used with libvoikko Python module on :

* load native dependencies of libvoikko1 with CDLL
* Setup libvoikko Python module correctly to find libvoikko1
* Setup `VOIKKO_DICTIONARY_PATH` environment variable

Conditional code is turned on by setting `SETUP_VOIKKO_LINUX` environment variable to `true`.

### How to run function locally with func core tools

* Setup `.venv`
* Install python dependencies: `pip install -r requirements.txt`
* Set `SETUP_VOIKKO_WINDOWS` or `SETUP_VOIKKO_LINUX` true in `local.settings.json` file
* Run functions with `func host start` or by other tooling

### How to run code-based version on local docker

Might be a good option if native dependencies cannot be installed system-wide:

* `docker build --tag azurefunctionsimagecode:v1.0.0 -f Dockerfile.code .`
* `docker run -e AzureWebJobsSecretStorageType=files -v ./.keys:/azure-functions-host/Secrets --name iddqd --rm -p 8080:80 -it -e AzureFunctionsJobHost__logging__logLevel__default=Trace -e CONTAINER_NAME=XYZ -e SETUP_VOIKKO_LINUX=true  azurefunctionsimagecode:v1.0.0`

`-e SETUP_VOIKKO_LINUX=true` enables linux-specific setop. For other command-line arguments check [README-DOCKER.md](README-DOCKER.md).

## Lessons learned

Containerized Function Apps or Azure Container Apps are better then code-based fucntion apps if extra native dependencies are needed. Python / function app runtime hides too much information e.g. when loading incompatible .so files.

Maintaining compatible set of .so files also requires extra work.
