from cassandra.cluster import Cluster

# CREATE TABLE foo (name text, age int, pet text, primary key (name, age)) ;

cluster = Cluster(['172.17.0.3'])
session = cluster.connect()
session.execute('USE test')
session.execute('insert into foo')
