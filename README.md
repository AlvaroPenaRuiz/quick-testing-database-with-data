# The Legend Of Pinha The Database Master

An educational SQL exercise database with a web interface (Adminer) and a reset API.

## Project structure

```
src/
  init/             # SQL scripts loaded on first DB startup
    0-initdb.sql    # Table definitions
    1-filldb.sql    # Sample data
  reset-api/        # Flask API to reset the database
docker-compose.yml       # Local / dev mode
docker-compose.prod.yml  # Production mode (Traefik)
```

---

## Mode 1 — Local / dev

### Start

```bash
docker compose up
```

### Adminer

[http://localhost:8080](http://localhost:8080)

| Field    | Value    |
|----------|----------|
| Server   | db       |
| User     | root     |
| Password | 123456   |
| Database | Learning |

### Reset API

| Action | Command |
|--------|---------|
| Info   | `GET http://localhost:8081/` |
| Health | `GET http://localhost:8081/health` |
| Reset  | `POST http://localhost:8081/reset` with header `X-Reset-Token: changeme` |

```bash
curl -X POST http://localhost:8081/reset -H "X-Reset-Token: changeme"
```

### DBeaver / IDE

| Field    | Value     |
|----------|-----------|
| Host     | 127.0.0.1 |
| Port     | 3306      |
| User     | root      |
| Password | 123456    |
| Database | Learning  |

---

## Mode 2 — Production / Traefik

### Requirements

- Traefik already running with an external Docker network named `traefik`
- Entrypoint: `websecure`, cert resolver: `letsencrypt`
- These names can be changed in `docker-compose.prod.yml` if your setup differs

### Environment variables

Create a `.env` file in the project root (never commit it):

```env
DB_PASSWORD=your_strong_password
RESET_TOKEN=your_secret_token
```

### Start

```bash
docker compose -f docker-compose.prod.yml up -d
```

### URLs

| Service | URL |
|---------|-----|
| Adminer | https://test-db.alvaropenaruiz.com/adminer |
| API info | https://test-db.alvaropenaruiz.com/api |
| Health  | https://test-db.alvaropenaruiz.com/api/health |
| Reset   | `POST https://test-db.alvaropenaruiz.com/api/reset` |

```bash
curl -X POST https://test-db.alvaropenaruiz.com/api/reset \
  -H "X-Reset-Token: your_secret_token"
```

### DBeaver / IDE (production)

Port 3306 is published on the host. You can connect directly or via SSH tunnel.

**Direct connection:**

| Field    | Value                               |
|----------|-------------------------------------|
| Host     | test-db.alvaropenaruiz.com (or IP)  |
| Port     | 3306                                |
| User     | root                                |
| Password | value of `DB_PASSWORD`              |
| Database | Learning                            |

**SSH tunnel (more secure if the port should not be public):**

```bash
ssh -L 3307:localhost:3306 user@your-server
# Then connect DBeaver to localhost:3307
```

> If you want to block direct external access to port 3306, remove or comment out
> `ports: "3306:3306"` in `docker-compose.prod.yml` and use the SSH tunnel instead.

### Note about Adminer under /adminer

Adminer may sometimes misbehave under a path prefix (broken CSS, wrong redirects after login)
because it generates absolute internal links. If that happens, switch to a subdomain in
`docker-compose.prod.yml`:

1. Change the Adminer router rule to:
   ```
   traefik.http.routers.test-db-adminer.rule=Host(`adminer.test-db.alvaropenaruiz.com`)
   ```
2. Remove the `middlewares` label and the `stripprefix` middleware label for Adminer.

---

## Extra info

Everything inside `src/init/` is copied to `/docker-entrypoint-initdb.d/` in the DB container.
Those scripts run only the first time the database is initialized (i.e. when the Docker volume
is new or has been deleted).

The reset API drops and recreates the `Learning` database from those same SQL scripts,
so it always leaves the database in the same state as a fresh start.

---

## Troubleshooting

### Tables not created or not populated on first start

1. Stop the containers
2. Delete the containers
3. Delete the Docker volume
4. Run `docker compose up` again

### Reset API cannot reach the database

Check that both services share the `internal` network and that `DB_HOST=db` is set.

### Adminer shows broken layout under /adminer

See the [note above](#note-about-adminer-under-adminer).
