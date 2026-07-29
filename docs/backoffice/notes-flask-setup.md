# Flask backoffice — setup notes

Notes taken while setting up the Flask app structure. Meant to help
teammates understand the choices, not as a launch guide (see the README
for that).

## Why Flask
Chosen because it is what we covered in the Python course — avoids a brutal
context switch for the team.

## Werkzeug — the HTTP layer under Flask
Flask relies on Werkzeug underneath. Werkzeug:
- turns a raw incoming HTTP request into a Python `request` object usable
  in our code
- provides the development server (`flask run` / `app.run()`)

The dev server is fine for development but is **not meant for production**
(not built to handle production traffic, slow requests, load spikes). In
production it is replaced by a WSGI server such as **gunicorn**. Our Flask
app itself does not change — only the server running it does.

## Blueprints
A blueprint is an intermediate "route holder": routes are attached to the
blueprint, and the blueprint is registered on the app in `create_app()`.

Why:
- avoids one endless file with all routes
- avoids circular imports (a route module never imports the app)

One blueprint per resource: health, users, branches, stock.

## The `__name__` argument
`Flask(__name__)` tells Flask where the app is located, so it can find the
`templates/` and `static/` folders automatically. Same reason for
`Blueprint("name", __name__)`.

## Ports
- Chose `8080` on the host because `5000` was already taken (macOS).
- Any free port above 1024 works (1024 and below are privileged /
  "well-known" ports). Common alternatives: 8888, 3000.
- Host and container ports are different:
```yaml
  ports:
    - "8080:5000"
  #    │    │
  #    │    └─ port INSIDE the container (what Flask listens on)
  #    └─ port ON the host (what you type in the browser)
```
- Ports can be moved to environment variables to stay configurable.

## Config
`config.py` centralizes reading environment variables (from `.env`, via
`os.environ`).
`app.config.from_object(Config)` copies the uppercase attributes of the
`Config` class into `app.config`, making them readable everywhere via
`app.config["SECRET_KEY"]`.