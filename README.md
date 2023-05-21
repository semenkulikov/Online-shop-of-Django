# ci/cd создание image на гитлабе

# start project docker-compose.yaml


# install pre-commit
    create - .pre-commit-config.yaml
    pip install pre-commit
    pre-commit install(устанавливаем нашу настройку)

# running Celery
    pip install -r requirements.txt
    celery -A shope worker --loglevel=info
