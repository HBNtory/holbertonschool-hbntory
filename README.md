# HBNtory README


## database service (MySQL)

Be sur to have your `.env` file at the root project with your credentials.

### 1. Start the database
Launch the container in background with the following command:
```bash
docker-compose up -d
```

### 2. Connect with CLI:
Connect as root:
```bash
docker-compose exec db mysql -u root -p
```
Connect as app user
```bash
docker-compose exec db mysql -u hbntory_app -p hbntory
```
*(💡 Adding “hbntory” at the end of this command connects you directly to the correct database.)*

### 3.Stop the database
```bash
docker-compose down
```
*Note: if you want to reset everything and delete the saved data, use `docker-compose down -v`*