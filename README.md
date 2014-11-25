# Hourglass

Hourglass is a tool to help contracting personnel estimate their per-hour labor costs for a contract, based on historical pricing information. The tool is in the very early stages of development. You can track our progress on our [trello board](https://trello.com/b/LjXJaVbZ/prices) or file an issue on this repo. 

# Setup

To install the requirements, use 
```
pip install -r requirements.txt
```

Currently, Hourglass is a basic Django project. You can get started by creating a local_settings.py file (based off of local_settings.example.py) with your local database configuration, and running 

```
./manage.py syncdb
```

to set up the database. After that, you can load all of the data by running 
```
./manage.py load_data
```

From there, you're just a hop, skip and a jump away from your own dev server, using 
```
./manage.py runserver
```

Currently the only endpoint is http://localhost:8000/api/rates/

You can search for prices of specific labor categories by using the q parameter. For example:
http://localhost:8000/api/rates/?q=accountant

You can also filter by the minimum education level, minimum years of experience, and maximum years of experience. For example:
http://localhost:8000/api/rates/?min_education=MA&min_experience=5&max_experience=10&q=technical

The valid values for min_education are AA (associates), BA (bachelors), MA (masters), and PHD (Ph.D).

The default pagination is set to 200. You can paginate using the page parameter. For example:
http://localhost:8000/api/rates/?q=translator&page=2

More to come soon!
