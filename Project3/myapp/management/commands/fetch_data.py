from datetime import datetime, date
from zoneinfo import ZoneInfo

import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from myapp.models import WeatherRecord


API_URL = "https://api.open-meteo.com/v1/forecast"
NY_TZ = ZoneInfo("America/New_York")

LOCATIONS = [
    {"name": "Jacksonville", "latitude": 30.3322, "longitude": -81.6556},
    {"name": "Miami", "latitude": 25.7743, "longitude": -80.1937},
    {"name": "Tampa", "latitude": 27.9475, "longitude": -82.4584},
    {"name": "Orlando", "latitude": 28.5383, "longitude": -81.3792},
    {"name": "St. Petersburg", "latitude": 27.7709, "longitude": -82.6793},
]

DAILY_FIELDS = [
    "temperature_2m_max",
    "temperature_2m_min",
    "sunrise",
    "sunset",
    "uv_index_max",
    "precipitation_probability_max",
    "rain_sum",
]


def _parse_date(value):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date() if isinstance(value, str) else value


def _parse_datetime(value):
    if not value:
        return None
    dt = datetime.fromisoformat(value)
    if timezone.is_naive(dt):
        dt = dt.replace(tzinfo=NY_TZ)
    return dt


def _get_daily_value(daily, key, index):
    values = daily.get(key) or []
    if index < len(values):
        return values[index]
    return None


class Command(BaseCommand):
    help = "Fetch latest 7-day forecast from Open-Meteo for Florida cities and save to DB."

    def handle(self, *args, **options):
        created_total = 0
        updated_total = 0

        for city in LOCATIONS:
            params = {
                "latitude": city["latitude"],
                "longitude": city["longitude"],
                "daily": ",".join(DAILY_FIELDS),
                "timezone": "America/New_York",
            }

            try:
                resp = requests.get(API_URL, params=params, timeout=30)
                resp.raise_for_status()
                data = resp.json()
            except requests.exceptions.Timeout:
                self.stderr.write(f"[{city['name']}] Request timed out, skipping.")
                continue
            except requests.exceptions.RequestException as err:
                self.stderr.write(f"[{city['name']}] Request error: {err}")
                continue
            except ValueError as err:
                self.stderr.write(f"[{city['name']}] Invalid JSON: {err}")
                continue

            daily = data.get("daily", {}) or {}
            dates = daily.get("time", []) or []

            created_city = 0
            updated_city = 0

            with transaction.atomic():
                for i, day_str in enumerate(dates):
                    day = _parse_date(day_str)
                    if day is None:
                        continue

                    defaults = {
                        "temp_max": _get_daily_value(daily, "temperature_2m_max", i),
                        "temp_min": _get_daily_value(daily, "temperature_2m_min", i),
                        "sunrise": _parse_datetime(_get_daily_value(daily, "sunrise", i)),
                        "sunset": _parse_datetime(_get_daily_value(daily, "sunset", i)),
                        "uv_index": _get_daily_value(daily, "uv_index_max", i),
                        "precip_probability": _get_daily_value(daily, "precipitation_probability_max", i),
                        "rain_sum": _get_daily_value(daily, "rain_sum", i),
                    }

                    _, created = WeatherRecord.objects.update_or_create(
                        city=city["name"],
                        date=day,
                        defaults=defaults,
                    )
                    if created:
                        created_city += 1
                    else:
                        updated_city += 1

            self.stdout.write(
                f"[{city['name']}] created={created_city} updated={updated_city}"
            )
            created_total += created_city
            updated_total += updated_city

        self.stdout.write(self.style.SUCCESS(
            f"Done. Created {created_total}, updated {updated_total} weather records."
        ))
