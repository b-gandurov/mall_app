# mall_app/stores/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic as views
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import StoreSearchForm
from .models import Store, Item, Reservation


class StoreListView(views.ListView):
    model = Store
    template_name = 'store_templates/store_list.html'
    context_object_name = 'stores'

    def get_queryset(self):
        queryset = super().get_queryset()
        form = StoreSearchForm(self.request.GET)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']
            category = form.cleaned_data['category']
            if search_term:
                queryset = queryset.filter(name__icontains=search_term)
            if category:
                queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = StoreSearchForm(self.request.GET)
        return context


class StoreDetailView(views.DetailView):
    model = Store
    template_name = 'store_templates/store_detail.html'
    context_object_name = 'store'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Item.objects.filter(store=self.object)
        return context


@login_required
def reserve_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if item.available_for_reservation and item.quantity > 0:
        Reservation.objects.create(item=item, user=request.user)
        item.quantity -= 1
        item.save()
    return redirect('store_detail', pk=item.store.id)


class ItemDetailView(views.DetailView):
    model = Item
    template_name = 'store_templates/item_detail.html'
