from machine import ADC, Pin
import utime

universalInputVoltageADC = ADC(Pin(28)) #should be coupled with 100nF or 1uF on the ADC input to ground.
voltageChangePin = Pin(19,Pin.IN)
inputVoltageDriverPin = Pin(17,Pin.IN)
desiredVoltage =0; #value of the desired voltage
unregulatedVoltage =0;
def getDesiredVoltage(): #calculates desired voltage based on signal received from the host
    inputVoltageDriverPin.value(1)
    dv_reading = universalInputVoltageADC.read_u16() #the reading after the adc
    print("dv_reading: " + str(dv_reading))
    if dv_reading >= 8276:
        desiredVoltage = 18* dv_reading/57594;#further calculations needed
        print("desired voltage: " + str(desiredVoltage))
    else: print("can't provide voltage less than 2.5v")
def getUnregulatedVoltage():
    inputVoltageDriverPin.value(1)
    unregulatedVoltage = universalInputVoltageADC.read_u16() #further calculations to be done


universalMeasuringPinADC = ADC(Pin(26))
measuringDriverPin = Pin(18,Pin.OUT)
outputVoltage = 0;
measuredCurrent = 0;
def getOutputVoltage():
    measuringDriverPin.value(1)
    outputVoltage = universalMeasuringPinADC.read_u16(); #further calculation will be done
def getAverageCurrent():
    measuringDriverPin.value(0)
    measuredCurrent = universalMeasuringPinADC.read_u16(); #further calculation will be done

shortCircuitADC = ADC(Pin(27))
def checkForShortCircuit():
    if shortCircuitADC.read_u16() > 6500:
        #indicate short circuit


getterPin = Pin(22, Pin.IN)
outputVoltagePin = Pin(21, Pin.OUT)
enderPin = Pin(20, Pin.OUT)
def sendOutputVoltage():
    print("output voltage stream start")
    index = 0;
    #algorithm to make output voltage in binary
    outputVoltageDigital = list(map(int, bin(int(outputVoltage))[2:]))
    while index<len(outputVoltageDigital):
            outputVoltagePin.value(outputVoltageDigital[index])
            print(outputVoltagePin.value())
            index = index +1;
            utime.sleep(0.05)       
    enderPin.value(1)
    print("output voltage stream end")
    utime.sleep(0.1)
    enderPin.value(0)#sends the output voltage to the host

while True:
    if voltageChangePin.value()==1:
        getDesiredVoltage()
    if getterPin.value() == 1:
        sendOutputVoltage()
    #print(enderPin.value())
    utime.sleep(0.05)



