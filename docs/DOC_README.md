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

## Contributing to these docs

### rst heading conventions

RestructuredText is very nice with the heading conventions, allowing almost anything to work in a file as long as it's consistent. However, we want to maintain readability and consistency across many files and projects, so here are our standard rst header conventions:

Title: over and under-line with `=========================`

Heading 1: under-line with `======================`

Heading 2: under-line with `--------------------`

Heading 3: under-line with `~~~~~~~~~~~~~~~~~~`

Anything beyond that, please pick something and add what you picked to the above list

### Graphic Best Practices

If you're going to create a graphic from scratch, to keep style consitent, please create the graphic using [excalidraw](https://excalidraw.com/), an online whiteboarding/graphic creation tool.

When you export your graphic as a PNG, use the "embed scene" option so if the graphic ever needs to be updated in the future, it can be done easily.
