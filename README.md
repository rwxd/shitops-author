# Tool to produce shitposts for [ShitOps](https://shitops.de)

## Description

Generates engineering-blog like posts full of stupid things with ChatGPT.

## Usage

```bash
export OPENAI_TOKEN=""
```

```bash
nix develop -c $SHELL
poetry env use python3.11
poetry update
```

```bash
poetry run python3 -m author --debug --dest ~/dev/shitops/content/posts --google-service-account ./shitops.json
```

```bash
docker run -v "$PWD:/app" -e "OPENAI_TOKEN=$OPENAI_TOKEN" test -- --debug --dest ./output --google-service-account ./shitops-d2b15bf38d97.json --az-subscription-key ""
```

## Azure Speech Service

```bash

```
