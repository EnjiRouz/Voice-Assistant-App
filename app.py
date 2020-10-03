"""
Проект голосового помощника (ассистента) на Python 3

Помощник умеет:
* воспроизводить случайное приветствие;
* воспроизводить случайное прощание с последующим завершением работы программы;
* производить поисковый запрос в поисковой системе Google
  (а также открывать список результатов и сами результаты данного запроса);
* производить поисковый запрос видео в системе YouTube и открывать список результатов данного запроса;
* выполнять поиск определения в Wikipedia c дальнейшим прочтением первых двух предложений;
* TODO........

Голосовой ассистент использует для синтеза речи встроенные в операционную систему Windows 10 возможности
(т.е. голоса зависят от операционной системы). Для этого используется библиотека pyttsx3

Для корректной работы системы распознавания речи в сочетании с библиотекой speech_recognition
используется библиотека PyAudio для получения звука с микрофона.

Для установки PyAudio можно найти и скачать нужный в зависимости от архитектуры файл здесь в папку с проектом:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

После чего его можно установить при помощи команды:
pip install PyAudio-0.2.11-cp37-cp37m-win_amd64.whl

Команды для установки прочих сторонних библиотек:
pip install google
pip install SpeechRecognition
pip install pyttsx3
pip install wikipedia-api

Дополнительную информацию по установке и использованию библиотек можно найти здесь:
https://pypi.org/
"""
import speech_recognition  # распознавание пользовательской речи (Speech-To-Text)
from termcolor import colored  # вывод цветных логов (для выделения распознанной речи)
from googlesearch import search  # поиск в Google
import pyttsx3  # синтез речи (Text-To-Speech)
import wikipediaapi  # поиск определений в Wikipedia
import random  # генератор случайных чисел
import webbrowser  # работа с использованием браузера по умолчанию (открывание вкладок с web-страницей)


# информация о владельце, включающие имя, город проживания
class OwnerPerson:
    name = ""
    home_city = ""

    def set_name(self, name):
        self.name = name

    def set_home_city(self, home_city):
        self.home_city = home_city


# настройки голосового ассистента, включающие имя, пол, язык речи
class VoiceAssistant:
    name = ""
    sex = ""
    speech_language = ""

    def set_name(self, name):
        self.name = name

    def set_sex(self, sex):
        self.sex = sex

    def set_speech_language(self, speech_language):
        self.speech_language = speech_language


# установка голоса по умолчанию (индекс может меняться в зависимости от настроек операционной системы)
def setup_assistant_voice():
    voices = ttsEngine.getProperty("voices")

    if assistant.speech_language == "en":
        if assistant.sex == "female":
            # Microsoft Zira Desktop - English (United States)
            ttsEngine.setProperty("voice", voices[1].id)
        else:
            # Microsoft David Desktop - English (United States)
            ttsEngine.setProperty("voice", voices[2].id)
    else:
        # Microsoft Irina Desktop - Russian
        ttsEngine.setProperty("voice", voices[0].id)


# запись и распознавание аудио
def record_and_recognize_audio(*args):
    with microphone:
        recognized_data = ""

        print("Listening...")
        audio = recognizer.listen(microphone, 5, 5)
        print("Started recognition...")

        try:
            recognized_data = recognizer.recognize_google(audio).lower()

        except speech_recognition.UnknownValueError:
            pass  # play_voice_assistant_speech("What did you say again?")

        except speech_recognition.RequestError:
            print("Sorry, speech service is unreachable at the moment")

        return recognized_data


# проигрывание речи ответов голосового ассистента
# аудио сохраняются в формате mp3
def play_voice_assistant_speech(text_to_speech):
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()


# проигрывание приветственной речи
def play_greetings(*args: tuple):
    greetings = [
        "hello, " + person.name + "! How can I help you today?",
        "Good day to you " + person.name + "! How can I help you today?"
    ]
    play_voice_assistant_speech(greetings[random.randint(0, len(greetings) - 1)])


# проигрывание прощательной речи и выход
def play_farewell_and_quit(*args: tuple):
    farewells = [
        "Goodbye, " + person.name + "! Have a nice day!",
        "See you soon, " + person.name + "!"
    ]
    play_voice_assistant_speech(farewells[random.randint(0, len(farewells) - 1)])
    ttsEngine.stop()
    quit()


# поиск в Google с автоматическим открытием ссылок (на список результатов и на сами результаты, если возможно)
def search_for_term_on_google(*args: tuple):
    if not args[0]: return
    search_term = " ".join(args[0])

    # открытие ссылки на поисковик в браузере
    url = "https://google.com/search?q=" + search_term
    webbrowser.get().open(url)

    # альтернативный поиск с автоматическим открытием ссылок на результаты (в некоторых случаях может быть небезопасно)
    search_results = []
    for _ in search(search_term,  # что искать
                    tld="com",  # верхнеуровневый домен
                    lang=assistant.speech_language,  # в данном случае используется язык, на котором говорит ассистент
                    num=1,  # количество результатов на странице
                    start=0,  # индекс первого извлекаемого результата
                    stop=1,  # индекс последнего извлекаемого результата (я хочу, чтобы открывался первый результат)
                    pause=1.0,  # задержка между HTTP-запросами
                    ):
        search_results.append(_)
        webbrowser.get().open(_)

    print(search_results)
    play_voice_assistant_speech("Here is what I found for" + search_term + "on google")


# поиск видео на YouTube с автоматическим открытием ссылки на список результатов
def search_for_video_on_youtube(*args: tuple):
    if not args[0]: return
    search_term = " ".join(args[0])
    url = "https://www.youtube.com/results?search_query=" + search_term
    webbrowser.get().open(url)
    play_voice_assistant_speech("Here is what I found for " + search_term + "on youtube")


# поиск в Wikipedia определения с озвучиванием результатов и открытием ссылок
def search_for_definition_on_wikipedia(*args: tuple):
    if not args[0]: return

    search_term = " ".join(args[0])

    # установка языка (в данном случае используется язык, на котором говорит ассистент)
    wiki = wikipediaapi.Wikipedia(assistant.speech_language)

    # поиск страницы по запросу, чтение summary, открытие ссылки на страницу для получения подробной информации
    wiki_page = wiki.page(search_term)
    if wiki_page.exists():
        play_voice_assistant_speech("Here is what I found for" + search_term + "on Wikipedia")
        webbrowser.get().open(wiki_page.fullurl)

        # чтение ассистентом первых двух предложений summary со страницы Wikipedia
        play_voice_assistant_speech(wiki_page.summary.split(".")[:2])
    else:
        # открытие ссылки на поисковик в браузере в случае, если на Wikipedia не удалось найти ничего по запросу
        play_voice_assistant_speech("Can't find" + search_term + "on Wikipedia. But here is what I found on google")
        url = "https://google.com/search?q=" + search_term
        webbrowser.get().open(url)


# выполнение команды с заданными пользователем кодом команды и аргументами
def execute_command_with_code(command_code: str, *args: list):
    for key in commands.keys():
        if command_code in key:
            commands[key](*args)
        else:
            pass  # print("Command code not found")


# перечень команд для использования (качестве ключей словаря используется hashable-тип tuple)
commands = {
    ("hello", "hi", "morning"): play_greetings,
    ("bye", "goodbye", "quit", "exit", "stop"): play_farewell_and_quit,
    ("search", "google", "find"): search_for_term_on_google,
    ("video", "youtube", "watch"): search_for_video_on_youtube,
    ("wikipedia", "definition", "about"): search_for_definition_on_wikipedia,
}

if __name__ == "__main__":

    # инициализация инструментов распознавания и ввода речи
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()
    ttsEngine = pyttsx3.init()

    # настройка данных пользователя
    person = OwnerPerson()
    person.name = "Tanya"
    person.home_city = "Yekaterinburg"

    # настройка данных голосового помощника
    assistant = VoiceAssistant()
    assistant.name = "Alice"
    assistant.sex = "female"
    assistant.speech_language = "en"

    # установка голоса по умолчанию
    setup_assistant_voice()

    while True:
        # старт записи речи с последующим выводом распознанной речи
        voice_input = record_and_recognize_audio()
        print(colored(voice_input, "blue"))

        # отделение комманд от дополнительной информации (аргументов)
        voice_input = voice_input.split(" ")
        command = voice_input[0]
        command_options = [str(input_part) for input_part in voice_input[1:len(voice_input)]]
        execute_command_with_code(command, command_options)

# TODO weather
# TODO get current time/date in place
# TODO toss a coin (get random value to choose something)
# TODO take screenshot
# TODO translate