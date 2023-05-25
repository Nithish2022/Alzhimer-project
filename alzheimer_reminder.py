import time
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set the rate of the voice message
engine.setProperty("rate", 100)

# Speak a voice message to remind the user to enter the reminders
engine.say("Please enter your reminders for the day.")
engine.runAndWait()

# Ask the user for the reminder messages and times
reminders = {}
while True:
    message = input("Enter a reminder message (or 'done' to finish): ")
    if message == "done":
        break
    time_str = input("Enter the time for this reminder (in format HH:MM): ")
    reminders[time_str] = message

# Set up the reminders based on user input
print("Setting up reminders:")
for time_str, message in reminders.items():
    print(f"- {time_str}: {message}")

# Speak a voice message to remind the user about the upcoming reminders
engine.say("Reminders have been set up")
#for time_str, message in reminders.items():
    #engine.say(f"At {time_str}, {message}")
#engine.runAndWait()

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
