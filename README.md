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
