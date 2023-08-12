from django.contrib.auth import get_user_model
from django.db import models
from mall_app.users.models import UserProfile


# Defines a cinema hall with a name and seating capacity
class CinemaHall(models.Model):
    hall_name = models.CharField(max_length=255)
    capacity = models.IntegerField()

    class Meta:
        verbose_name_plural = "Halls"

    def __str__(self):
        return self.hall_name


# Defines a movie with its name, type, duration, and associated cinema halls
class Movie(models.Model):
    movie_name = models.CharField(max_length=255)
    movie_type = models.CharField(max_length=255)
    duration = models.DurationField()
    halls = models.ManyToManyField(CinemaHall)
    image = models.ImageField(upload_to='movies/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Movies"

    def __str__(self):
        return self.movie_name


# Defines the schedule for a particular movie in a cinema hall
class Schedule(models.Model):
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Schedules"

    def __str__(self):
        return f"{self.movie.movie_name} in {self.hall.hall_name} at {self.show_time}"


# Defines the seats in a cinema hall
class HallSeat(models.Model):
    User = get_user_model()
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE)
    row = models.PositiveIntegerField()
    column = models.PositiveIntegerField()
    taken = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ['row', 'column','hall']

    def __str__(self):
        return f'Hall {self.hall_id}, Row {self.row}, Column {self.column}'


# Defines a ticket purchased by a customer for a particular screening
class Ticket(models.Model):
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    seat = models.ForeignKey(HallSeat, on_delete=models.CASCADE)
    screening = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Tickets"

    def __str__(self):
        return f"Ticket {self.id} for {self.customer.user.email}"
