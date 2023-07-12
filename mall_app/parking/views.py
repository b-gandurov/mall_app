from django.shortcuts import render
from django.urls import reverse
from django.views import View, generic
from django.utils import timezone
from .models import Parking
from django.views import View
from django.shortcuts import render, redirect
from .models import CustomerCar
from .forms import CustomerCarForm, CarEntryForm


class ParkingView(generic.TemplateView):
    template_name = 'parking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user

        if hasattr(current_user, 'userprofile'):
            parked_car = Parking.objects.filter(license_plate__customer=current_user.userprofile,
                                                exit_date__isnull=True).first()
            context['parked_car'] = parked_car
            context['registered_cars'] = CustomerCar.objects.filter(customer=current_user.userprofile)

        context['free_spots'] = 400 - Parking.objects.filter(exit_date__isnull=True).count()

        return context


# views.py


class RegisterCarView(View):
    template_name = 'register_car.html'
    form_class = CustomerCarForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_car = form.save(commit=False)
            new_car.customer = request.user.userprofile
            new_car.save()
            return redirect('parking')
        return render(request, self.template_name, {'form': form})


from django.views.generic.edit import FormView


class CarEntryView(FormView):
    template_name = 'car_entry.html'
    form_class = CarEntryForm
    success_url = '/parking'

    def form_valid(self, form):
        license_plate = form.cleaned_data['license_plate']

        # Check if the car is already parked.
        if Parking.objects.filter(license_plate__license_plate=license_plate, exit_date__isnull=True).exists():
            form.add_error(None, 'This car is already parked.')
            return self.form_invalid(form)

        # Check if there's available parking space.
        if Parking.objects.filter(exit_date__isnull=True).count() >= 400:
            form.add_error(None, 'Parking lot is full.')
            return self.form_invalid(form)

        # If the car is registered, link it.
        try:
            car = CustomerCar.objects.get(license_plate=license_plate)
        except CustomerCar.DoesNotExist:
            car = None

        Parking.objects.create(license_plate=car)
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
        parking_instance = Parking.objects.filter(license_plate__license_plate=license_plate,
                                                  exit_date__isnull=True).first()

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