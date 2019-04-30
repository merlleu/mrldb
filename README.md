# MrlDB by Rémi "Mr e-RL" LANGDORPH
## Copyright (c) 2019 Rémi LANGDORPH - mrerl@warlegend.net (under MIT license)

## Links:
#### [pypi project](https://pypi.org/project/mrldb/)
#### [github repo](https://github.com/merlleu/mrldb)

## Install with pypi:
```
pip install mrldb
```

### This package supports the followings database systems: mariadb, mysql, cassandra, sqlite3

# Tutorial script:
```python
from mrldb import MrlDBCassandra, MrlDBCluster, mdbcl
```

# we add a simple cassandra cluster as connection to the mrldb cluster, we set cc0 as an alias to the db
```python
mdbcl.add("cassandracluster0", MrlDBCassandra("127.0.0.2"), aliases=["cc0"])
```
# we can add other aliases to this connection:
```python
mdbcl.addalias("cassandracluster0", ["cc0_", "cassandra0", "testcluster"])
```
# you can connect to your host with password and username
```python
mdbcl.add("cassandracluster1", MrlDBCassandra("127.0.0.3", username="admin", password="something"))
```
# you can specify the database too
```python
mdbcl.add("cassandracluster2", MrlDBCassandra("127.0.0.4", database="mydbtest", aliases=["cc3"]))
```
# and the best, you can provide database structure to have advanced features
```python
mdbcl.add("cassandracluster3", MrlDBCassandra("127.0.0.5", database="mydbtest",
structure={"table0": {"col1": "integer unique", "col2": "text"}, "table2": {"name": "text"}}), aliases=["cc3"])
```

## the following examples are working for all the differents database systems
### SELECT
## with the correct structure, the following command will give you for each records a dict with the col name and the value, (you can replace the columns by a `"*"`
```python
mdbcl.get("cc3").select(table="table0", columns=["col1"], conds=None)
```
# result= [{"col1": 0}, {"col1": 1}...]

## you can use this without structure, it just return the results without dictionnarys
```python
mdbcl.get("cc2").select(table="table0", columns=["col1"], conds=None)
```
# result= [(0, ), (1, )...]

## you can use conditions
```python
mdbcl.get("cc3").select(table="table0", columns="*", conds="col2='test'")
```
# result= [{"col1": 0, "col2": "test"}, ...]


### INSERT
## data is a dict with all the values to insert
```python
mdbcl.get("cc3").insert(table="table0", data={"col1": 5, "col2": "ok"})
```

### UPDATE
# use data as the insert command, you can specify conditions with conds
```python
mdbcl.get("cc3").update(table="table0", data={"col1": 5, "col2": "ok"}, conds="col2='test'")
```


### DB init
# will create the table (or ignore if exists) as the structure
```python
mdbcl.get("cc3").init()
```
# with structure={"table0": {"col1": "integer unique", "col2": "text"}, "table2": {"name": "text"}}
# will execute the following commands:
```python
['CREATE TABLE IF NOT EXISTS table0(col1 integer unique, col2 text)',
 'CREATE TABLE IF NOT EXISTS table2(name text)']
 ```


### DOCUMENTATION

### STRUCTURE
# with structure, you can get the column names with the results in a dict for each records
# structure is an argument for all the DB classes, it must be a None oject or a dictionnary:
```python
MrlDBCassandra(... ,structure={"table0": {"col1": "integer unique", "col2": "text"}, "table2": {"name": "text"}}, ...)
```
# Imports:
* **MrlDBCluster**(): a cluster of databases, the last created *MrlDBCluster* can be accessible via **mdbcl**
```python
from mrldb import MrlDBCluster, mdbcl
mycluster=MrlDBCluster()
```
* **mdbcl**: return  the last created **MrlDBCluster**
```python
print(mdbcl)
```

* **MrlDBCassandra**(*cluster, db=None, structure=None, username=None, password=None*): a cassandra cluster handler, require library `cassandra-driver`
  * you can use the database you want or don't use it
  * username and passsword are only used with PlainTextAuthProvider, if you've configured users and password for your db, else, we're connecting as anonymous
* **MrlDBSqlite**(*file, structure=None, autocommit=0*): a sqlite file handler, require base library `sqlite3` (not recommanded)
  * the file is sqlite3 db file
  * autocommit is the time in seconds (can be a float) between each autocommit, disabled if set 0 (by default)
* **MrlDBMsql**(*host, database=None, structure=None, username=None, password=None*): a cassandra cluster handler, require library `mysql`
  * host is the ip adress of the host or a dns-resolvable name of the host
  * you can use the database you want
  * username and passsword are only used with PlainTextAuthProvider, if you've configured users and password for your db, else, we're connecting as anonymous
