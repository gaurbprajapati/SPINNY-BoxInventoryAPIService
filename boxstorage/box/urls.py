from django.urls import path
from .views import BoxListCreateView, BoxRetrieveUpdateDeleteView, MyBoxListView, FilteredBoxListView, BoxDetailView

urlpatterns = [
    path('boxes/', BoxListCreateView.as_view(), name='box-list-create'),
    path('boxes/<int:pk>/', BoxRetrieveUpdateDeleteView.as_view(), name='box-detail'),
    path('my-boxes/', MyBoxListView.as_view(), name='my-box-list'),
    path('filtered-boxes/', FilteredBoxListView.as_view(),
         name='filtered-box-list'),
    path('boxdel/<int:pk>', BoxDetailView.as_view(),
         name='boxdel'),
]
