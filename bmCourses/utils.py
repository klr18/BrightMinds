from django.db.models import Count, Q
from django.core.cache import cache

from .models import *

menu = [{'title': 'О сайте', 'url_name': 'about'},
            {'title': 'Добавить курс', 'url_name': 'add_course'},
            {'title': 'Обратная связь', 'url_name': 'contact'},
            ]

class DataMixin:
    paginate_by = 12
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.all().annotate(total=Count('course', filter=Q(course__is_published=True))).filter(total__gt=0)
            cache.set('cats', cats, 60)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0

        return context