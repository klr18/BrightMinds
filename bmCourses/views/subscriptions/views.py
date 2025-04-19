from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from bmCourses.models import Course, Subscription


class SubscriptionView(LoginRequiredMixin, View):
    def post(self, request, course_slug):
        course = get_object_or_404(Course, slug=course_slug)
        subscription, created = Subscription.objects.get_or_create(
            user=request.user,
            course=course
        )
        if not created:
            subscription.delete()
            return JsonResponse({'status': 'unsubscribed'})
        return JsonResponse({'status': 'subscribed'})