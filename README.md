# Python com Django
## Comandos Utilizados
```bash
    ## Para criar o setup do django
    django-admin startproject setup .
    ## Para criar o setup do modulo
    python manage.py startapp <modulo>
    ## Para iniciar o server
    python manage.py runserver
    ## Para atualizar as migrações
    python manage.py makemigrations
    ## Para fazer a migração dos dados
    python manage.py migrate
    ## Para criar um super usuario
    python manage.py createsuperuser
```

## Bibliotecas utilizadas
```bash
    ## Para utilizar o django numa versão certa
    pip install Django==5.0.3
    ## Para utilizar apis
    pip install djangorestframework
    ## Para se ter uma navegação melhor nas apis
    pip install markdown
    ## Para se criar um arquivo de requerimentos
    pip freeze > requirements.txt
```