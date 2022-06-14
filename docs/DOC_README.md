# Orquestra Core Docs

This readme is not for the whole of orquestra-core, this is just for information on the docs and how to build them. For this whole README we'll assume that you've `cd`ed into the docs directory.

## Requirements

### Doc-specific requirements

_Note: if you want to activate a [virtualenvironment](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/) do that before installing the requirements_

The docs have their own requirements, found in the `requirements.txt` file. Install those requirements with `pip install -r requirements.txt`

### Installing Orquestra Core to run examples

If you want to be able to run the examples in the docs, install the actual orquestra-core package: `cd .. && pip install . && cd docs`

### Downloading repos for autoapi building

In order for autoapi to build the API docs, the repositories we want the API for must be downloaded. This can be done with `make update`

## Building the docs

Building the docs can be done with `make html`

## Viewing the docs

Once the docs are built, they can be opened in browser with `open _build/html/index.html`
