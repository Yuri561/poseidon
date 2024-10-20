import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
index = 0
for voice in voices:
    print(f'Voice {index}: {voice.name}')
    print(f' - ID: {voice.id}')
    print(f' - Gender: {voice.gender}')
    print(f' - Age: {voice.age}')
    print('--------------------')
    index += 1
engine.runAndWait()