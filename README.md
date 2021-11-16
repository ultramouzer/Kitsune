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
    cp redis_map.py.example redis_map.py
    ```

2. Create a virtual environment:
    ```sh
    pip install virtualenv # install the package if it's not installed
    virtualenv --upgrade-embed-wheels # makes it easier to manage python versions
    virtualenv --python 3.8 venv
    ```
3. Activate the virtual environment:
    ```sh
    source venv/bin/activate # venv\Scripts\activate on Windows
    ```
4. Install python packages:
    ```sh
    pip install --requirement requirements.txt
    ```

5. Install `pre-commit` hooks:
    ```sh
    pre-commit install --install-hooks
    ````

This way you'll have all IDE juice while working on it as a submodule.

### IDE-specific steps
#### VSCode
On windows install `libmagic` DLL to not crash on debugging:
```sh
pip install python-magic-bin
```

<!-- https://fadil-nohur.medium.com/resolving-intra-project-imports-in-python-a-simple-guide-visual-studio-code-98472b0a8f59 -->
Install the project inside your virtual environment for `Run Python File in Terminal` command to work.
```sh
py -m pip install -e .
```


### Other steps
#### Updating `pre-commit` hooks
1. Add an entry to the `.pre-commit-config.yaml` file
2. Update the hooks:
    ```sh
    pre-commit autoupdate --freeze
    ```
3. Install the hooks:
    ```sh
    pre-commit install --install-hooks
    ```
