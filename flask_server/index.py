from flask import Flask, request
import RPi.GPIO as GPIO
import time
import myDHT22

# GPIO Settings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set PIN 18 as output 
GPIO.setup(18, GPIO.OUT)


app = Flask(__name__)

# Sample test to see if I could the LED to light up
##@app.route("/<action>")
##def on(action):
##        if action == "on":
##                GPIO.output(18, GPIO.HIGH)
##                return "LED IS ON!"
##
##@app.route("/off")
##def off():
##        GPIO.output(18, GPIO.LOW)
##        return "LED is OFF!"

@app.route("/test", methods=['GET'])
def test():
	data = "{'status': 'It works'}"
       	return data

#######################################################

# Get the current humidity
@app.route("/humidity_sensor", methods=['GET'])
def getHumiditySensor():
        
	
	# Get the humidity sensor reading
        reading = myDHT22.getHumidity()
	print(reading['humidity'])
	time = reading['datetime']
        current_humidity = reading['humidity']
        current_temp = reading['temp']
	print(reading)

        data = {
                'status' : '',
                'time' : '',
                'current_humidity' : '',
                'current_temp' : '',
        }

        if(reading):
                data['status'] = 'success'
                data['time'] = time
                data['current_humidity'] = current_humidity
                data['current_temp'] = current_temp
		print("Data:", str(data)) 
                return str(data)


        data['current_humidity'] = "null"
        data['current_temp'] = "null"
        data['status'] = "fail"
        data['time'] = time
        data['error'] = "Unable to read from sensor"
        
        return str(data)

        

@app.route("/change_humidity_setting/<setting>", methods=['GET', 'POST'])
def setCurrentHumidity(setting):

        print ("Change humidity settings....")
        # Set new value
	value = setting
	print("value", value)

        current_humidity_setting = ''
        
        try:
                myFile = open('settings', 'w')
                myFile.truncate()

                myFile.write(value)
                myFile.close()

                current_humidity_setting = value

                data = { 
			'status' : 'success',
			'current_humidity_setting' : str(current_humidity_setting)
		}
                return str(data)
                
        except Exception:
                data = {
                        'status' : 'failure',
                        'message' : 'Could not write to file'
                }
        return str(data)
                


# Get the current humidity setting
@app.route("/humidity_setting", methods=['GET'])
def getCurrentHumiditySetting():

        print ("Get Humidity Setting....")
        # Get the current humidity setting
        try:
                myFile = open('settings', 'r')
                print ("Get Humidity Setting....2")
                #value = myFile.readLine()#Aakash, it's not readLine, but readline
                value = myFile.readline()
                print ("Get Humidity Setting....3")
                myFile.close()

                current_humidity_setting = value

                data = {
                        'status' : 'success',
                        'current_humidity_setting' : current_humidity_setting,
                }
                return str(data)
                
        except Exception:
                return "{'status' : 'failure','message' : 'Could not read from file'})"

# User updated on/off
@app.route("/user_state/<state>", methods=['GET'])
def setUserState(state):

        # Set new value
	value = state

        try:
                myFile = open('user_state', 'w')
                myFile.truncate()

                myFile.write(value)
                myFile.close()

                current_user_state = value

                data = { 
			'status' : 'success',
			'current_user_state' : str(current_user_state)
		}
                return str(data)
                
        except Exception:
                return "{'status' : 'failure','message' : 'Could not write user_state from file'})"


 
# Get current state of humidifier
@app.route("/state", methods=['GET'])
def getCurrentState():


        data = {
                'status' : '',
                'humidifier_state' : '',
        }
        
        # Get the status, on or off
        try:
                myFile = open('state', 'r')
                state = myFile.readline()
                myFile.close()

                data['status'] = 'success'
                data['humidifier_state'] = state
                return str(data)
                
        except Exception:
                return "{'status' : 'failure','message' : 'Could not read humidifier state from file'})"
        


if __name__ == "__main__":
	#app.run(processes=3)
        app.run(host='0.0.0.0', processes=3)
        print("Succesfully launched!")
