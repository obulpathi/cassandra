# Cassandra Query Language

## Create keyspace
* CREATE KEYSPACE app;
* CREATE KEYSPACE app WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 3};
* CREATE KEYSPACE app WITH REPLICATION = {'class': 'NetowrkTopologyStrategy', 'DC1': 3, 'DC2': 3};

## Create table
* CREATE TABLE users (name varchar, city varchar, age int, PRMIMARY KEY(name, city));

## Describe commands
* DESCRIBE KEYSPACES;
* DESCRIBE KEYSPACE app;
* DESCRIBE TABLES;
* DESCRIBE TABLE users;

## Insert into table
* INSERT INTO users (name, city, age) VALUES ('Obul', 'Atlanta', 30);
* INSERT INTO users (name, city) VALUES ('Dheeraj', 'Vijayawada');
* INSERT INTO users (name, city, age) VALUES ('Unknown', 'Unknown', 35) USING TTL 100;

## Select Query
* SELECT * FROM users;
* SELECT name, city FROM users ORDER BY name ASC;
* SELECT name, city FROM users WHERE name = 'Obul';
* SELECT TTL(age) FROM users WHERE name = 'Unkown';
* SELECT WRITETIME(age) FROM users;

## Adding Columns to a table
* ALTER TABLE users ADD year int;
* ALTER TABLE users DROP year;

## Change type of a table
* ALTER TABLE users ALTER year TYPE varchar

## TTL
* INSERT INTO users (name, city, age) VALUES ('Unknown', 'Uknown', 42) USING TTL 3600;
* UPDATE users USING TTL 3600 SET age = 38 WHERE name = 'Unknown'

## DROP
* DROP TABLE users;
* DROP KEYSPACE app;

## DELETE
* DELETE FROM users WHERE name = 'Unknown';
* DELETE age FROM users WHERE name = 'Unknown';

## INDEX
* CREATE INDEX age_key ON users (age);

## TRNUCATE
* TRUNCATE services;
