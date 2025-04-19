from django.urls import path
from django.views.decorators.cache import cache_page

from bmCourses.views import *

urlpatterns = [
    path('', CourseHome.as_view(), name='home'),
    path('about/', About.as_view(), name='about'),
    path('add_course/', AddCourse.as_view(), name='add_course'),
    path('add_lesson/<slug:course_slug>', AddLesson.as_view(), name='add_lesson'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('course/<slug:course_slug>', ShowCourse.as_view(), name='course'),
    path('lesson/<slug:lesson_slug>', ShowLesson.as_view(), name='lesson'),
    path('category/<slug:cat_slug>', CourseCategory.as_view(), name='category'),

    path('profile/<str:username>', Profile.as_view(), name='profile'),
    path('course/<slug:course_slug>/subscribe/', SubscriptionView.as_view(), name='subscription'),

    path('course/<slug:course_slug>/test/create/', AddTest.as_view(), name='test_create'),
    path('test/<int:test_id>/question/create/', AddQuestion.as_view(), name='question_create'),
    path('question/<int:question_id>/answer/create/', AddAnswer.as_view(), name='answer_create'),
    path('test/<int:pk>/', TestDetailView.as_view(), name='test_detail'),
    path('test/<int:pk>/result/', TestResultView.as_view(), name='test_result'),
]