# MIET union

## Description
Web application of the union of the MIET Institute
## Installation env

``` bash
git clone https://github.com/IMB-a/miet_union
cd miet_union
python -m venv .venv
cd .venv/Scripts
activate # (for windows)
source activate # (for linux)
cd ../..
```

## Installation app
``` bash
pip install -r requirements.txt # pip3 for linux
python manage.py makemigrations
python manage.py migrate
```

## Usage
``` bash
python manage.py runserver
```
