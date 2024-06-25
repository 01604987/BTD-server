# Server
This repository contains server code for receiving, pre-/postprocessing, plotting of IMU data from the M5 Stick C Plus. This application was built for a handsfree, ubiqutous and wearable computing project, "Smart Presenter", which allows for intuitive gesture to control Mouse and Keyboard events. Workflow, process and ideation of this project can be in this [Miro board](https://miro.com/app/board/uXjVKQi3msY=/?share_link_id=143508401314). Included are a complete set of presentations and their accompanying video recordings for Milestone 2/3 and a small image gallery.

# Hardware
- [M5 Stick C Plus ESP32-PICO Mini IoT Development Kit](https://shop.m5stack.com/products/m5stickc-plus-esp32-pico-mini-iot-development-kit) ``required``
- Middle button on the M5 Stick ``for testing``
- Right button on the M5 Stick ``for testing``
- Glove with touch capacitive fingertips
- Wires connecting touch capacitive fingertips to GPIO pins
- Pull up resistor: 10k ohm
- GPIO 26 (index finger)
- GPIO 36 (middle finger)
- 3.3v
- GND

A simple wiring diagram can also be found in our [Miro board](https://miro.com/app/board/uXjVKQi3msY=/), with proper setup of pull-up resistors that are required for the configured buttons on the M5 Stick C Plus.

# How to install the Server
- Make sure python ``3.11`` is installed.
- ``git clone https://github.com/01604987/BTD-server.git`` this repository
- Navigate into the cloned folder
- Run ``python -m venv venv`` to create a virtual environment
- In your chosen IDE make sure to select the python venv interpreter
- activate the virtual env (from terminal).
    - Linux: ``source venv/bin/activate``
    - Windows: ``Set-ExecutionPolicy Unrestricted`` <br>
        then: ./venv/Script/activate <br>
        optionally: ``Set-ExecutionPolicy Restricted`` to revert policy. (Will be automatically reverted after session)
    - Mac: ``source venv/bin/activate``
- run ``pip install -r requirements.txt``
    - for Mac run ``pip install -r requirements_mac.txt``
- start ``main.py``


# How to use the Server
It is suggested to start the server via terminal ``python main.py`` to reduce input delay and windows related issues. 

On startup, a set of empty plots should be displayed.
Please checkout [Controlling Plot Animation](#controlling-plot-animation) for available hotkeys.

The server will be listening on the host machines network ip address under port 5500.

For configuring the M5 Stick with the correct local network, host ip and port, please checkout this repository containing the client application: [BTD-framework](https://github.com/01604987/BTD-framework)

Upon successful connection, the following functionalities can be applied:
``The application can also be easily tested without a glove. Index finger = middle button. Middle finger = right side button. Further details in the client application repository``
- Keyboard ``left``/``right``: abrupt left / right swipe of the hand without any buttons
- Mouse ``lmb click``: short tap of index and thumb
- Mouse ``lmb double click``: short double tap of index and thumb
- Mouse ``cursor control``: holding index and thumb with pitch and roll of hand in horizontal position
- Mouse ``drag & drop with cursor``: double tap and hold index and thumb with pitch and roll of hand in horizontal position
- Mouse ``rmb click``: short tap of middle finger and thumb
- Keyboard ``l + ctrl``: double tap of middle finger and thumb for entering/exiting presentation mode for pdf slides
- Hostmachine ``volume control``: hold middle finger and thumb with rotating wrist left/right 
- Mouse/Keyboard ``ctrl + scroll wheel``: double tap and hold middle finger and thumb with rotating wrist up/down

``note: All functionalities are only guaranteed on windows machines running Windows 10/11. On Apple Macs, volume control is not implemented.``

The server can be shutdown with ``ctrl + c`` or closing the terminal. 


# Controlling Plot Animation
- Pause entire plot animation: ``p``
- Pause raw acceleration graph: ``a``
- Pause raw gyro graph: ``g``
- Pause orientation graph: ``o``
- Pause linear acceleration graph: ``l``
- Pause velocity graph: ``v``