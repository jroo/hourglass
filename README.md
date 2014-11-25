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

More to come soon!
