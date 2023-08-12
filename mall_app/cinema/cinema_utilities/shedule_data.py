import os
import django
import random
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mall_app.settings')
django.setup()

from mall_app.cinema.models import CinemaHall, Movie, Schedule
from django.utils import timezone


def generate_schedules():
    halls = list(CinemaHall.objects.all())
    movies = list(Movie.objects.all())

    if not halls or not movies:
        print("Please make sure there are some halls and movies before running this script.")
        return

    for _ in range(30):
        hall = random.choice(halls)
        movie = random.choice(movies)
        show_time = timezone.now() + timedelta(days=random.randint(1, 60),
                                               hours=random.randint(0, 23))

        schedule = Schedule(hall=hall, movie=movie, show_time=show_time)
        schedule.save()

    print("30 schedules have been created.")


generate_schedules()
