#!/bin/bash

python combank.py &
python ndb.py 2>/dev/null &
python hnb.py &
python sampath.py &
python seylan.py &
python nationstrust.py &
wait

echo -e "\n Combining csv files...!"
python combine.py
