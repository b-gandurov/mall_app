import random

from django.contrib import messages
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Parking
from django.views import View
from django.shortcuts import render, redirect
from .models import CustomerCar
from .forms import CustomerCarForm, CarEntryForm
from django.views.generic.edit import FormView, UpdateView, DeleteView

class ParkingView(generic.TemplateView):
    template_name = 'parking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user

        if hasattr(current_user, 'userprofile'):
            parked_car = Parking.objects.filter(customer_car__customer=current_user.userprofile,
                                                exit_date__isnull=True).first() # changed line here
            context['parked_car'] = parked_car
            context['registered_cars'] = CustomerCar.objects.filter(customer=current_user.userprofile)

        context['free_spots'] = 400 - Parking.objects.filter(exit_date__isnull=True).count()

        return context


# views.py


class RegisterCarView(FormView):
    template_name = 'register_car.html'
    form_class = CustomerCarForm


    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['code']

            # Check if there is a parked car with the entered code
            parking_instance = Parking.objects.filter(non_registered_code=entered_code, exit_date__isnull=True).first()

            if not parking_instance:
                form.add_error('code', 'Invalid code. Please enter the correct 12-digit code.')
                return render(request, self.template_name, {'form': form})

            new_car = form.save(commit=False)
            new_car.customer = request.user.userprofile
            new_car.save()

            parking_instance.customer_car = new_car
            parking_instance.save()

            return redirect('parking')

        return render(request, self.template_name, {'form': form})






class CarEntryView(FormView):
    template_name = 'car_entry.html'
    form_class = CarEntryForm
    success_url = '/parking/enter'

    def form_valid(self, form):
        license_plate = form.cleaned_data['license_plate']
        # Check if the car is already parked.
        if Parking.objects.filter(customer_car__license_plate=license_plate, exit_date__isnull=True).exists():
            form.add_error(None, 'This car is already parked.')
            return self.form_invalid(form)

        # Check if there's available parking space.
        if Parking.objects.filter(exit_date__isnull=True).count() >= 400:
            form.add_error(None, 'Parking lot is full.')
            return self.form_invalid(form)

        # If the car is registered, link it.
        try:
            car = CustomerCar.objects.get(license_plate=license_plate)
            welcome_message = f"Welcome {car.customer.user.get_username()}!"
            messages.success(self.request, welcome_message)
            Parking.objects.create(license_plate=license_plate, customer_car=car)

        except CustomerCar.DoesNotExist:
            car = None
            code = random.randint(100000000000, 999999999999)  # Generate a random 12-digit code
            messages.success(self.request, f"Your car is not registered. Here is your 12-digit code: {code}")
            Parking.objects.create(license_plate=license_plate, non_registered_code=code)
            # Parking.objects.create(customer_car=car)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['free_spots'] = 400 - Parking.objects.filter(exit_date__isnull=True).count()
        return context


class CarExitView(View):
    def get(self, request):
        return render(request, 'car_exit.html')

    def post(self, request):
        license_plate = request.POST.get('license_plate')

        # Find the car in the parking lot
        parking_instance = Parking.objects.filter(license_plate=license_plate, exit_date__isnull=True).first()


        if parking_instance:
            # Car found in the parking lot. Mark it as exited.
            parking_instance.exit_date = timezone.now()
            parking_instance.save()
            return redirect(reverse('parking'))

        # If no matching car is found in the parking lot, return an error message.
        context = {
            'error_message': f"No car with license plate {license_plate} is currently parked."
        }
        return render(request, 'car_exit.html', context)

class DeleteCarView(DeleteView):
    model = CustomerCar
    template_name = 'confirm_delete_car.html'
    success_url = '/parking'