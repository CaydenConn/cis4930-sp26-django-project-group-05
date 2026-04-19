from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Movie, Genre, WeatherRecord
from .forms import MovieForm


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
