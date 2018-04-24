## Usage

- For local development, start https://github.com/schul-cloud/schulcloud-content on localhost.
- Run `src/app.py`

### Configuration

Configuration uses environment variables that are parsed in `src/settings.py`.
For docker you can use `local.env` to overwrite the environment variables. `local.env` is ignored by `git`.
For local usage, no configuration should be necessary.
An Api Key for Deutsche Digitale Bibliothek is required for usage of the api
(see local.env.example)

https://www.deutsche-digitale-bibliothek.de/user/registration


## Run crawler  in docker context, connected to existing network : "schulcloudserver_schulcloud-server-network"

`docker-compose up`
