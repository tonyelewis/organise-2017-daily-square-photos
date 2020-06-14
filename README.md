# organise-2017-daily-square-photos

## On desktop

~~~sh
python3.8 -m venv --prompt $( basename $PWD ) .venv
source .venv/bin/activate
pip install wheel
pip install -r requirements.txt
~~~

~~~sh
pip install -r requirements.dev.txt
python -m pytest
~~~

~~~sh
source .venv/bin/activate
./organise.py
~~~

## On diskstation

~~~sh
rsync -av --exclude '.venv' lewis@192.168.178.23:/home/lewis/organise-2017-daily-square-photos/ /volume1/tony/organise-2017-daily-square-photos/
cd /volume1/tony/organise-2017-daily-square-photos/
python3 -m venv .venv

cd /volume1/tony/organise-2017-daily-square-photos/
source .venv/bin/activate
./organise.py
~~~
