from django.urls import path
from .views import create_robot, robots_report_page, generate_report

urlpatterns = [
    path('api/robots/', create_robot, name='create_robot'),
    path('reports/', robots_report_page, name='robots_report_page'),
    path('reports/download/', generate_report, name='generate_report'),
]
