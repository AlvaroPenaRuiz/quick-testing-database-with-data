# The Legend Of Pinha The Database Master

## Deployment

1. Make sure you have running the docker daemon.
2. From the root folder of the project run

```
docker compose up
```

## Connecting

### Adminer

You can access through the adminer panel with your web browser at:
[http://localhost:8080/](http://localhost:8080/)

> **Server**: db
> **User**:  root
> **Password**: 123456
> **Database**: Learning

---



### MySQLWorkbench

Create a connection with the following information:

> **Hostname**: 127.0.0.1
> **Port**: 3306
> **User**:  root
> **Default Schema**: Learning

Password will be asked after and is also "123456"

---

## Extra Info

Everything you put inside "src/init/" will go to "/docker-entrypoint-initdb.d/" in the container. Those scripts will run the first time the database is initializated (actually it will consider it is a new database if the docker volume used changes the name)).


---



## TROUBLESHOOTING

### Problem creating the default tables and populating them

1. Stop the containers.
2. Delete the containers.
3. Delete the volume.
4. Run again the docker compose.
