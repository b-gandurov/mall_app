import random

from django.contrib import messages
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Parking, ParkingRate
from django.views import View
from django.shortcuts import render, redirect
from .models import CustomerCar
from .forms import CustomerCarForm, CarEntryForm, LicensePlateForm
from django.views.generic.edit import FormView, DeleteView


class ParkingView(generic.TemplateView):
    template_name = 'parking_templates/parking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lookup_form = LicensePlateForm()
        context['lookup_form'] = lookup_form

        if self.request.user.is_authenticated:
            current_user = self.request.user
            parked_car = Parking.objects.filter(customer_car__customer=current_user.userprofile,
                                                exit_date__isnull=True
                                                ).first()
            context['parked_car'] = parked_car
            context['registered_cars'] = CustomerCar.objects.filter(
                customer=current_user.userprofile)
        else:
            license_plate = self.request.GET.get('license_plate')
            if license_plate:
                parking_instance = Parking.objects.filter(
                    license_plate=license_plate,
                    exit_date__isnull=True
                ).first()

                if parking_instance:
                    if parking_instance.customer_car:
                        context['error_message'] = 'This car is registered to another user.'
                    else:
                        entry_time = parking_instance.entrance_date
                        amount_to_pay = parking_instance.amount_to_pay()
                        formatted_entry_time = entry_time.strftime("%H:%M:%S / %d-%m-%Y")
                        time_parked = timezone.now() - entry_time
                        hours_parked = time_parked.total_seconds() // 3600
                        context[
                            'parking_message'] = f'This car has been parked for {hours_parked} hours (since {formatted_entry_time})' \
                                                 f'\nThe total parking cost for this car is: {amount_to_pay}.'
                else:
                    context['error_message'] = 'Invalid license plate.'

        return context


class RegisterCarView(FormView):
    template_name = 'parking_templates/register_car.html'
    form_class = CustomerCarForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['code']
            parking_instance = Parking.objects.filter(
                non_registered_code=entered_code,
                exit_date__isnull=True
            ).first()

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
    template_name = 'parking_templates/car_entry.html'
    form_class = CarEntryForm
    success_url = '/parking/enter'

    def form_valid(self, form):
        license_plate = form.cleaned_data['license_plate']
        if Parking.objects.filter(license_plate=license_plate, exit_date__isnull=True).exists():
            form.add_error(None, 'This car is already parked.')
            return self.form_invalid(form)

        if Parking.objects.filter(exit_date__isnull=True).count() >= 400:
            form.add_error(None, 'Parking lot is full.')
            return self.form_invalid(form)

        try:
            car = CustomerCar.objects.get(license_plate=license_plate)
            welcome_message = f"Welcome {car.customer.user.get_username()}!"
            messages.success(self.request, welcome_message)
            Parking.objects.create(license_plate=license_plate, customer_car=car)

        except CustomerCar.DoesNotExist:
            code = random.randint(100000000000, 999999999999)
            messages.success(self.request, f"Your car is not registered. Here is your 12-digit code: {code}.\n You can register your car from your profile")
            Parking.objects.create(license_plate=license_plate, non_registered_code=code)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['free_spots'] = 400 - Parking.objects.filter(exit_date__isnull=True).count()
        return context


def get(request):
    return render(request, 'parking_templates/car_exit.html')


class CarExitView(View):

    def get(self, request):
        return render(request, 'parking_templates/car_exit.html')

    def post(self, request):
        license_plate = request.POST.get('license_plate')
        parking_instance = Parking.objects.filter(license_plate=license_plate, exit_date__isnull=True).first()

        if parking_instance:
            parking_rate = ParkingRate.objects.first()
            total_hours = (timezone.now() - parking_instance.entrance_date).total_seconds() / 3600
            payable_hours = int(max(total_hours - parking_rate.free_hours, 0))
            fee = payable_hours * parking_rate.hourly_rate
            parking_instance.fee = fee
            parking_instance.exit_date = timezone.now()
            parking_instance.save()
            context = {
                'error_message': f"Car with license-plate {license_plate} has exited the parkinglot.It has been parked for {total_hours:.2f} and the total parking cost was {fee}"
            }
        else:
            context = {
                'error_message': f"No car with license plate {license_plate} is currently parked."
            }
        return render(request, 'parking_templates/car_exit.html', context)


class DeleteCarView(DeleteView):
    model = CustomerCar
    template_name = 'parking_templates/confirm_delete_car.html'
    success_url = '/parking'
