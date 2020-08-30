# MIET union

## Description
Web application of the union of the MIET Institute
## Installation env (linux)

``` bash
git clone https://github.com/IMB-a/miet_union
cd miet_union
python3 -m venv venv
source venv/Scripts/bin/activate
```

## Installation app (linux)
``` bash
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
```

## Usage
``` bash
python3 manage.py runserver
```
