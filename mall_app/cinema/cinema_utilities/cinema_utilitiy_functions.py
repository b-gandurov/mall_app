from mall_app.cinema.models import HallSeat


# Function to create hall seats based on capacity and fixed column number
def create_hall_seats(hall):
    HallSeat.objects.filter(hall=hall).delete()

    number_of_rows = hall.capacity // 16

    for row in range(1, number_of_rows + 1):
        for column in range(1, 17):
            HallSeat.objects.create(hall=hall, row=row, column=column)
