from socket import *
from threading import *
from tkinter import Text, Entry, font, Tk, Label, Button, END
import Audio as audio
import User as user

frames = []

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

hostIp = "127.0.0.1"
portNumber = 7500

clientSocket.connect((hostIp, portNumber))

window = Tk()
window.title("ZyCraft | Base to LongRunner | , Connected To: [" + hostIp + "]:" + str(portNumber))

txtMessages = Text(window, width=100)
txtMessages.grid(row=0, column=0, padx=10, pady=10)

txtYourMessage = Entry(window, width=50)

txtYourMessage.grid(row=1, column=0, padx=10, pady=10)


#############################################################################
#
#
#
#############################################################################
# GUI RELATED #

# 1. handle_enter method so when user presses enter, sends text message instead of typing
def handle_enter(event):
    sendMessage()


txtYourMessage.bind("<Return>", handle_enter)


# 2. On button is pressed and hold, turns red
def on_button_press(event):
    event.widget.config(bg="red")


def on_button_release(event):
    event.widget.config(bg="SystemButtonFace")


# buttons = []
# button_names = ['btnSendMessage', 'btnSendVoiceMessage', 'btnSiren', 'btnCannedMessage', 'btnTranscribe','btnStopAudio']
# for i, text in enumerate(button_names):
#     button = Button(window, text=text, width=20, height=5)
#     button.grid(row=i, column=0)  # Use grid instead of pack
#     buttons.append(button)
#     button.bind("<ButtonPress-1>", on_button_press)
#     button.bind("<ButtonRelease-1>", on_button_release)


# 3. custom_font
custom_font = font.Font(family="Arial", size=12)

# Create a label with the custom font
label = Label(window, text="Hello, World!", font=custom_font)
label.pack()


def sendMessage():
    global hostIp
    clientMessage = txtYourMessage.get()
    txtMessages.insert(END, user.getUser(hostIp) + clientMessage + "\n")
    clientSocket.send(clientMessage.encode("utf-8"))
    txtYourMessage.delete(0, 'end')  # Clear the input box


btnSendMessage = Button(window, text="Send", width=10, command=sendMessage)
btnSendMessage.grid(row=2, column=0, padx=10, pady=10)
btnSendMessage.bind("<ButtonPress-1>", on_button_press)
btnSendMessage.bind("<ButtonRelease-1>", on_button_release)


def recvMessage():
    while True:
        serverMessage = clientSocket.recv(1024).decode("utf-8")
        print(serverMessage)
        txtMessages.insert(END, serverMessage + "\n")
        if serverMessage.endswith("siren.wav"):
            sendSiren()
        elif serverMessage.endswith("hello.wav"):
            sendCannedMessage()


recvThread = Thread(target=recvMessage)
recvThread.daemon = True
recvThread.start()


def sendVoiceMessage():
    clientMessage = audio.recordVoice()
    txtMessages.insert(END, "\n" + clientMessage)
    clientSocket.send(clientMessage.encode("utf-8"))


sendVoiceMessageThread = Thread(target=sendVoiceMessage)
sendVoiceMessageThread.daemon = True
sendVoiceMessageThread.start()

btnSendVoiceMessage = Button(window, text="Record", width=10, command=sendVoiceMessage)
btnSendVoiceMessage.grid(row=3, column=0, padx=10, pady=10)
btnSendVoiceMessage.bind("<ButtonPress-1>", on_button_press)
btnSendVoiceMessage.bind("<ButtonRelease-1>", on_button_release)


def sendSiren():
    audio.playSiren()


btnSiren = Button(window, text="Siren", width=10, command=sendSiren)
btnSiren.grid(row=4, column=0, padx=10, pady=10)
btnSiren.bind("<ButtonPress-1>", on_button_press)
btnSiren.bind("<ButtonRelease-1>", on_button_release)


def sendCannedMessage():
    return audio.playCannedMessage()


btnCannedMessage = Button(window, text="CannedMessage", width=10, command=sendCannedMessage)
btnCannedMessage.grid(row=5, column=0, padx=10, pady=10)
btnCannedMessage.bind("<ButtonPress-1>", on_button_press)
btnCannedMessage.bind("<ButtonRelease-1>", on_button_release)


def transcribeMessage():
    return audio.transcribe()


btnTranscribe = Button(window, text="Transcribe", width=10, command=transcribeMessage)
btnTranscribe.grid(row=6, column=0, padx=10, pady=10)
btnTranscribe.bind("<ButtonPress-1>", on_button_press)
btnTranscribe.bind("<ButtonRelease-1>", on_button_release)


def stopAudio():
    audio.stopAllAudio()


btnStopAudio = Button(window, text="Stop All Audio", width=10, command=transcribeMessage)
btnStopAudio.grid(row=7, column=0, padx=10, pady=10)
btnStopAudio.bind("<ButtonPress-1>", on_button_press)
btnStopAudio.bind("<ButtonRelease-1>", on_button_release)

window.mainloop()
