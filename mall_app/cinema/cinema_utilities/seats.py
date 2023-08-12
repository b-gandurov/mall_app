import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mall_app.settings')
django.setup()

from mall_app.cinema.models import CinemaHall, HallSeat


def create_hall_seats(hall):
    HallSeat.objects.filter(hall=hall).delete()

    number_of_rows = hall.capacity // 12

    for row in range(1, number_of_rows + 1):
        for column in range(1, 12):
            HallSeat.objects.create(hall=hall, row=row, column=column)


def generate_halls_and_seats():
    hall_data = [
        {'hall_name': 'CinemaHall 1', 'capacity': 144},
        {'hall_name': 'CinemaHall 2', 'capacity': 144},
        {'hall_name': 'CinemaHall 3', 'capacity': 96},
        {'hall_name': 'CinemaHall 4', 'capacity': 96},
        {'hall_name': 'CinemaHall 5', 'capacity': 48},
    ]

    for hall in hall_data:
        created_hall = CinemaHall.objects.create(**hall)
        create_hall_seats(created_hall)


generate_halls_and_seats()
