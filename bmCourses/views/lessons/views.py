from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, CreateView

from bmCourses.forms import AddLessonForm
from bmCourses.models import Lesson
from bmCourses.utils import DataMixin

from bmCourses.models import Course


class AddLesson(DataMixin, CreateView):
    form_class = AddLessonForm
    template_name = 'bmCourses/lessons/add_lesson.html'
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление урока', course=get_object_or_404(Course, slug=self.kwargs['course_slug']))
        return context | c_def

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        course_slug = self.kwargs['course_slug']
        kwargs['course'] = get_object_or_404(Course, slug=course_slug)
        return kwargs

class ShowLesson(DataMixin, DetailView):
    model = Lesson
    template_name = 'bmCourses/lessons/lesson.html'
    slug_url_kwarg = 'lesson_slug'
    context_object_name = 'lesson'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['lesson'], course=Course.objects.get(pk=context['lesson'].course_id))
        return context | c_def