# DatabaseWrapper

After cloning the repository, open a terminal in the project folder.

Create a virtual environment: `python -m venv testEnv `

Activate the virtual environment: `source testEnv/bin/activate`

Install the required libraries: `pip install -r requirements.txt`

Run the application with: `python3 Web.py`

The website can be accessed with the link: <http://127.0.0.1:5000>

To import the database, a MySQL server is necessary: <https://dev.mysql.com/downloads/workbench/>
After the MySQL server is installed using a database IDE: <https://www.jetbrains.com/datagrip/download/> the SQL files can be imported by right-clicking on the `@localhost` then `New` and then `Query Console`. The content of the `Atelier.sql` has to be copied here and then run.
The predefined problems can be imported by right-clicking the new `Atelier` database in DataGrip, then `New` and finally `Query Console` where the stored procedures have to be copied and then run.
