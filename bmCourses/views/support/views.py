from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from bmCourses.forms import ContactForm
from bmCourses.utils import DataMixin


class About(DataMixin, TemplateView):
    template_name = 'bmCourses/support/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О сайте')
        return context | c_def

class ContactFormView(DataMixin, CreateView):
    form_class = ContactForm
    template_name = 'bmCourses/support/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return context | c_def

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs