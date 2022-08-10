from django.urls import path, include
from .views import TaskList, TaskDetail, TaskUpdate, TaskDelete, CustomLoginView, RegisterPage, \
    ProfileDetail, Statistics, TaskCreateViewSet, TaskCreate, TaskListViewSet, TaskUpdateViewSet, TaskDeleteViewSet, \
    ProfileUpdate
from django.contrib.auth.views import LogoutView
from rest_framework import routers

router = routers.SimpleRouter()
router.register('task_create_view', TaskCreateViewSet, basename='task_create_view')
router.register('task_list_view', TaskListViewSet, basename='task_list_view')
router.register('task_update_view', TaskUpdateViewSet, basename='task_update_view')
router.register('task_delete_view', TaskDeleteViewSet, basename='task_delete_view')

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task_create/', TaskCreate.as_view(), name='task_create'),
    path('statistics/', Statistics.as_view(), name='statistics'),
    path('profile/<int:pk>/', ProfileDetail.as_view(), name='profile'),
    path('profile_update/<int:pk>/', ProfileUpdate.as_view(), name='profile_update'),
    path('task_update/<int:pk>/', TaskUpdate.as_view(), name='task_update'),
    path('task_delete/<int:pk>/', TaskDelete.as_view(), name='task_delete'),
    path('', include(router.urls)),

]




