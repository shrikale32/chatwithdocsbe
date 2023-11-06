# Chat With Docs Backend

Chat with docs allows users to chat with PDF documents.

### Application Architecture

<img width="1079" alt="Screen Shot 2023-11-06 at 10 12 52 AM" src="https://github.com/shrikale32/chatwithdocsbe/assets/27811189/b307c16c-42c8-4992-a9fe-356f8aa993d5">

## Installing

Step by step commands on how to run this project on your computer

1)- Install Virtualenv

```
pip install virtualenv
```

2)- Create Virtualenv

```
virtualenv venv
```

3)- Activate virtual env

```
venv/Scripts/activate
```

4)- Install requirements

```
pip install -r requirements.txt
```
Note: Above lines are required for first time installation

5)- Execute below commands

```
python manage.py makemigrations
python manage.py migrate
```
Note: Above commands should be executed if there is any db level changes

6)- Create superuser for admin access and follow instruction, if not created one

```
python manage.py createsuperuser
```

7)- Run the application

```
python manage.py runserver
```
And the project is ready for use on your computer!
