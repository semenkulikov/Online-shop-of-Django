# ci/cd создание image на гитлабе

# start project docker-compose.yaml


# install pre-commit
    create - .pre-commit-config.yaml
    pip install pre-commit
    pre-commit install(устанавливаем нашу настройку)

# running Celery
    pip install -r requirements.txt
    celery -A shope worker --loglevel=info

# Website translation
    python manage.py makemessages -l ru - сгенерировать переводы на русский язык
    python manage.py makemessages -l en - сгенерировать переводы на English
    python manage.py compilemessages - скомпиллировать переводы

# Apply fixtures
    python manage.py apply_fixtures - применить все фикстуры

# Running imports
    python manage.py run_imports - запустить импорты всех файлов в директории imports/expected_imports
    python manage.py run_imports -p <file_1> <file_2> <file_3> - запустить импорт указанных файлов 