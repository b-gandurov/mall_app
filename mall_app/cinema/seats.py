import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mall_app.settings')
django.setup()

from mall_app.cinema.models import CinemaHall, HallSeat


def create_hall_seats(hall):
    # Clear any existing seats for this hall
    HallSeat.objects.filter(hall=hall).delete()

    # The number of columns is constant (16), calculate the number of rows
    number_of_rows = hall.capacity // 16

    # Create the seats
    for row in range(1, number_of_rows + 1):
        for column in range(1, 17):  # Columns from 1 to 16
            HallSeat.objects.create(hall=hall, row=row, column=column)


def generate_halls_and_seats():
    hall_data = [
        {'hall_name': 'CinemaHall 1', 'capacity': 300},
        {'hall_name': 'CinemaHall 2', 'capacity': 250},
        {'hall_name': 'CinemaHall 3', 'capacity': 200},
        {'hall_name': 'CinemaHall 4', 'capacity': 150},
        {'hall_name': 'CinemaHall 5', 'capacity': 100},
    ]

    for hall in hall_data:
        created_hall = CinemaHall.objects.create(**hall)
        create_hall_seats(created_hall)


generate_halls_and_seats()
