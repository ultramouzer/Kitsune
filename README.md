# Kitsune Archiver

## Setup
This repo used mainly as a submodule for the [main repo](https://github.com/OpenYiff/Kemono2) and is pretty hard to work on outside of it.
Therefore follow its [setup section](https://github.com/OpenYiff/Kemono2#setup) first to get the files.

## Development
While it is mainly used as a submodule, contributing code to this repo is easier with some local setup.

Assuming you are in the `archiver` folder:

1. Create `config.py` file:
    ```sh
    cp config.py.example config.py
    ```

2. Create a virtual environment:
    ```sh
    pip install virtualenv # install the package if it's not installed
    virtualenv venv
    ```
3. Activate the virtual environment:
    ```sh
    source venv/bin/activate # venv\Scripts\activate on Windows
    ```
4. Install python packages:
    ```sh
    pip install --requirement requirements.txt
    ```

This way you'll have all IDE juice while working on it as a submodule.
