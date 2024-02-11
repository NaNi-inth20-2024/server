# Charity Auction Project

### [Visit our website](http://20.82.148.177/)

### Run manually instruction:
1. Install Python 3.11
2. `git clone` this repository 
3. Enter the repository folder and run `python -m venv venv`
4. Activate the virtual environment with `venv/Script/activate` or (MacOS / Linux) `source venv/bin/activate`
5. Copy `.example.env` as `.env` and set your variables
6. Install postgresql and redis (instruction for Windows):
- Install wsl with Ubuntu
- Inside wsl run `sudo apt update`, `sudo apt install postgresql`, `sudo apt install redis-server`
- Start the services with `sudo service postgresql start`, `sudo service postgresql start`
- Enter PostgreSQL `sudo -u postgres psql postgres` and run `CREATE DATABASE _name_of_your_db; `
7. While being in Python virtual environment run `pip-compile requirements/requirements.ini` and `pip-sync requirements/requirements.txt`
8. Run `python manage.py migrate`
9. Run `python manage.py runserver`

Now your local application should be up and running!