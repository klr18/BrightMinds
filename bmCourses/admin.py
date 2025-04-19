from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}
    fields = ('title', 'slug', 'cat', 'description', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    save_on_top = True

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = 'Миниатюра'

class LessonAdmin(admin.ModelAdmin):
    fields = ('name', 'slug', 'course', 'description', 'content', 'video', 'is_published', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

class FeedBackAdmin(admin.ModelAdmin):
    fields = ('topic', 'content', 'user')

class SubscriptionAdmin(admin.ModelAdmin):
    fields = ('user', 'course', 'subscribed_at')
    readonly_fields = ('subscribed_at',)

class TestAdmin(admin.ModelAdmin):
    fields = ('course', 'title', 'description', 'time_create')
    readonly_fields = ('time_create',)

class QuestionAdmin(admin.ModelAdmin):
    fields = ('test', 'text', 'order')

class AnswerAdmin(admin.ModelAdmin):
    fields = ('question', 'text', 'is_correct')

class UserTestResultAdmin(admin.ModelAdmin):
    fields = ('user', 'test', 'score', 'completed_at')
    readonly_fields = ('completed_at',)

admin.site.register(Course, CourseAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(FeedBack, FeedBackAdmin)

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(UserTestResult, UserTestResultAdmin)

admin.site.site_title = 'Админ-панель'
admin.site.site_header = 'Админ-панель'