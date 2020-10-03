# Voice-Assistant-App
Проект голосового ассистента на Python 3, который умеет:
* воспроизводить случайное приветствие;
* воспроизводить случайное прощание с последующим завершением работы программы;
* производить поисковый запрос в поисковой системе Google
  (а также открывать список результатов и сами результаты данного запроса);
* производить поисковый запрос видео в системе YouTube и открывать список результатов данного запроса;
* выполнять поиск определения в Wikipedia c дальнейшим прочтением первых двух предложений;
* переводить с изучаемого языка на родной язык пользователя (с учетом особенностей воспроизведения речи);
* менять настройки языка распознавания и синтеза речи;
* TODO многое другое...

Голосовой ассистент использует для синтеза речи встроенные в операционную систему Windows 10 возможности
(т.е. **голоса зависят от операционной системы**). Для этого используется библиотека `pyttsx3`

    Для корректной работы системы распознавания речи в сочетании с библиотекой SpeechRecognition
    используется библиотека PyAudio для получения звука с микрофона.
    
Для установки PyAudio можно найти и скачать нужный в зависимости от архитектуры файл [здесь](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) в папку с проектом.
После чего его можно установить при помощи команды: `pip install PyAudio-0.2.11-cp37-cp37m-win_amd64.whl`

Команды для установки прочих сторонних библиотек:
Команда установки  | Назначение библиотеки
----------------|----------------------
`pip install google`       | Работа с результатами поиска в Google
`pip install SpeechRecognition`       | Работа с распознаванием речи (Speech-To-Text)
`pip install pyttsx3`   | Работа с синтезом речи на Windows (Text-To-Speech)
`pip3 install wikipedia-api`| Работа с Wikipedia API
`pip install googletrans`| Работа с Google Translate

Дополнительную информацию по установке и использованию библиотек можно найти [здесь](https://pypi.org/)
