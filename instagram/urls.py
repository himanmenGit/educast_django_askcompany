from django.urls import path, re_path, register_converter

from . import views


class YearConverter:
    regex = r"20\d{2}"

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)


register_converter(YearConverter, "year")

app_name = "instagram"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("<int:pk>/", views.post_detail, name="post_detail"),
    # path("archives/<int:year>/", views.archives_year),
    # re_path("archives/(?P<year>20\d{2})/", views.archives_year),
    path("archives/<year:year>/", views.archives_year),
]
