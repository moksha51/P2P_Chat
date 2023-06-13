import socket
import pyaudio
import threading
import wave
import datetime
import os
import pygame
import whisper

##########################################################################
# PyAudio Configurations #
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

pyAudio = pyaudio.PyAudio()

stream = pyAudio.open(format=FORMAT,
                      channels=CHANNELS,
                      rate=RATE,
                      input=True,
                      frames_per_buffer=CHUNK)

# if isPlaying = True, means some audio file somewhere is playing.
isPlaying = False
frames = []
###########################################################################
#
#
#
##########################################################################
# Socket Configuration #
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostIp = "127.0.0.1"
portNumber = 7500
server_address = (hostIp, portNumber)
try:
    sock.connect(server_address)
    print(f'Connected to server: {server_address[0]}:{server_address[1]}')
except socket.error as e:
    print(f"Socket error: {e}")
    exit(1)
#############################################################################
#
#
#
#############################################################################
# Various folder paths
ReceivedVoiceRecordings = '/'
CannedRecordings = '/'

def playSiren():
    global isPlaying
    # Initialize Pygame
    pygame.init()

    # Load the media file
    media_file = r"CannedRecordings/siren.wav"
    pygame.mixer.music.load(media_file)

    # Play the media file
    pygame.mixer.music.play()
    isPlaying = True

    # Wait for the media file to finish playing
    while pygame.mixer.music.get_busy():
        continue

    # Clean up resources
    pygame.quit()
    isPlaying = False


def playCannedMessage():
    global isPlaying
    # Initialize Pygame
    pygame.init()

    # Load the media file
    media_file = r"CannedRecordings/3xShipBlast.mp3"
    pygame.mixer.music.load(media_file)

    # Play the media file
    pygame.mixer.music.play()
    isPlaying = True

    # Wait for the media file to finish playing
    while pygame.mixer.music.get_busy():
        continue

    # Clean up resources
    pygame.quit()
    isPlaying = False


def transcribe():
    folder_path = "/Users/xingjietan/PycharmProjects/indian_guy_chat/ReceivedVoiceRecordings"

    # Get the list of files in the folder
    files = os.listdir(folder_path)

    # Sort the files based on their creation time
    sorted_files = sorted(files, key=lambda x: os.path.getctime(os.path.join(folder_path, x)), reverse=True)

    # Get the path of the latest file
    if sorted_files:
        latest_file_path = os.path.join(folder_path, sorted_files[0])
        print("Latest file:", latest_file_path)
        model = whisper.load_model("base")
        result = model.transcribe(latest_file_path)
        resultText = result["text"]
        return resultText
    else:
        print("No files found in the folder.")

    print('test transcribing')


def sendVoice():
    global sock, frames
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    while True:
        try:
            data = stream.read(CHUNK)
            sock.sendall(data)
            frames.append(data)
        except socket.error as e:
            print(f"Socket error: {e}")
            break

    stream.stop_stream()
    stream.close()
    audio.terminate()

    sock.close()

def recordVoice():
    global frames
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    while True:
        if len(frames) > 0:
            break

    while True:
        if len(frames) > 0:
            data = stream.read(CHUNK)
            frames.append(data)
        else:
            break

    stream.stop_stream()
    stream.close()
    audio.terminate()
    saveVoiceRecording()

def saveVoiceRecording():
    global frames
    if frames:
        timestamp = datetime.datetime.now().strftime("%H%M%S_%d%b%Y")
        filename = f"recording_{timestamp}.wav"
        directory = "ReceivedVoiceRecordings"

        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, filename)

        wf = wave.open(file_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        sendVoice()

def stopAllAudio():
    global isPlaying
    # Stop the media file
    pygame.mixer.music.stop()
    isPlaying = False


# def handle_input(sock):
#     while True:
#         try:
#             command = input("Enter command (p to start audio, o to stop audio, q to quit): ")
#             if command == "p":
#                 push_to_talk_event.set()  # Start transmitting audio
#                 print("Push to talk")
#                 frames.clear()  # Clear frames for new recording
#                 recording_thread = threading.Thread(target=record_audio, args=(frames,))
#                 recording_thread.start()
#             elif command == "o":
#                 push_to_talk_event.clear()  # Stop transmitting audio
#                 print("Audio transmission stopped")
#                 recording_thread.join()  # Wait for recording to complete
#                 save_audio(frames)
#             elif command == "q":
#                 push_to_talk_event.clear()  # Stop audio transmission
#                 break
#         except Exception as e:
#             print(f"Error: {e}")
#             break
#

#

#
# push_to_talk_event = threading.Event()
# push_to_talk_event.clear()  # Initially not transmitting audio
# frames = []
#
# send_thread = threading.Thread(target=audio_sender, args=(sock, frames))
# send_thread.start()
#
# handle_input(sock)
#
# push_to_talk_event.clear()  # Stop audio transmission
# sock.close()
#
# send_thread.join()
