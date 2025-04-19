from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from bmCourses.models import Course, Subscription, UserTestResult
from bmCourses.utils import DataMixin


class Profile(DataMixin, DetailView):
    model = User
    template_name = 'bmCourses/user/profile.html'
    context_object_name = 'profile'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)

        test_results = UserTestResult.objects.filter(user=user).select_related('test').order_by('completed_at')[:10]

        performance_data = []
        for result in test_results:
            total_questions = result.test.questions.count()
            percent = round((result.score / total_questions) * 100) if total_questions else 0
            performance_data.append({
                'title': result.test.title,
                'percent': percent,
                'score': result.score,
                'total': total_questions,
                'date': result.completed_at,
            })

        context.update({
            'profile_user': user,
            'is_own_profile': (self.request.user == user),
            'courses': Course.objects.filter(is_published=True, user=user),
            'subscriptions': Subscription.objects.filter(user=user),
            'test_results': UserTestResult.objects.filter(user=user).order_by('-completed_at')[:10],
            'performance_data': performance_data,
        })

        c_def = self.get_user_context(title='Профиль')
        return context | c_def
