from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Movie(models.Model):
    RATING_CHOICES = [
        ('G', 'G'),
        ('PG', 'PG'),
        ('PG-13', 'PG-13'),
        ('R', 'R'),
        ('NC-17', 'NC-17'),
        ('Not Rated', 'Not Rated'),
        ('Approved', 'Approved'),
        ('TV-PG', 'TV-PG'),
        ('Unrated', 'Unrated'),
        ('X', 'X'),
        ('TV-MA', 'TV-MA'),
        ('TV-14', 'TV-14')
    ]

    name = models.CharField(max_length=255)
    rating = models.CharField(max_length=10, choices=RATING_CHOICES)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(1800), MaxValueValidator(2030)]
    )
    released = models.CharField(max_length=100, blank=True)
    score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
    )
    votes = models.PositiveIntegerField()
    director = models.CharField(max_length=255, blank=True)
    writer = models.CharField(max_length=255, blank=True)
    star = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    budget = models.FloatField(null=True, blank=True)
    gross = models.FloatField(null=True, blank=True)
    company = models.CharField(max_length=255, blank=True)
    runtime = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year', 'name']
        unique_together = ['name', 'year']

    def __str__(self):
        return f"{self.name} ({self.year})"

    @property
    def profit(self):
        if self.gross is not None and self.budget is not None:
            return self.gross - self.budget
        return None


class WeatherRecord(models.Model):
    CITY_CHOICES = [
        ('Jacksonville', 'Jacksonville'),
        ('Miami', 'Miami'),
        ('Orlando', 'Orlando'),
        ('Tampa', 'Tampa'),
        ('St. Petersburg', 'St. Petersburg')
    ]

    city = models.CharField(max_length=50, choices=CITY_CHOICES)
    date = models.DateField()
    temp_max = models.FloatField(null=True, blank=True)
    temp_min = models.FloatField(null=True, blank=True)
    sunrise = models.DateTimeField(null=True, blank=True)
    sunset = models.DateTimeField(null=True, blank=True)
    uv_index = models.FloatField(null=True, blank=True)
    precip_probability = models.FloatField(null=True, blank=True)
    rain_sum = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['city', 'date']

    def __str__(self):
        return f"{self.city}, {self.date},  {self.temp_min}C - {self.temp_max}C"