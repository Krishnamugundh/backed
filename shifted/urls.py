from django.urls import path
from . import views

urlpatterns = [
    path("homei/", views.home , name="home"),
    path("login/", views.login_patient, name="login"),
    path("register/", views.register_user, name="register"),
    path("logout/", views.logout_patient, name="logging_out"),
    path("menu_page/", views.new_page, name="new_page"),
    path("recipe_name/", views.recipe_name, name = "recipe"),
    path("description/<str:pk>", views.recipe_desc, name = "detail"),
    path("NewRecipes/", views.post_recipes, name = "create"),
    path("update_recipe/<str:pk>/", views.update_recipes, name = 'update_recipe'),
    path("delete/<uuid:pk>", views.delete_recipe, name = "deleteRec"),
    path('create/', views.updateORcreate_patient, name='create_patient'),
    path("update_patient_properties", views.patient_prop, name="update_patient_properties"),
    path('patient/profile', views.patient_detail, name='patient_detail'),
    path("audio_record/<uuid:ids>", views.audio_in, name="upload_audio_record"),
    path("audio_record/predict/<uuid:pp_ids>/<uuid:audio_id>", views.prediction, name = "predict"),
]