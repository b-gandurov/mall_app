from django.db import models

from mall_app.users.models import UserProfile


class CinemaHall(models.Model):
    hall_name = models.CharField(max_length=255)
    capacity = models.IntegerField()

    class Meta:
        verbose_name_plural = "Halls"

    def __str__(self):
        return self.hall_name


class Movie(models.Model):
    movie_name = models.CharField(max_length=255)
    movie_type = models.CharField(max_length=255)
    duration = models.DurationField()
    halls = models.ManyToManyField(CinemaHall)

    class Meta:
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.movie_name


class Schedule(models.Model):
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Schedules"

    def __str__(self):
        return f"{self.movie.movie_name} in {self.hall.hall_name} at {self.show_time}"


class HallSeat(models.Model):
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE)
    row = models.PositiveIntegerField()
    column = models.PositiveIntegerField()
    taken = models.BooleanField(default=False)

    class Meta:
        unique_together = ['hall', 'row', 'column']

    def __str__(self):
        return f'Hall {self.hall_id}, Row {self.row}, Column {self.column}'


def create_hall_seats(hall):
    # Clear any existing seats for this hall
    HallSeat.objects.filter(hall=hall).delete()

    # The number of columns is constant (16), calculate the number of rows
    number_of_rows = hall.capacity // 16

    # Create the seats
    for row in range(1, number_of_rows + 1):
        for column in range(1, 17):  # Columns from 1 to 16
            HallSeat.objects.create(hall=hall, row=row, column=column)


class Ticket(models.Model):
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    seat = models.ForeignKey(HallSeat, on_delete=models.CASCADE)
    screening = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Tickets"

    def __str__(self):
        return f"Ticket {self.id} for {self.customer.user.email}"
