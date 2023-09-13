# Configuring PostgreSQL

The following guide explains how to configure PostgreSQL to work with the CAP RSS API. This
is only necessary if its manually installed.

Create the appropriate roles and databases in PostgreSQL. First connect to postgres with the default user.

```shell
sudo -u postgres psql
```

Creating a role and a database

```sql
CREATE ROLE dba 
CREATEDB 
LOGIN 
PASSWORD 'Abcd1234';

CREATE DATABASE database_name
WITH
   OWNER = role_name;
```
