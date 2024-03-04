# How to run containerized function apps locally

## Current state of containerized function apps local testing

[Official documentation](https://learn.microsoft.com/en-us/azure/azure-functions/functions-create-container-registry?tabs=acr%2Cbash&pivots=programming-language-python) offers following guidance:

> func new --name HttpExample --template "HTTP trigger" --authlevel anonymous

and

> Because the HTTP triggered function you created uses anonymous authorization, you can call the function running in the container without having to obtain an access key. For more information, see authorization keys.

I personally want to avoid modifying function code to run it in particular environment.

Documentation issue tracker has more suitable [answer](https://github.com/Azure/azure-functions-host/issues/4147#issuecomment-477431016): `option 2`. 
This option has not been added into documentation: [ticket](https://github.com/MicrosoftDocs/azure-docs/issues/45642)

### Local logging level changes

`AzureFunctionsJobHost__*` environment variable can be used to [override](https://learn.microsoft.com/en-gb/azure/azure-functions/functions-host-json#override-hostjson-values) host.json settings. Especially [logging levels](https://learn.microsoft.com/en-gb/azure/azure-functions/configure-monitoring?tabs=v2#configure-log-levels)

`CONTAINER_NAME` can be used to [enable worker logging](https://github.com/Azure/azure-functions-host/issues/6693).


## Setup

Copy directory `.keys-template` to `.keys` and modify `.keys/host.json` if needed.

`masterKey.value` is the value function app runtime will use as master key.

Example:

```JSON
{
  "masterKey": {
    "name": "master",
    "value": "iqkfa",
    "encrypted": false
  },
  "functionKeys": [ ]
}
```

## Build image

* `docker build --tag azurefunctionsimage:v1.0.0 .`

The resulting image will have entrypoint, all runtime files, function apps code and function app code depencies.

### Run

* `docker run -e AzureWebJobsSecretStorageType=files -v ./.keys:/azure-functions-host/Secrets --name iddqd --rm -p 8080:80 -it -e AzureFunctionsJobHost__logging__logLevel__default=Trace -e CONTAINER_NAME=XYZ azurefunctionsimage:v1.0.0`

Explanation for command line arguments:

* `-e AzureWebJobsSecretStorageType=files` -- tells function app runtime to load secret storage from file system
* `-v ./.keys:/azure-functions-host/Secrets` -- mounts `.keys/host.json` configuration file we created earlier as secret storage
* `--name iddqd` -- setup a name for running container instead of using random names
* `--rm` -- delete container as soon as it is not running
* `-p 8080:80` -- port forward port 80 to port 8080 on host's localhost
* `-it` -- keep stdin open to see logs and allocate pseudo tty
* `-e CONTAINER_NAME=XYZ` enable worked logs (optional)
* `-e AzureFunctionsJobHost__logging__logLevel__default=Trace` -- override host.json logging level (optional)

### "SSH" into container

* `docker exec -it iddqd bash`

## API calls into container

Secret key is being passed as `code` query parameter

`curl -s http://localhost:8080/api/function\?code=idkfa | jq .`

`curl -s --data-binary @- -X POST http://localhost:8080/api/function\?code=idkfa | jq .`

`echo 'Rongorongo on Pääsiäissaarella rapanuin kielessä käytetty tulkitsematon kirjoitusjärjestelmä. Rongorongon kirjoitusta on yritetty tulkita, mutta siinä ei ole onnistuttu. Sanan ”rongorongo” merkityksestä ei ole varmaa tietoa. Viimeiset rongorongon ymmärtäjät hävisivät 1800-luvulla. Näihin päiviin asti on säilynyt 26 puulaattaa, joissa on rongorongolla kirjoitettua tekstiä. Merkkejä on yhteensä noin 14 000.' | curl -s --data-binary @- -X POST http://localhost:8080/api/function\?code=idkfa | jq .`

## ALternative approaches

* Check if function app authentication can be disabled by using some other undocumented environment variable
  * Initial answer: No
