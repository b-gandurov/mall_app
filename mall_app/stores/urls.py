# mall_app/stores/urls.py

from django.urls import path

from mall_app.stores.views import *

urlpatterns = (
    path('', StoreListView.as_view(), name='store_list'),
    path('<int:pk>/', StoreDetailView.as_view(), name='store_detail'),
    path('items/<int:item_id>/', ItemDetailView.as_view(), name='item_detail'),
    path('items/<int:item_id>/reserve/', reserve_item, name='reserve_item'),
)
