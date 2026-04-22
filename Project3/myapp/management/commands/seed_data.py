from django.core.management.base import BaseCommand
from myapp.models import Genre, Movie 
import pandas as pd

class Command(BaseCommand):
    help = "Load cleaned dataset into a database"

    def handle(self, *arg, **options):
        df = pd.read_csv("data/cleaned_movies_data.csv")
        
        created_count = 0
        for _, row in df.iterrows():
            genre_name = str(row['genre']).strip()
            genre, _ = Genre.objects.get_or_create(name=genre_name)

            Movie.objects.update_or_create(
                name = str(row['name']).strip(),
                year = int(row['year']),
                defaults={
                    'genre': genre,
                    'released': str(row['release_date']),
                    'rating': str(row['rating']),
                    'score': float(row['score']),
                    'votes': int(row['votes']),
                    'director': str(row.get('director', '')).strip(),
                    'writer': str(row.get('writer', '')).strip(),
                    'star': str(row.get('star', '')).strip(),
                    'country': str(row.get('country', '')).strip(),
                    'budget': float(row['budget']),
                    'gross': float(row['gross']),
                    'company': str(row.get('company', '')).strip(),
                    'runtime': float(row['runtime']),
                }
            )

            created_count += 1
        self.stdout.write(self.style.SUCCESS(f"Loaded ${created_count} Data Entries"))