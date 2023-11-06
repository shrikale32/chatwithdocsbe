# Chat With Docs Backend

Chat with docs allows users to chat with PDF documents. The project is designed to provide a seamless chat experience where users can upload PDF files and interact with an AI assistant in the context of uploaded documents.

### Application Architecture

<img width="1079" alt="Screen Shot 2023-11-06 at 10 12 52 AM" src="https://github.com/shrikale32/chatwithdocsbe/assets/27811189/b307c16c-42c8-4992-a9fe-356f8aa993d5">

## Installing

Follow the below steps to set up the project on your local system:

1) Clone the repository:
   
Open your terminal and run the following command:

```
git clone https://github.com/shrikale32/chatwithdocsbe.git
```

2) Navigate to the project directory

```
cd chatwithdocsbe
```

3)- Install Virtualenv

```
pip install virtualenv
```

4)- Create Virtualenv

```
virtualenv venv
```

5)- Activate virtual env

```
Windows - venv/Scripts/activate
Mac - source venv/bin/activate
```

6)- Install requirements

```
pip install -r requirements.txt
```
Note: Above lines are required for first time installation

7)- Execute below commands

```
python manage.py makemigrations
python manage.py migrate
```
Note: Above commands should be executed if there is any db level changes

8)- Create superuser for admin access and follow instruction, if not created one

```
python manage.py createsuperuser
```

9)- Run the application

```
python manage.py runserver
```
And the project is ready for use on your computer!
