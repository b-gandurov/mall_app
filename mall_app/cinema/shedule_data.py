import os
import django
import random
from datetime import timedelta

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mall_app.settings')
django.setup()

# Import the necessary models now that the Django environment has been setup
from mall_app.cinema.models import CinemaHall, Movie, Schedule
from django.utils import timezone

def generate_schedules():
    # Get all halls and movies
    halls = list(CinemaHall.objects.all())
    movies = list(Movie.objects.all())

    # Ensure that there are some halls and movies
    if not halls or not movies:
        print("Please make sure there are some halls and movies before running this script.")
        return

    # Generate 30 schedules
    for _ in range(30):
        hall = random.choice(halls)
        movie = random.choice(movies)
        show_time = timezone.now() + timedelta(days=random.randint(1, 60), hours=random.randint(0, 23))  # random date and time in the next 60 days

        schedule = Schedule(hall=hall, movie=movie, show_time=show_time)
        schedule.save()

    print("30 schedules have been created.")

generate_schedules()
