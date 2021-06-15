from RPi import GPIO
import time
import os
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

# sensors
sunlight = Sunlight()
temphumi = TempHumi()
spi = SPI()

# oled displays
eyes = OLED(1)
mouthL = OLED(3)
mouthR = OLED(4)
face_state = True
face_current_state = 'normal'
face_previous_state = 'nothing'

# speakers
speakers = Speaker()
speaker_state = False

# lcd with ip address
lcd = LCD(0x27)
ips = check_output(['hostname', '-I']).split()
if len(ips) > 1 and ips[0].decode() == '192.168.168.168':
    lan = ips[0].decode()
    wlan = ips[1].decode()
    lcd.lcd_string(f'{lan}', lcd.LCD_LINE_1)
    lcd.lcd_string(f'{wlan}', lcd.LCD_LINE_2)
elif len(ips) == 1 and ips[0].decode() == '192.168.168.168':
    message = 'Fallback IP'
    lan = ips[0].decode()
    lcd.lcd_string(f'{message}', lcd.LCD_LINE_1)
    lcd.lcd_string(f'{lan}', lcd.LCD_LINE_2)
else:
    message = 'Site IP address'
    wlan = ips[0].decode()
    lcd.lcd_string(f'{message}', lcd.LCD_LINE_1)
    lcd.lcd_string(f'{wlan}', lcd.LCD_LINE_2)


# Code voor Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*",
                    logger=False, engineio_logger=False, ping_timeout=1)
CORS(app)


# START een thread op. Belangrijk!!! Debugging moet UIT staan op start van de server, anders start de thread dubbel op
# werk enkel met de packages gevent en gevent-websocket.
def read_values():
    while True:
        moist = spi.read_moist()
        if moist is not -1:
            print('*** Read all values **')
            VIS, UV, IR = sunlight.read_values()
            humi, temp = temphumi.read_values()
            temp -= 3   # temperatuur overdijft een beetje want heeft maar een accuraatheid van 2graden en rond af naar boven
            air = spi.read_air()
            print(moist, IR, temp, humi, air)

            DataRepository.create_log_moist(datetime.now(), moist)
            DataRepository.create_log_VIS(datetime.now(), VIS)
            DataRepository.create_log_UV(datetime.now(), UV)
            DataRepository.create_log_IR(datetime.now(), IR)
            DataRepository.create_log_temp(datetime.now(), temp)
            DataRepository.create_log_humi(datetime.now(), humi)
            DataRepository.create_log_air(datetime.now(), air)

            socketio.emit('B2F_send_data', {
                          'Moisture': moist, 'IR': IR, 'Temperature': temp, 'Humidity': humi, 'Air': air})
            getFace(moist, IR, temp, humi, air)

thread = threading.Timer(0, read_values)
thread.start()


def getFace(moist, IR, temp, humi, air):
    global face_current_state
    if moist < 30 or humi < 30:
        face_current_state = 'thirsty'
    elif moist > 70 or humi > 75:
        face_current_state = 'sick'
    elif IR < 200 or temp < 13:
        face_current_state = 'cold'
    elif IR > 5000 or temp > 30:
        face_current_state = 'hot'
    elif air > 21:
        face_current_state = 'sad'
    else:
        face_current_state = 'normal'
    showFace()


def showFace():
    global face_state
    global face_current_state
    global face_previous_state
    global speaker_state
    if face_state == True:
        # if the faces are turned on
        if face_current_state != face_previous_state:
            socketio.emit('B2F_send_face', {'face': face_current_state})
            # show the right face
            face_previous_state = face_current_state
            eyes.backlight(True)
            mouthL.backlight(True)
            mouthR.backlight(True)
            # thirsty, sick, cold, hot, sad, normal or off
            if face_current_state == 'thirsty':
                print('thirsty')
                for i in range(0, 16):
                    eyes.setCursor(i, 0)
                    mouthL.setCursor(i, 0)
                    mouthR.setCursor(i, 0)
                    eyes.write(OLED.openEye[i])
                    mouthL.write(OLED.wideOpenLeft[i])
                    mouthR.write(OLED.wideOpenRight[i])
                DataRepository.create_log_actuator(
                    datetime.now(), 'Eye open', 'EYEL')
                DataRepository.create_log_actuator(
                    datetime.now(), 'Eye open', 'EYER')
                DataRepository.create_log_actuator(
                    datetime.now(), 'Mouth wide open left', 'MOUTHL')
                DataRepository.create_log_actuator(
                    datetime.now(), 'Mouth wide open right', 'MOUTHR')

            if face_current_state == 'sick':
                print('sick')
                for i in range(0, 16):
                    eyes.setCursor(i, 0)
                    mouthL.setCursor(i, 0)
                    mouthR.setCursor(i, 0)
                    eyes.write(OLED.halfOpenEye[i])
                    mouthL.write(OLED.openLeft[i])
                    mouthR.write(OLED.openRight[i])
                DataRepository.create_log_actuator(
                    datetime.now(), 'Eye half open', 'EYEL')
                DataRepository.create_log_actuator(
                    datetime.now(), 'Eye half open', 'EYER')
                DataRepository.create_log_actuator(
                    datetime.now(), 'Mouth open left', 'MOUTHL')
                DataRepository.create_log_actuator(
                    datetime.now(), 'Mouth open right', 'MOUTHR')

            if face_current_state == 'cold':
                print('cold')
                for i in range(0, 16):
                    eyes.setCursor(i, 0)
                    mouthL.setCursor(i, 0)
                    mouthR.setCursor(i, 0)
                    eyes.write(OLED.openEye[i])
                    mouthL.write(OLED.sadLeft[i])
                    mouthR.write(OLED.sadRight[i])
                DataRepository.create_log_actuator(
                    datetime.now(), 'Eye open', 'EYEL')
                DataRepository.create_log_actuator(
                    datetime.now(), 'Eye open', 'EYER')
                DataRepository.create_log_actuator(
                    datetime.now(), 'Mouth sad left', 'MOUTHL')
                DataRepository.create_log_actuator(
                    datetime.now(), 'Mouth sad right', 'MOUTHR')

            if face_current_state == 'hot':
                print('hot')
                for i in range(0, 16):
                    eyes.setCursor(i, 0)
                    mouthL.setCursor(i, 0)
                    mouthR.setCursor(i, 0)
                    eyes.write(OLED.downEye[i])
                    mouthL.write(OLED.openLeft[i])
                    mouthR.write(OLED.openRight[i])
                DataRepository.create_log_actuator(
                    datetime.now(), 'Eye down', 'EYEL')
                DataRepository.create_log_actuator(
                    datetime.now(), 'Eye down', 'EYER')
                DataRepository.create_log_actuator(
                    datetime.now(), 'Mouth open left', 'MOUTHL')
                DataRepository.create_log_actuator(
                    datetime.now(), 'Mouth open right', 'MOUTHR')

            if face_current_state == 'sad':
                print('sad')
                for i in range(0, 16):
                    eyes.setCursor(i, 0)
                    mouthL.setCursor(i, 0)
                    mouthR.setCursor(i, 0)
                    eyes.write(OLED.downEye[i])
                    mouthL.write(OLED.sadLeft[i])
                    mouthR.write(OLED.sadRight[i])
                DataRepository.create_log_actuator(
                    datetime.now(), 'Eye down', 'EYEL')
                DataRepository.create_log_actuator(
                    datetime.now(), 'Eye down', 'EYER')
                DataRepository.create_log_actuator(
                    datetime.now(), 'Mouth sad left', 'MOUTHL')
                DataRepository.create_log_actuator(
                    datetime.now(), 'Mouth sad right', 'MOUTHR')

            if face_current_state == 'normal':
                print('normal')
                for i in range(0, 16):
                    eyes.setCursor(i, 0)
                    mouthL.setCursor(i, 0)
                    mouthR.setCursor(i, 0)
                    eyes.write(OLED.openEye[i])
                    mouthL.write(OLED.happyLeft[i])
                    mouthR.write(OLED.happyRight[i])
                DataRepository.create_log_actuator(
                    datetime.now(), 'Eye open', 'EYEL')
                DataRepository.create_log_actuator(
                    datetime.now(), 'Eye open', 'EYER')
                DataRepository.create_log_actuator(
                    datetime.now(), 'Mouth happy left', 'MOUTHL')
                DataRepository.create_log_actuator(
                    datetime.now(), 'Mouth happy right', 'MOUTHR')
        if speaker_state == True and face_current_state != 'normal':
            # if the speakers are on and the face is not normal play a tone
            speakers.playAlarm()
    else:
        # if the faces are turned off
        face_previous_state = 'off'
        print('off')
        eyes.backlight(False)
        mouthL.backlight(False)
        mouthR.backlight(False)
        DataRepository.create_log_actuator(datetime.now(), 'OFF', 'EYEL')
        DataRepository.create_log_actuator(datetime.now(), 'OFF', 'EYER')
        DataRepository.create_log_actuator(datetime.now(), 'OFF', 'MOUTHL')
        DataRepository.create_log_actuator(datetime.now(), 'OFF', 'MOUTHR')


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
    socketio.emit('B2F_send_states', {
                  'FaceState': face_state, 'SpeakerState': speaker_state})
    socketio.emit('B2F_send_face', {'face': face_current_state})


@socketio.on('F2B_toggle_face')
def toggle_face():
    global face_state
    face_state = not face_state
    print(f'face is now {face_state}')
    showFace()


@socketio.on('F2B_toggle_speakers')
def toggle_speakers():
    global speaker_state
    speaker_state = not speaker_state
    print(f'speakers are now {speaker_state}')
    DataRepository.create_log_actuator(
        datetime.now(), f'Speakers are {speaker_state}', 'SPEAKER')
    showFace()


@socketio.on('F2B_shutdown')
def shutdown():
    lcd.clear()
    spi.close_spi()
    eyes.backlight(False)
    mouthL.backlight(False)
    mouthR.backlight(False)
    speakers.quiet()
    print("Shutting Down")
    os.system("sudo shutdown -h now")


if __name__ == '__main__':
    socketio.run(app, debug=False, host='0.0.0.0')
