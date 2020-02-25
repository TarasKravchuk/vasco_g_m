Before installation, please make sure that at your computer already installed:
Python ver. >= 3.6  (project was created at ver == Python 3.6.8)
PostgreSQL ver. >= 10

INSTALLATION:
Create DB, Test DB and DB Owner
run in your terminal:
sudo -u postgres psql postgres
create user vasco_db_admin with password 'Very_protected_password_123';
alter role vasco_db_admin set client_encoding to 'utf8';
create database vasco_db owner vasco_db_admin;
create database test_vasco_db owner vasco_db_admin;
alter user vasco_db_admin CREATEDB;

run in your virtualenv 
pip3 install -r requirements.txt

please be sure that everything is installed successfully

in folder where located manage.py run:
python3 manage.py runserver

in case 8000 port are occupied run 
python3 manage.py runserver [free port]

to run Django tests in folder where located manage.py run:
python3 manage.py test vasco_engine.tests
