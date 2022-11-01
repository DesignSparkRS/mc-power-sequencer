import time
from machine import Pin
import random

heaterPins = [4, 5, 6, 7, 8, 9, 10, 11, 12]
fanPins = [13, 14, 15, 16, 17, 18, 19, 20, 21]
heaterPinObjects = []
fanPinObjects = []
timerPin = 28
redLed = 0
greenLed = 1
blueLed = 2
buttonInput = 3

redLedPin = Pin(redLed, Pin.OUT, value=0)
greenLedPin = Pin(greenLed, Pin.OUT, value=0)
blueLedPin = Pin(blueLed, Pin.OUT, value=0)
buttonPin = Pin(buttonInput, Pin.IN)

for heaterPin in heaterPins:
    heaterPinObjects.append(Pin(heaterPin, Pin.OUT, value=0))

for fanPin in fanPins:
    fanPinObjects.append(Pin(fanPin, Pin.OUT, value=0))
    
timerPinObject = Pin(timerPin, Pin.OUT, value=0)

currentStatus = 0 # 0: idle, 1: heating, 2: cooling

heaterTimeout = 60 # seconds
fanTimeout = 120

heaterStatuses = {
    "1":{
        "heater": heaterPinObjects[0],
        "heating": False,
        "fan": fanPinObjects[0],
        "cooling": False,
        "heaterOnTime": 0,
        "fanOnTime": 0
        },
    "2":{
        "heater": heaterPinObjects[1],
        "heating": False,
        "fan": fanPinObjects[1],
        "cooling": False,
        "heaterOnTime": 0,
        "fanOnTime": 0
        },
    "3":{
        "heater": heaterPinObjects[2],
        "heating": False,
        "fan": fanPinObjects[2],
        "cooling": False,
        "heaterOnTime": 0,
        "fanOnTime": 0
        },
    "4":{
        "heater": heaterPinObjects[3],
        "heating": False,
        "fan": fanPinObjects[3],
        "cooling": False,
        "heaterOnTime": 0,
        "fanOnTime": 0
        },
    "5":{
        "heater": heaterPinObjects[4],
        "heating": False,
        "fan": fanPinObjects[4],
        "cooling": False,
        "heaterOnTime": 0,
        "fanOnTime": 0
        },
    "6":{
        "heater": heaterPinObjects[5],
        "heating": False,
        "fan": fanPinObjects[5],
        "cooling": False,
        "heaterOnTime": 0,
        "fanOnTime": 0
        },
    "7":{
        "heater": heaterPinObjects[6],
        "heating": False,
        "fan": fanPinObjects[6],
        "cooling": False,
        "heaterOnTime": 0,
        "fanOnTime": 0
        },
    "8":{
        "heater": heaterPinObjects[7],
        "heating": False,
        "fan": fanPinObjects[7],
        "cooling": False,
        "heaterOnTime": 0,
        "fanOnTime": 0
        },
    "9":{
        "heater": heaterPinObjects[8],
        "heating": False,
        "fan": fanPinObjects[8],
        "cooling": False,
        "heaterOnTime": 0,
        "fanOnTime": 0
        }
    }

def triggerTimer():
    timerPinObject.value(1)
    time.sleep(0.25)
    timerPinObject.value(0)

def updateButtonLed():
    if currentStatus == 0:
        redLedPin.value(0)
        greenLedPin.value(1)
        blueLedPin.value(0)

    if currentStatus == 1:
        redLedPin.value(1)
        greenLedPin.value(0)
        blueLedPin.value(0)

    if currentStatus == 2:
        redLedPin.value(0)
        greenLedPin.value(0)
        blueLedPin.value(1)

while True:
    if buttonPin.value() == 1 and currentStatus == 0:
        time.sleep(0.07)
        if buttonPin.value() == 0:
            # Turn on a heater
            heaterNum = str(random.randint(1, 9))
        
            # Check heater and fan isn't in use
            if heaterStatuses[heaterNum]["heating"] == False and heaterStatuses[heaterNum]["cooling"] == False:
                print("Turning on heater {}".format(heaterNum))
                greenLedPin.value(0)
                triggerTimer()
                redLedPin.value(1)

                heaterStatuses[heaterNum]["heater"].value(1)
                heaterStatuses[heaterNum]["heating"] = True
                heaterStatuses[heaterNum]["heaterOnTime"] = time.time()
                currentStatus = 1
            else:
                print("Heater miss, recently used")

    # Check for expired heaters
    for heaterKey, heaterItem in heaterStatuses.items():
        if heaterItem["heating"] and time.time() > heaterItem["heaterOnTime"] + heaterTimeout:
            # Turn off heater
            print("Turning off heater {}".format(heaterKey))
            heaterItem["heater"].value(0)
            heaterItem["heating"] = False

            # Move to cooling
            print("Turning on fan for heater {}".format(heaterKey))
            heaterItem["fan"].value(1)
            heaterItem["cooling"] = True
            heaterItem["fanOnTime"] = time.time()

            currentStatus = 2

    # Check for expired fans
    for heaterKey, heaterItem in heaterStatuses.items():
        if heaterItem["cooling"] and time.time() > heaterItem["fanOnTime"] + fanTimeout:
            # Turn off fan
            print("Turning off fan for heater {}".format(heaterKey))
            heaterItem["fan"].value(0)
            heaterItem["cooling"] = False

            currentStatus = 0

    updateButtonLed()
    time.sleep(0.01)