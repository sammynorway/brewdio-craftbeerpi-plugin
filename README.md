# cbpi4-brewdio

A CraftBeerPi 4 plugin that synchronizes recipes from Brewdio and connects the brewing
workflow back to Brewdio.

## What it does

- Reads recipes from Brewdio's authenticated integration API.
- Creates managed recipes in CraftBeerPi's normal recipe book.
- Creates a Brewdio batch when brewing starts in CraftBeerPi.
- Lets Brewdio calculate and record inventory deductions exactly once.
- Converts mash temperatures and times and adds boil-hop alerts.

The plugin only manages files named `brewdio_<recipe-id>.yaml`. It does not modify
recipes created directly in CraftBeerPi.

## Relationship to Brewdio

This repository contains only the CraftBeerPi 4 plugin: recipe conversion,
synchronization, batch-start handling, configuration, and plugin tests.

The main [Brewdio repository](https://github.com/sammynorway/brewdio) contains the
application, inventory calculations, authentication, integration-key management,
Recipe API, and Batch API. The two projects are kept separate so the plugin can be
installed and released without bundling it into the Brewdio application.

Compatible Brewdio server API support is required for this plugin to synchronize
recipes and create inventory-aware batches.

## Requirements

- CraftBeerPi 4
- Python 3.10 or newer
- A running Brewdio server that CraftBeerPi can reach
- A Brewdio integration key with `recipes:read` and `batches:write` scopes

## Installation

Install the plugin into the CraftBeerPi pipx environment:

```bash
pipx runpip cbpi4 install https://github.com/sammynorway/brewdio-craftbeerpi-plugin/archive/main.zip
```

Create the configuration file:

```bash
mkdir -p ~/craftbeerpi/config
curl -fsSL https://raw.githubusercontent.com/sammynorway/brewdio-craftbeerpi-plugin/main/settings.example.json \
  -o ~/craftbeerpi/config/brewdio.json
chmod 600 ~/craftbeerpi/config/brewdio.json
```

Edit `~/craftbeerpi/config/brewdio.json` and set:

- `base_url`: the URL of the Brewdio server, for example `http://192.168.1.100:3000`
- `kettle_id`: the CraftBeerPi ID of the brew kettle
- `sensor_id`: the CraftBeerPi ID of the kettle temperature sensor
- `sync_interval_seconds`: how often recipes are refreshed, with a minimum of 15 seconds

Store the API key without displaying it or adding it to shell history:

```bash
~/.local/share/pipx/venvs/cbpi4/bin/python \
  -m cbpi4_brewdio.configure ~/craftbeerpi/config/brewdio.json
```

Restart CraftBeerPi after configuring the plugin.

## How synchronization works

The plugin refreshes recipes periodically. Each managed recipe starts with a
`BrewdioStartBatchStep`. When that step runs, it asks Brewdio to create a batch and
apply the server-calculated inventory plan before CraftBeerPi advances to the first
mash step.

The request uses an idempotency key. Retrying the same CraftBeerPi step therefore does
not create a second batch or deduct ingredients twice. If Brewdio rejects the request,
the recipe stays on the start step and heating does not begin.

## Updating

Run the installation command again with `--force-reinstall`, then restart CraftBeerPi:

```bash
pipx runpip cbpi4 install --force-reinstall \
  https://github.com/sammynorway/brewdio-craftbeerpi-plugin/archive/main.zip
```

## Security

`brewdio.json` contains an API key. Keep the file private (`chmod 600`), never commit
it, and revoke the key in Brewdio if it may have been exposed. The example file contains
no key.

## Development

Run the converter tests from the repository root:

```bash
~/.local/share/pipx/venvs/cbpi4/bin/python -m unittest discover -s tests
```

## License

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE).
