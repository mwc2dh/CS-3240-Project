# CS-3240-Project
This repository is a copy of my course project for the Advanced Software Development Methods (CS 3240) course at UVA (Fall 2022).

During the Fall 2022 semester, this application was hosted on Heroku. To view it now, follow these steps:

1. Install [virtualenv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)
2. Create your virtual env by running `py -m venv env` (Windows) or `python3 -m venv env` (Mac/Unix) in your terminal from the project directory.
3. Activate you virtual environment. Do this by running `./env/Scripts/activate`
4. Once you have activated the virtual environment, you will need to install the required Python packages. Run the command `pip install -r requirements.txt`
5. Migrate the databases with the command `python manage.py migrate`
6. After migrating the databases, run `python manage.py runserver` and navigate to http://127.0.0.1:8000 on your web browser of choice.
7. To import the data to the website, navigate to http://127.0.0.1:8000/loadall. You will see the command prompt begin to import the data from the JSON folder and create courses.