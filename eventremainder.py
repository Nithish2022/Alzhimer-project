import time
import pyttsx3
import speech_recognition as sr

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set the rate of the voice message
engine.setProperty("rate", 150)

# Initialize speech recognition engine
recognizer = sr.Recognizer()

# Speak a voice message to remind the user to enter the reminders
engine.say("Please enter your reminders for the day.")
engine.runAndWait()

# Ask the user for the reminder messages and times
reminders = {}
while True:
    # Speak a voice message to prompt the user to speak
    engine.say("Please speak your reminder message.")
    engine.runAndWait()

    # Get the user's speech input
    with sr.Microphone() as source:
        audio = recognizer.listen(source)

    # Convert the user's speech to text
    message = recognizer.recognize_google(audio)

    # Check if the user wants to finish entering reminders
    if message == "done":
        break

    # Speak a voice message to prompt the user to speak
    engine.say("Please speak the time for this reminder.")
    engine.runAndWait()

    # Get the user's speech input
    with sr.Microphone() as source:
        audio = recognizer.listen(source)

    # Convert the user's speech to text
    time_str = recognizer.recognize_google(audio)

    reminders[time_str] = message

# Set up the reminders based on user input
print("Setting up reminders:")
for time_str, message in reminders.items():
    print(f"- {time_str}: {message}")

# Speak a voice message to remind the user about the upcoming reminders
engine.say("Reminders have been set up. You will be reminded of the following tasks:")
for time_str, message in reminders.items():
    engine.say(f"At {time_str}, {message}")
engine.runAndWait()

while True:
    # Get the current time
    current_time = time.strftime("%H:%M")

    # Check if the current time matches any of the reminder times
    if current_time in reminders.keys():
        # Speak the reminder message
        engine.say(reminders[current_time])
        engine.runAndWait()

    # Wait for 1 minute before checking the time again
    time.sleep(60)
