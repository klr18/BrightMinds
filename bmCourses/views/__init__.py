from .auth.views import RegisterUser, LoginUser, logout_user
from .courses.views import CourseHome, AddCourse, ShowCourse, CourseCategory
from .lessons.views import ShowLesson, AddLesson
from .tests.views import (AddTest, AddQuestion, AddAnswer,
                        TestDetailView, TestResultView)
from .subscriptions.views import SubscriptionView
from .support.views import About, ContactFormView
from .user.views import Profile

__all__ = [
    'RegisterUser', 'LoginUser', 'logout_user',
    'CourseHome', 'AddCourse', 'ShowCourse', 'CourseCategory',
    'ShowLesson', 'AddLesson',
    'AddTest', 'AddQuestion', 'AddAnswer',
    'TestDetailView', 'TestResultView', 'SubscriptionView',
    'About', 'ContactFormView',
    'Profile'
]