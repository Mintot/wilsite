# CIT-U Wildcat Innovation Labs Web App

This is the official Wildcat Innovation Labs Website which is still under construction.
Here is where you book our facilities: Coworking Space and Conference Rooms.

## Development
### Modules
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required modules for this app.

```bash
pip install -r requirements.txt
```
### Database
You would also need to have [XAMPP](https://www.apachefriends.org/download.html) for the database.
After installing XAMPP, do the following tasks:
* Before Starting MySQL, click the "Config" button and choose "my.ini".
* Under [mysqld], add the following line, typically at line 45:
```text
skip-grant-tables
```
* Save the file.
* Start MySQL in XAMPP.
* Go to the database admin at localhost/phpmyadmin.
* Go to Import tab.
* Click "Choose file" and choose "db.sql" found in this application.

### Server
In order to run the application in Django, do the following in your command prompt:
```bash
python manage.py migrate
python manage.py runserver
```

### Adding Custom Users
To add users including yourselves:
* Go back to the database admin at localhost/phpmyadmin.
* Under "db", select "account_client".
* Go to "Insert" tab.
* Only fill the "Username" field. It can be any string as you'd like.
* Navigate yourself to the bottommost part of the page and click "Go" (the one beside "Reset").
* Now go back to "[your site]/signin", place your username, fill up more fields, and click "Submit".
* Now you can go to booking via "[your site]/booking".

### Testcases
For the tests on startups and technopreneurship functionality, I have created thousands of dummy data with testcases.
They can be viewed [on our shared Google Drive](https://drive.google.com/drive/u/0/folders/19jZIcuH_OkQ7swMcJ6k6zdbDhKdO9SxO).
You are also to re-do the "Database" and "Server" steps above.

## Contact Us
Should you have concerns, we are reachable via the following:
* Back End Support: Jay Vince Serato - jayvince.serato@gmail.com
* Front End Support: Pinkfloyd Adonay - pinkfloyd.adonay@gmail.com

Happy coding!