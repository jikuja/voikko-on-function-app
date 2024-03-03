# How to run containerized Azure function on local machine

This example is running simple function containing following components

* Python
* spacy_fi_experimental_web_md python module
* libvoikko as dependency
* Native library libvoikko1 as OS packaging dependency

## Setup

Copy directory `.keys-template` to `.keys` and modify `.keys/host.json` if needed.

`masterKey.value` is the value function app runtime will use as master key.

## How to run

### Build image

* `docker build --tag azurefunctionsimage:v1.0.0 .`

The resulting image will have entrypoint, all runtime files, runtime dependencies function code and function code depencies.

### Run

* `docker run -e AzureWebJobsSecretStorageType=files -v ./.keys:/azure-functions-host/Secrets --name iddqd --rm -p 8080:80 -it azurefunctionsimage:v1.0.0`

Explanations:

* `-e AzureWebJobsSecretStorageType=files` -- tells function app runtime to load secret storage from file system
* `-v ./.keys:/azure-functions-host/Secrets` -- mounts `.keys/host.json` configuration file we created earlier as secret storage
* `--name iddqd` -- setup a name for running container instead of using random names
* `--rm` -- delete container as soon as it is not running
* `-p 8080:80` -- port forward port 80 to port 8080 on host's localhost
* `-it` -- keep stdin open to see logs and allocate pseudo tty

### "SSH" into container

* `docker exec -it iddqd bash`

## API calls into container

`curl -s http://localhost:8080/api/function\?code=idkfa | jq .`

`curl -s --data-binary @- -X POST http://localhost:8080/api/function\?code=idkfa | jq .`

`echo 'Rongorongo on Pääsiäissaarella rapanuin kielessä käytetty tulkitsematon kirjoitusjärjestelmä. Rongorongon kirjoitusta on yritetty tulkita, mutta siinä ei ole onnistuttu. Sanan ”rongorongo” merkityksestä ei ole varmaa tietoa. Viimeiset rongorongon ymmärtäjät hävisivät 1800-luvulla. Näihin päiviin asti on säilynyt 26 puulaattaa, joissa on rongorongolla kirjoitettua tekstiä. Merkkejä on yhteensä noin 14 000.' | curl -s --data-binary @- -X POST http://localhost:8080/api/function\?code=idkfa | jq .`
