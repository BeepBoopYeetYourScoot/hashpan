from django.urls import path

from hashpan_checker.views import HashpanView

urlpatterns = [
    path(
        "main/",
        HashpanView.as_view(template_name="card_orders.html"),
        name="hashpan_view",
    ),
]
