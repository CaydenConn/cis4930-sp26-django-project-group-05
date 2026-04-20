from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Movie, Genre, WeatherRecord
from .forms import MovieForm
import pandas as pd
import json


def home(request):
    total_movies = Movie.objects.count()
    total_genres = Genre.objects.count()
    recent = Movie.objects.select_related('genre').order_by('-created_at')[:5]
    return render(request, 'myapp/home.html', {
        'total_movies': total_movies,
        'total_genres': total_genres,
        'recent': recent,
    })


def movie_list(request):
    qs = Movie.objects.select_related('genre').order_by('-year', 'name')
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'myapp/list.html', {'page_obj': page_obj})


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'myapp/detail.html', {'movie': movie})


def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save()
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = MovieForm()
    return render(request, 'myapp/form.html', {'form': form, 'action': 'Add'})


def movie_update(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'myapp/form.html', {'form': form, 'action': 'Edit', 'movie': movie})


def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')
    return render(request, 'myapp/confirm_delete.html', {'movie': movie})


def weather_list(request):
    qs = WeatherRecord.objects.order_by('-date')
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'myapp/weather_list.html', {'page_obj': page_obj})


def weather_detail(request, pk):
    record = get_object_or_404(WeatherRecord, pk=pk)
    return render(request, 'myapp/weather_detail.html', {'record': record})

# Reused aggregations from project 1
def analytics(request):
    # Pull all movie data from the ORM into a DataFrame
    movies_data = Movie.objects.select_related('genre').values(
        'name', 'genre__name', 'year', 'rating',
        'score', 'votes', 'budget', 'gross', 'runtime',
        'country', 'director',
    )
    df = pd.DataFrame(list(movies_data))

    # If database is empty
    if df.empty:
        return render(request, 'myapp/analytics.html', {
            'empty': True,
        })

    # Rename genre column for readability
    df.rename(columns={'genre__name': 'genre'}, inplace=True)

    # count, mean, min, and max for score, gross, and runtime
    summary_stats = {}
    for col in ['score', 'gross', 'runtime']:
        series = df[col].dropna()
        summary_stats[col] = {
            'count': int(series.count()),
            'mean': round(float(series.mean()), 2) if len(series) > 0 else 0,
            'min': round(float(series.min()), 2) if len(series) > 0 else 0,
            'max': round(float(series.max()), 2) if len(series) > 0 else 0,
        }

    # Average score of R-rated movies per year
    r_movies = df.loc[df['rating'] == 'R']
    r_movies_trend = r_movies.groupby('year').agg(
        avg_score=('score', 'mean'),
        movie_count=('name', 'count')
    ).sort_index(ascending=True)

    # Average gross revenue per genre
    genre_gross = df.dropna(subset=['gross'])
    genre_gross_summary = genre_gross.groupby("genre").agg(
        avg_gross=("gross", "mean"),
        total_gross=("gross", "sum"),
        movie_count=("name", "count"),
    ).sort_values("avg_gross", ascending=False)

    # Average ROI per country (top 10)
    df_roi = df.dropna(subset=['budget', 'gross']).copy()
    df_roi['roi'] = df_roi['gross'] / df_roi['budget']
    country_roi = df_roi.groupby("country").agg(
        avg_roi=("roi", "mean"),
        movie_count=("name", "count"),
    ).sort_values("avg_roi", ascending=False)


    return render(request, 'myapp/analytics.html', {
        'empty': False,
        'summary_stats': summary_stats,
    })