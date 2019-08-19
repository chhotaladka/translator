# translator
Web APIs for English to Hindi translation

## Install PostgreSQL for suggestions
sudo apt install postgresql postgresql-contrib libpq-dev

pip install psycopg2

## Configuring PostGREsql for Django

* Get into `postgres` user shell and enter `psql` shell
```
sudo su - postgres
psql
```

* Create Database

```
CREATE DATABASE transdb;
```

* Create User `root` and set password `root1234`

```
CREATE USER root WITH PASSWORD 'root1234';
```

* Set encoding to utf8

```
ALTER ROLE root SET client_encoding TO 'utf8';
```

* Grant privileges to root

```
GRANT ALL PRIVILEGES ON DATABASE transdb TO root;
```

* Exit SQL prompt to user's session

```
\q
exit
```

## Load word list for suggestions

python manage.py loadwordlist

 

