from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse

class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to="[photos/%Y/%m/%d]", verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Пользователь')
    subscribers = models.ManyToManyField(
        User,
        related_name='subscribed_courses',
        blank=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course', kwargs={'course_slug': self.slug})

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-time_create', 'title']

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='Курс')
    subscribed_at = models.DateTimeField(auto_now=True, verbose_name='Время подписки')

    def __str__(self):
        return f'{self.user} на {self.course}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-subscribed_at']
        unique_together = ('user', 'course')

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Описание')
    content = models.TextField(blank=True, verbose_name='Контент')
    video = models.FileField(upload_to="[videos/%Y/%m/%d]", verbose_name='Видео', null=True, validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')
    course = models.ForeignKey('Course', on_delete=models.PROTECT, verbose_name='Курс')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('lesson', kwargs={'lesson_slug': self.slug})

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['id']

class FeedBack(models.Model):
    topic = models.CharField(max_length=50, verbose_name='Тема')
    content = models.TextField(blank=True, verbose_name='Контент')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
        ordering = ['id']

class Test(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='Курс')
    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    attempts = models.PositiveIntegerField(blank=True, null= True, verbose_name='Количество попыток')
    time_to_complete = models.PositiveIntegerField(blank=True, null=True, verbose_name='Ограничение по времени в минутах')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('test_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        ordering = ['time_create']

class Question(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE, related_name='questions', verbose_name='Тест')
    text = models.TextField(verbose_name='Вопрос')

    SINGLE_CHOICE = 'SC'
    MULTIPLE_CHOICE = 'MC'
    TEXT_INPUT = 'TI'

    QUESTION_TYPES = [
        (SINGLE_CHOICE, 'Один вариант ответа'),
        (MULTIPLE_CHOICE, 'Несколько вариантов ответа'),
        (TEXT_INPUT, 'Ввод ответа вручную'),
    ]

    type = models.CharField(
        max_length=2,
        choices=QUESTION_TYPES,
        default=SINGLE_CHOICE,
        verbose_name='Тип вопроса'
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

class Answer(models.Model):
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers', verbose_name='Вопрос')
    text = models.TextField(max_length=300, verbose_name='Ответ')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['id']

class UserTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Тест')
    score = models.PositiveIntegerField(verbose_name='Балл')
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name='Время прохождения')
    selected_answers = models.ManyToManyField('Answer', blank=True, verbose_name='Выбранные ответы')
    user_inputs = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} прошел {self.test.title} в {self.completed_at}'

    def get_absolute_url(self):
        return reverse('test_result', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Результат прохождения'
        verbose_name_plural = 'Результаты прохождения'
        ordering = ['-score']