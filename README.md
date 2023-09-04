# Бот-викторина

Бот-викторина с направленностью в исторические вопросы.

Демо бота:
 - [Телеграм](https://t.me/history_quizlet_bot)
 - [ВКонтакте](https://vk.com/im?sel=-222307795)

![Без имени](https://github.com/pas-zhukov/quiz-bot/assets/117192371/64f0b6da-32ed-4ed7-903b-69bde294b0cf)


# Развертывание бота

Первым делом, скачайте код:

```shell
git clone https://github.com/pas-zhukov/quiz-bot.git
```

Сразу установите важные зависимости командой:

```shell
pip install -r requirements.txt
```

Если будете разворачивать ботов при помощи Docker, хватит только библиотеки tqdm:
```shell
pip install tqdm==4.66.1
```

## Подготовка БД вопросов

В репозитории есть специальный скрипт, позволяющий создать БД вопросов на основе файлов из [этого архива](https://dvmn.org/media/modules_dist/quiz-questions.zip).

Скачайте архив с вопросами и распакуйте. Рекомендуется распаковывать не все файлы с вопросами, а несколько штук, иначе заполнение БД будет очень длительным.

Теперь выполните команду:
```shell
python quiz_questions.py <путь к папке с вопросами>
```

Вот так выглядит хороший результат.

![upload_questions.png](.github%2Fupload_questions.png)

_Некоторые вопросы могут не загрузиться из-за проблем с кодировкой, но таких меньшинство._

## Переменные окружения

Для работы Вам понадобится БД Redis. Получить можно после регистрации тут: https://redislabs.com/ (нужен VPN).

Для работы ботов необходимо в корне с программой создать файл `.env` и заполнить его следующим содержимым:
```shell
TG_BOT_TOKEN=<API-токен Вашего Телеграм-бота>
VK_BOT_TOKEN=<API-токен бота ВКонтакте>
REDIS_DB_HOST=<Адрес базы данных Redis>
REDIS_DB_PORT=<Порт БД Redis>
REDIS_DB_PASSWORD=<Пароль БД Redis>
```

## Запуск с помощью Docker

Соберите докер-образ:
```shell
docker build -t quiz-bot .
```

Запустите докер-контейнер:
```shell
docker run --env-file ./.env --restart=on-failure -d quiz-bot
```

_P.S.`./.env` замените на <путь к Вашему `.env` файлу>, если он не находился в корне с приложением._

В итоге запустятся оба бота!

## Простой запуск

Для запуска Телеграм бота используйте следующую команду:

```shell
python tg_bot.py
```

Для бот ВКонтакте:

```shell
python vk_bot.py
```

# Цели проекта

Код написан в учебных целях.
