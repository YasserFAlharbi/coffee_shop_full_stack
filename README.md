# Coffee Shop Full Stack

## About the project:

A new digitally enabled cafe for students to order drinks, socialize, and study hard.

1) Display graphics representing the ratios of ingredients in each drink.
2) Allow public users to view drink names and graphics.
3) Allow the shop baristas to see the recipe information.
4) Allow the shop managers to create new drinks and edit existing drinks.

### This project demonstrate the following :

- Implementing authentication and authorization in Flask
- Designing against key security principals
- Implementing role-based control design patterns
- Securing a REST API
- Applying software system risk and compliance principles

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Securing the application with :

[auth0](https://auth0.com/)

## Auth0 Account configuration variables:

- AUTH0_DOMAIN = 'pixelcode.us.auth0.com'
- ALGORITHMS = ['RS256']
- API_AUDIENCE = 'Coffee-Shop'

### Application URI:

`https://pixelcode.us.auth0.com/authorize?response_type=token&client_id=iIuKpv3cETqwNZw2gaiCCUkjPVxPy1gG&redirect_uri=http://127.0.0.1:8100/tabs/user-page&audience=Coffee-Shop`

### Manager Access_token
`eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjIwcWhpd3ViZTZtOWR0NDM5NGE3cSJ9.eyJpc3MiOiJodHRwczovL3BpeGVsY29kZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYzZjAxYmY0NzY2ODMwMDY3ZWFmMWM4IiwiYXVkIjoiQ29mZmVlLVNob3AiLCJpYXQiOjE1OTgyODExMTEsImV4cCI6MTU5ODI4ODMxMSwiYXpwIjoiaUl1S3B2M2NFVHF3Tlp3MmdhaUNDVWtqUFZ4UHkxZ0ciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZHJpbmtzIl19.msK-N385CecP1yWofXdvoU4rtRlgO7ix6vLzb08MSnWif8uQzkAJy1FoiJ3nfI103QdsQI00zQaXlZTc7c_X_z19aU1Oa5-cY9HWYUOBTsYtdQ2bJO4ZT64_sA4Arfe8YgSxJSIYt2X5Fj4P8EViwpaxsx-_chRfwdHweEDAa1j59nF8CWHeraXXWKDkPYE_NP5qpcVNNOjbHSJeNuQweRqJfYoJXo5nP4hmw1CZZbUGjIFHGKyvsjugnHEYuJ-_pQ6rpzVMZLRjSqOhdPRtN9gYdeDPY3EUt_vGFwkE90lbibuUbRzPalY1ER1omAyAlCQbE1ewegif9cTN6wJvnQ`

### Barista Access_token
`eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjIwcWhpd3ViZTZtOWR0NDM5NGE3cSJ9.eyJpc3MiOiJodHRwczovL3BpeGVsY29kZS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYzZjAxNGRhMWI0MWYwMDY3ODFmMjJjIiwiYXVkIjoiQ29mZmVlLVNob3AiLCJpYXQiOjE1OTgyODE1MzksImV4cCI6MTU5ODI4ODczOSwiYXpwIjoiaUl1S3B2M2NFVHF3Tlp3MmdhaUNDVWtqUFZ4UHkxZ0ciLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpkcmlua3MtZGV0YWlsIl19.UujbR41AJmTyYUWi2OgFcfwP1KNmW4KoxaT3Fyfjxbn8dlzXOaKfB4Rye_7t4iGvcdeduRBip8_h1ynI6iPhIQ5j7y76px6HmxdlAS7nVsVhNHjvsnVi4cPe7pkHdv2t-WNAanuFxKDubEB2P7YhweZDsR2IMnQTrp7sxPM60ljNit5BOnmcu7ldQvt2gpzEem1stI6M56x579LcFqUrtGqxomelDusc_Jt1IWB_3BsKisrbkC0RKGCnw3iix3Ve-Rw_CNKW3PEfyj3EtOiffQ9IGFcL4-w_DUHmrtTPuuOG8D3Tv1wMj0yHL33vnSx4P0rsr1NN86X2Fx9SCbB_yA`

## Backend:

- Added Auth0 functionalities on auth.py
- Implemented RESTful endpoints on api.py
- Implemented error handlers 400, 404, 405, 422 on api.py
- Implemented Autherror handlers with appropriate status code indicating reason for failure on api.py

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Integration test with Postman :

- Exported collection with configured tokens can be found at: /backend/udacity-fsnd-udaspicelatte.postman_collection.json

- Test results containing 20 successful cases: /backend/Results_udacity-fsnd-udaspicelatte.postman_collection.json

## Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server.

[View the README.md within ./frontend for more details.](./frontend/README.md)