from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, DetailView

from bmCourses.forms import AddCourseForm
from bmCourses.models import Course, Lesson, Test, Subscription, Category
from bmCourses.utils import DataMixin


class CourseCategory(DataMixin, ListView):
    model = Course
    template_name = 'bmCourses/courses/course_list.html'
    context_object_name = 'courses'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title=str(c.name), cat_selected=c.pk)
        return context | c_def

    def get_queryset(self):
        return Course.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

class ShowCourse(DataMixin, DetailView):
    model = Course
    template_name = 'bmCourses/courses/course.html'
    slug_url_kwarg = 'course_slug'
    context_object_name = 'course'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_subscribed'] = Subscription.objects.filter(
                user=self.request.user,
                course=self.object
            ).exists()
        c_def = self.get_user_context(title=context['course'],
                                      cat_selected=context['course'].cat_id,
                                      lessons=Lesson.objects.filter(course_id=context['course'].pk),
                                      tests=Test.objects.filter(course_id=context['course'].pk),
                                      subscribers=User.objects.filter(subscription__course=self.object),
                                      user=User.objects.get(pk=context['course'].user_id))

        return context | c_def

class AddCourse(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddCourseForm
    template_name = 'bmCourses/courses/add_course.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление курса')
        return context | c_def

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class CourseHome(DataMixin, ListView):
    model = Course
    template_name = 'bmCourses/courses/course_list.html'
    context_object_name = 'courses'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return context | c_def

    def get_queryset(self):
        return Course.objects.filter(is_published=True).select_related('cat')

class About(DataMixin, TemplateView):
    template_name = 'bmCourses/support/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О сайте')
        return context | c_def