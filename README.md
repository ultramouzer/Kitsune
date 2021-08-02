# Kitsune Archiver

## Setup
1. Clone the repo and switch to the created folder:
    ```sh
    git clone --recurse-submodules https://github.com/OpenYiff/Kitsune.git kitsune
    cd kitsune
    ```
2. Create `config.py` and `.env` files and set their values if needed:
    ```sh
    cp config.py.example config.py
    cp .env.example .env
    ```
3. Create a virtual environment:
    ```sh
    pip install virtualenv # install the package if it's not installed
    virtualenv venv
    ```
4. Activate the virtual environment:
    ```sh
    source venv/bin/activate # venv\Scripts\activate on Windows
    ```
5. Install python packages:
    ```sh
    pip install --requirement requirements.txt
    ```
6. Start Kitsune:
    ```sh
    flask run
    ```
