from RPi import GPIO
import time
from flask_cors import CORS
from flask_cors.core import CONFIG_OPTIONS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify, request
from datetime import datetime, date
import threading

from repositories.DataRepository import DataRepository

from helpers.klasseSunlight import Sunlight
from helpers.klasseTempHumi import TempHumi
from helpers.klasseMCP import SPI
from helpers.klasseOLED import OLED
from helpers.klasseSpeaker import Speaker
from helpers.klasseLCD import LCD
from subprocess import check_output


# Code voor Hardware
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#sensors
sunlight = Sunlight()
temphumi = TempHumi()
spi = SPI()

# oled displays
eyes = OLED(1)
mouthL = OLED(3)
mouthR = OLED(4)
face_current_state = 'start'

# speakers
speakers = Speaker()
speaker_current_state = False

# lcd with ip address
lcd = LCD(0x27)
ips = check_output(['hostname', '--all-ip-addresses']).split()
lan = ips[0].decode()
wlan = ips[1].decode()
lcd.lcd_string(f'{lan}', lcd.LCD_LINE_1)
lcd.lcd_string(f'{wlan}', lcd.LCD_LINE_2)




# Code voor Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False, engineio_logger=False, ping_timeout=1)
CORS(app)


# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket.
def read_values():
    while True:
        moist = spi.read_moist()
        air = spi.read_air()
        if moist is not 0 and air is not 0:
            print('*** Read all values **')
            VIS, UV, IR = sunlight.read_values()
            humi, temp = temphumi.read_values()
            temp -= 3   # temperatuur overdijft een beetje want heeft maar een accuraatheid van 2graden en rond af naar boven
            print(moist, VIS, UV, IR, temp, humi, air)

            # try:
            #     DataRepository.create_log_moist(datetime.now(), moist)
            #     DataRepository.create_log_VIS(datetime.now(), VIS)
            #     DataRepository.create_log_UV(datetime.now(), UV)
            #     DataRepository.create_log_IR(datetime.now(), IR)
            #     DataRepository.create_log_temp(datetime.now(), temp)
            #     DataRepository.create_log_humi(datetime.now(), humi)
            #     DataRepository.create_log_air(datetime.now(), air)                
            # except:
            #     print('Not able to add value to database')

            socketio.emit('B2F_send_data', {'Moisture': moist, 'VIS': VIS, 'UV': UV, 'IR': IR, 'Temperature': temp, 'Humidity': humi, 'Air': air})


thread = threading.Timer(0, read_values)
thread.start()


# Custom endpoint
endpoint = '/api/v1'

# API ENDPOINTS
@app.route('/')
def info():
    return jsonify(info='Please go to the endpoint ' + endpoint)

@app.route(endpoint + '/history', methods=['GET'])
def get_history():
    if request.method == 'GET':
        return jsonify(data=DataRepository.read_history()), 200

@app.route(endpoint + '/actions', methods=['GET'])
def get_actions():
    if request.method == 'GET':
        return jsonify(data=DataRepository.read_actions()), 200

@app.route(endpoint + '/devices', methods=['GET'])
def get_devices():
    if request.method == 'GET':
        return jsonify(data=DataRepository.read_devices()), 200


# SOCKETIO
@socketio.on_error()        
def error_handler(e):
    print(e)

@socketio.on('connect')
def initial_connection():
    print('A new client connect')

@socketio.on('F2B_sendFace')
def showFace(jsonObject):
    global face_current_state
    global speaker_current_state
    value = jsonObject['statusFace']
    speaker_current_state = jsonObject['statusSpeaker']
    print(jsonObject)

    if speaker_current_state == True:
        speakers.playTone()
    else:
        speakers.quiet()

    if value != face_current_state:
        face_current_state = value
        eyes.backlight(True)
        mouthL.backlight(True)
        mouthR.backlight(True)
        # thirsty, sick, cold, hot, sad or normal
        if value=='thirsty':
            print('thirsty')
            for i in range(0, 16):
                eyes.setCursor(i, 0)
                mouthL.setCursor(i, 0)
                mouthR.setCursor(i, 0)
                eyes.write(OLED.openEye[i])
                mouthL.write(OLED.wideOpenLeft[i])        
                mouthR.write(OLED.wideOpenRight[i])

        if value=='sick':
            print('sick')
            for i in range(0, 16):
                eyes.setCursor(i, 0)
                mouthL.setCursor(i, 0)
                mouthR.setCursor(i, 0)
                eyes.write(OLED.halfOpenEye[i])
                mouthL.write(OLED.openLeft[i])        
                mouthR.write(OLED.openRight[i])

        if value=='cold':
            print('cold')
            for i in range(0, 16):
                eyes.setCursor(i, 0)
                mouthL.setCursor(i, 0)
                mouthR.setCursor(i, 0)
                eyes.write(OLED.openEye[i])
                mouthL.write(OLED.sadLeft[i])        
                mouthR.write(OLED.sadRight[i])

        if value=='hot':
            print('hot')
            for i in range(0, 16):
                eyes.setCursor(i, 0)
                mouthL.setCursor(i, 0)
                mouthR.setCursor(i, 0)
                eyes.write(OLED.downEye[i])
                mouthL.write(OLED.openLeft[i])        
                mouthR.write(OLED.openRight[i])

        if value=='sad':
            print('sad')
            for i in range(0, 16):
                eyes.setCursor(i, 0)
                mouthL.setCursor(i, 0)
                mouthR.setCursor(i, 0)
                eyes.write(OLED.downEye[i])
                mouthL.write(OLED.sadLeft[i])        
                mouthR.write(OLED.sadRight[i])
        
        if value=='normal':
            print('normal')
            for i in range(0, 16):
                eyes.setCursor(i, 0)
                mouthL.setCursor(i, 0)
                mouthR.setCursor(i, 0)
                eyes.write(OLED.openEye[i])
                mouthL.write(OLED.happyLeft[i])        
                mouthR.write(OLED.happyRight[i])
        
        if value=='OFF':
            print('OFF')
            eyes.clear()
            mouthL.clear()
            mouthR.clear()
            eyes.backlight(False)
            mouthL.backlight(False)
            mouthR.backlight(False)   


if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
