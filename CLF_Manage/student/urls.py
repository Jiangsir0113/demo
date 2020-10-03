from django.conf.urls import url
from student import views

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^login/', views.login),
    url(r'^register/', views.register),
    url(r'^student/', views.student),
    url(r'^update/', views.update),
    url(r'^delete/(\d+)', views.delete),
    url(r'^delete2/', views.delete2),
    url(r'^pwd_change/(\w+)', views.pwd_change),
    url(r'^add_student/', views.add_student),
    url(r'^select_user/(\w+)', views.select_user),
    url(r'^logout/', views.logout),
    url(r'^get_valid_img/', views.get_valid_img),

    url(r'^index1/', views.index1, name='index11')
]
