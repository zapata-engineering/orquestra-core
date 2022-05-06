# orquestra-python-template
This is a template repository for Orquestra Python projects.

After creating repository from this template, make sure to follow the steps below:

1. Specify license. Supply LICENSE file and fill license entry in `setup.cfg` accordingly.
2. Update `setup.cfg`. At the very least update the following fields:
   - `[metadata]` section: `name`, `description`, `license`, `license_file`, 
   - `install_requires` in `[options]` section. You don't have to do this at the very beginning and you may add requirements as you go, but be warry that the ones present in this repository are only example ones and may not be applicable to your project.
3. Substitute an example `orquestra.pythontemplate` package `src/` directory with your actual code. Remember, that `orquestra` is a namespace package, so you *cannot* put an `__init__.py` in `src/orquestra` directory. Remove tests for the dummy package and replace them with meaningful ones as you develop your package.
4. Remove this instruction and replace it with a meaningful description of your package.
