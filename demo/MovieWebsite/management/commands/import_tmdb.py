import os
import requests
from dotenv import load_dotenv
from django.conf import settings
from django.core.management.base import BaseCommand
from MovieWebsite.models import Movie, TvShow, Genre

BASE = "https://api.themoviedb.org/3"
PAGES = 5

def year_of(date_str):
    return int(date_str[:4]) if date_str else None

class Command(BaseCommand):
    help = "Import movies and TV shows from TMDB"

    def handle(self, *args, **options):
        load_dotenv()
        token = os.environ.get("TMDB_TOKEN")
        if not token:
            self.stderr.write("TMDB_TOKEN not found in environment variables.")
            return

        session = requests.Session()
        session.headers.update({
            "Authorization": f"Bearer {token}"})


        def get(path, **params):
            r = session.get(f"{BASE}/{path}", params=params, timeout=10)
            r.raise_for_status()
            return r.json()


        for kind in ("movie", "tv"):
            for g in get(f"genre/{kind}/list")["genres"]:
                Genre.objects.update_or_create(
                    tmdb_id=g["id"],
                    defaults={"name": g["name"]}
                )

        movies_count = 0
        for page in range(1, PAGES + 1):
            for m in get("movie/popular", page=page)["results"]:
                movie, _ = Movie.objects.update_or_create(
                    tmdb_id=m["id"],
                    defaults={
                        "title": m["title"],
                        "year": year_of(m.get("release_date","")),
                        "overview": m.get("overview", ""),
                        "poster_path": m.get("poster_path", ""),
                        "rating": round(m.get("vote_average") or 0, 1),
                    },
                )
                movie.genres.set(
                    Genre.objects.filter(tmdb_id__in=m.get("genre_ids", []))
                )
                movies_count += 1



        shows_count = 0
        for page in range(1, PAGES + 1):
            for t in get("tv/popular", page=page)["results"]:
                details = get(f"tv/{t['id']}")
                ended = details.get("status") in ("Ended", "Canceled")
                show, _ = TvShow.objects.update_or_create(
                    tmdb_id=t["id"],
                    defaults={
                        "title": t["name"],
                        "year": year_of(t.get("first_air_date", "")),
                        "toyear": year_of(t.get("last_air_date", "")),
                        "overview": t.get("overview", ""),
                        "poster_path": t.get("poster_path", ""),
                        "rating": round(t.get("vote_average") or 0, 1),
                    }
                )

                show.genres.set(
                    Genre.objects.filter(tmdb_id__in=t.get("genre_ids", []))
                )
                shows_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {movies_count} movies and {shows_count} TV shows from TMDB."
            )
        )