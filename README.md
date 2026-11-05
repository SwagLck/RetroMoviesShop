# Retro Movie Shop

A Django website that shows movies and TV shows from TMDb.

## Setup

1. Clone the project:

```
git clone <repo-url>
cd RetroMovieShop
```

2. Create and activate a virtual environment:

```
python -m venv .venv
.venv\Scripts\activate
```

If PowerShell says "running scripts is disabled", run this once and try again:

```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

3. Install the packages:

```
pip install -r requirements.txt
```

4. Here you can create an account at https://www.themoviedb.org, then go to Settings > API and copy the API Read Access Token.

5. Create a file `.env` inside the `demo` folder (next to `manage.py`):

```
TMDB_TOKEN=(here goes the token)
```

6. Set up the database and import the data:

```
cd demo
python manage.py migrate
python manage.py import_tmdb
```

7. Start the server:

```
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.
