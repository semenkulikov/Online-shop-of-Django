# Правила разработки

1.django
2.postgresql
3.ajax
4.celery
5.numba - jit(для ускорения) декоратор
6.beartype декоратор
7.mediater - library
8.injector - library
9.pydantic
10.flake8
11.pre-commit
12.


pattern
CQRS  - как основу(usecases)
repository - для моделей



app
    core
        inject.py
        constant.py
        ....
    project
        settings
        url
        ....
    catalog
        interface
            product
        repository
            product
        usecases
            dto
            handlers
            requests
    auth
        .....
    pay
        gataweys
            queries
                dto
                handler
                requests
            commands
                dto
                handler
                request


or

standart
    mvt

# Оформления
    Каждый модуль каждый метод должен быть описан и соблюдены правила написания кода
    Каждое апп должно заканчиваться на app
        authapp
# linter
    pep8
    flake8
    isort

# commit
    1.Все форкаемся только от development
    2.Каждая новая задача начинается с того что вы сливаете себе все изменения из ветки development методом pull
    3.Вы делаете мр или в idea или в гитлабе и пишите в чате что вы сделали мр.
    4.Я проверяю если все ок сливаю в дев и другой участник уже может забрать себе всю инфу если есть замечания я их сделаю 
    5.Если фича  origin/feature/description(работа с оплатой)
    6.Если баг   origin/bugfix/description(исправления ошибки работа с ордерам)

# gitignore
    Добавить вашу базу в гитигноре
