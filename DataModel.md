# Cassandra Data Model

## Clusters
The outermost structure in Cassandra is the cluster. Cassandra database is designed to be distributed over several machines operating together that appear as a single instance to the end user. A node holds a replica for different ranges of data. If the first node goes down, a replica can respond to queries. The peer-to-peer protocol allows the data to replicate across nodes in a manner transparent to the user, and the replication factor is the number of machines in your cluster that will receive copies of the same data.

## Keyspace
A cluster is a container for keyspaces. A keyspace is the outermost container for data in Cassandra, corresponding closely to a relational database. Like a relational database, a keyspace has a name and a set of attributes that define keyspace-wide behavior. In Cassandra, the basic attributes that you can set per keyspace are Replication factor,

## Replication factor
In simplest terms, the replication factor refers to the number of nodes that will act as copies (replicas) of each row of data. The replication factor essentially allows you to decide how much you want to pay in performance to gain more consistency / availability.
## Replica placement strategy
The replica placement refers to how the replicas will be placed in the ring. There are different strategies that ship with Cassandra for determining which nodes will get copies of which keys. These are SimpleStrategy (RackUnawareStrategy), OldNetworkTopologyStrategy (RackAwareStrategy), and NetworkTopologyStrategy (Datacenter-
ShardStrategy).
## Column families
In the same way that a database is a container for tables, a keyspace is a container for a list of one or more column families. A column family is roughly analagous to a table in the relational model, and is a container for a collection of rows. Each row contains ordered columns. Column families represent the structure of your data. Each keyspace has at least one and often many column families. Column families are each stored in separate files on disk, it’s important to keep related columns defined together in the same column family.
When you write data to a column family in Cassandra, you specify values for one or more columns. That collection of values together with a unique identifier is called a row. That row has a unique key, called the row key, which acts like the primary key unique identifier for that row.
It’s an inherent part of Cassandra's replica design that all data for a single row must fit on a single machine in the cluster. The reason for this limitation is that rows have an associated row key, which is used to determine the nodes that will act as replicas for that row. Further, the value of a single column cannot exceed 2GB.

## Columns
A column is the most basic unit of data structure in the Cassandra data model. A column is a triplet of a name, a value, and a clock, which can be thought of as a timestamp. In, Cassandra, you don't define the columns up front; you just define the column families you want in the keyspace, and then you can start writing data without defining the columns anywhere. That's because in Cassandra, all of a column's names are supplied by the client. This adds considerable flexibility to how your application works with data, and can allow it to evolve organically over time.

## Row
A Row is a set of columns with a row key. Row key must be unique for that column family.
Values in a row Column names are sorted.
Rows can be narrow or wide.

## Column Families
A column family is a set of rows.

## Super Column Families
Lets not talk about them, coz, I don't like them.

## Data Modeling Patterns
### Entities
Entities (users/services/objects) are typically modeled using narrow, fixed set of columns.
### Time Series Data
Time series data is modeled by chunking the time and each chunk is stored in a row with each column representing a time value.
### Event Modeling
An object is modeled using a series of updates / a series of objects.

## Design Differences Between RDBMS and Cassandra
### Joins
You cannot perform joins in Cassandra. If you have designed a data model and find that you need something like a join, you’ll have to either do the work on the client side, or create a denormalized second column family that represents the join results for you. This is common among Cassandra users. Performing joins on the client should be a very rare case; you really want to duplicate (denormalize) the data instead.
### No Referential Integrity
Cassandra has no concept of referential integrity, and therefore has no concept of joins. In a relational database, you could specify foreign keys in a table to reference the pri- mary key of a record in another table. But Cassandra does not enforce this. It is still a common design requirement to store IDs related to other entities in your tables, but operations such as cascading deletes are not available.
### Sorting Is a Design Decision
In RDBMS, you can easily change the order in which records are returned to you by using ORDER BY in your query. The default sort order is not configurable; by default, records are returned in the order in which they are written. If you want to change the order, you just modify your query, and you can sort by any list of columns. In Cassan- dra, however, sorting is treated differently; it is a design decision. Column family definitions include a CompareWith element, which dictates the order in which your rows will be sorted on reads, but this is not configurable per query.
### Denormalization
In relational database design, we are often taught the importance of normalization. This is not an advantage when working with Cassandra because it performs best when the data model is denormalized. It is often the case that companies end up denormalizing data in a relational database. There are two common reasons for this. One is Design Differences Between RDBMS and Cassandra | 57performance. Companies simply can’t get the performance they need when they have to do so many joins on years’ worth of data, so they denormalize along the lines of known queries. This ends up working, but goes against the grain of how relational databases are intended to be designed, and ultimately makes one question whether using a relational database is the best approach in these circumstances.
### Secondary Indexes
For traditional relational databases, secondary indexes work well with high cardinality.


## Data Model Patterns
### Time Series Data Model
CREATE TABLE temperature (
weatherstation_id text,
event_time timestamp,
temperature text,
PRIMARY KEY (weatherstation_id,event_time)
);



Now we can insert a few data points for our weather station.

INSERT INTO temperature(weatherstation_id,event_time,temperature)
VALUES (’1234ABCD’,’2013-04-03 07:01:00′,’72F’);

INSERT INTO temperature(weatherstation_id,event_time,temperature)
VALUES (’1234ABCD’,’2013-04-03 07:02:00′,’73F’);

INSERT INTO temperature(weatherstation_id,event_time,temperature)
VALUES (’1234ABCD’,’2013-04-03 07:03:00′,’73F’);

INSERT INTO temperature(weatherstation_id,event_time,temperature)
VALUES (’1234ABCD’,’2013-04-03 07:04:00′,’74F’);



A simple query looking for all data on a single weather station.

SELECT event_time,temperature
FROM temperature
WHERE weatherstation_id=’1234ABCD’;



A range query looking for data between two dates. This is also known as a slice since it will read a sequence of data from disk.

SELECT temperature
FROM temperature
WHERE weatherstation_id=’1234ABCD’
AND event_time > ’2013-04-03 07:01:00′
AND event_time < ’2013-04-03 07:04:00′;

### Row partitioned Time Series Data
CREATE TABLE temperature_by_day (
weatherstation_id text,
date text,
event_time timestamp,
temperature text,
PRIMARY KEY ((weatherstation_id,date),event_time)
);



Note the (weatherstation_id,date) portion. When we do that in the PRMARY KEY definition, the key will be compounded with the two elements. Now when we insert data, the key will group all weather data for a single day on a single row.

INSERT INTO temperature_by_day(weatherstation_id,date,event_time,temperature)
VALUES (’1234ABCD’,’2013-04-03′,’2013-04-03 07:01:00′,’72F’);

INSERT INTO temperature_by_day(weatherstation_id,date,event_time,temperature)
VALUES (’1234ABCD’,’2013-04-03′,’2013-04-03 07:02:00′,’73F’);

INSERT INTO temperature_by_day(weatherstation_id,date,event_time,temperature)
VALUES (’1234ABCD’,’2013-04-04′,’2013-04-04 07:01:00′,’73F’);

INSERT INTO temperature_by_day(weatherstation_id,date,event_time,temperature)
VALUES (’1234ABCD’,’2013-04-04′,’2013-04-04 07:02:00′,’74F’);



To get all the weather data for a single day, we can query using both elements of the key.

SELECT *
FROM temperature_by_day
WHERE weatherstation_id=’1234ABCD’
AND date=’2013-04-03′;

### Rolling Time Series
CREATE TABLE latest_temperatures (
weatherstation_id text,
event_time timestamp,
temperature text,
PRIMARY KEY (weatherstation_id,event_time),
) WITH CLUSTERING ORDER BY (event_time DESC);



Now when we insert data. Note the TTL of 20 which means the data will expire in 20 seconds.

INSERT INTO latest_temperatures(weatherstation_id,event_time,temperature)
VALUES (’1234ABCD’,’2013-04-03 07:03:00′,’72F’) USING TTL 20;

INSERT INTO latest_temperatures(weatherstation_id,event_time,temperature)
VALUES (’1234ABCD’,’2013-04-03 07:02:00′,’73F’) USING TTL 20;

INSERT INTO latest_temperatures(weatherstation_id,event_time,temperature)
VALUES (’1234ABCD’,’2013-04-03 07:01:00′,’73F’) USING TTL 20;

INSERT INTO latest_temperatures(weatherstation_id,event_time,temperature)
VALUES (’1234ABCD’,’2013-04-03 07:04:00′,’74F’) USING TTL 20;
