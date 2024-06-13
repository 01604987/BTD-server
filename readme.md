# Server
This repository contains server code for receiving, preprocessing and plotting raw accelerometer data from the m5stick c plus.

# How to install
- Make sure python ``3.x`` is installed. Only tested with python ``3.11``
- ``git clone https://github.com/01604987/BTD-server.git`` this repository
- Navigate into the cloned folder
- Run ``python -m venv venv`` to create a virtual environment
- In your chosen IDE make sure to select the python venv interpreter
- activate the virtual env (from terminal).
    - Linux: ``source venv/bin/activate``
    - Windows: ``Set-ExecutionPolicy Unrestricted`` <br>
        then: ./venv/Script/activate <br>
        optionally: ``Set-ExecutionPolicy Restricted`` to revert policy. (Will be automatically reverted after session)
    - Mac: ``?``
- run ``pip install -r requirements.txt``
- start ``main.py``


# How to use
- Configure ESP-IDF menu config with correct ip and ports
    - ip adress: check on host
        - Windows: ipconfig
        - Mac: ifconfig | grep "inet " | grep -v 127.0.0.1
    - port: 5050

- Configure ESP-IDF network/wifi connection

- Run server with main.py
- 3 plots should appear
    - upper left: raw accelerometer scaled by 0.00048808125 (see BTD-Framework)
    - upper right: raw gyroscope scaled by 0.007633587786 (equal to degrees/sec)
    - lower left: orientation in x,y axis (tilt) 




# Threads
- Server (handles clinet connections) 2x
    - TCP read/write
    - UDP read
- Data storer (starts if queue not empty)
- Plotter (main)

# TODO
- terminate program and close threads for udp
- apply filters to raw accel values



# Notes

- accel offset: {}
- gyro offset: {5, 25, -43}