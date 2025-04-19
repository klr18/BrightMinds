from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from bmCourses.forms import TestForm, QuestionForm, AnswerForm
from bmCourses.models import Test, Course, Question, Answer, UserTestResult
from bmCourses.utils import DataMixin


class AddTest(DataMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Test
    form_class = TestForm
    template_name = 'bmCourses/tests/add_test.html'
    slug_url_kwarg = 'course_slug'

    def test_func(self):
        course = get_object_or_404(Course, slug=self.kwargs['course_slug'])
        return self.request.user == course.user

    def form_valid(self, form):
        course = get_object_or_404(Course, slug=self.kwargs['course_slug'])
        form.instance.course = course
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('question_create', kwargs={'test_id': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, slug=self.kwargs['course_slug'])
        context['course'] = course
        return {**context, **self.get_user_context(title='Добавление теста')}


class AddQuestion(DataMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'bmCourses/tests/add_question.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.test = get_object_or_404(Test, pk=self.kwargs['test_id'])

    def test_func(self):
        return self.request.user == self.test.course.user

    def form_valid(self, form):
        form.instance.test = self.test
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test'] = self.test
        return {**context, **self.get_user_context(title='Добавление вопроса')}

    def get_success_url(self):
        return reverse('answer_create', kwargs={'question_id': self.object.pk})


class AddAnswer(DataMixin, LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'bmCourses/tests/add_answer.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.question = get_object_or_404(Question, pk=self.kwargs['question_id'])
        self.test = self.question.test

    def test_func(self):
        return self.request.user == self.test.course.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['question'] = self.question
        return kwargs

    def form_valid(self, form):
        form.instance.question = self.question

        if self.question.type == 'TI':
            form.instance.is_correct = True

        response = super().form_valid(form)

        if 'add_question' in self.request.POST:
            return redirect('question_create', test_id=self.test.pk)
        elif 'finish' in self.request.POST:
            return redirect('course', course_slug=self.test.course.slug)

        return response

    def get_success_url(self):
        return reverse('answer_create', kwargs={'question_id': self.question.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context, **self.get_user_context(
            title='Добавление ответа',
            type=self.question.type,
            question=self.question,
            test=self.test
        )}


class TestDetailView(DataMixin, LoginRequiredMixin, DetailView):
    model = Test
    template_name = 'bmCourses/tests/test_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f'Прохождение теста "{self.get_object().title}"')
        return context | c_def

    def dispatch(self, request, *args, **kwargs):
        self.test = self.get_object()

        user_attempts = UserTestResult.objects.filter(user=request.user, test=self.test).count()
        if self.test.attempts is not None and user_attempts >= self.test.attempts:
            return HttpResponseForbidden("Вы исчерпали все попытки прохождения этого теста.")

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        test = self.get_object()
        score = 0
        selected_ids = []
        user_inputs = {}

        for question in test.questions.all():
            field_name = f'question_{question.id}'
            if question.type == 'SC':  # одиночный выбор
                ans_id = request.POST.get(field_name)
                if ans_id:
                    answer = get_object_or_404(Answer, id=ans_id)
                    selected_ids.append(answer.id)
                    if answer.is_correct:
                        score += 1

            elif question.type == 'MC':  # множественный выбор
                ans_list = request.POST.getlist(field_name)
                correct_ids = list(
                    question.answers.filter(is_correct=True).values_list('id', flat=True)
                )
                int_ids = [int(a) for a in ans_list]
                selected_ids.extend(int_ids)
                if set(int_ids) == set(correct_ids):
                    score += 1

            elif question.type == 'TI':  # ввод вручную
                text = request.POST.get(field_name, '').strip()
                user_inputs[str(question.id)] = text
                correct = question.answers.filter(is_correct=True).first()
                if correct and correct.text.strip().lower() == text.lower():
                    score += 1
                # добавляем правильный ответ в selected для вывода
                if correct:
                    selected_ids.append(correct.id)

        result = UserTestResult.objects.create(
            user=request.user,
            test=test,
            score=score,
            user_inputs=user_inputs
        )
        result.selected_answers.set(selected_ids)
        return redirect('test_result', pk=result.id)

class TestResultView(DataMixin, LoginRequiredMixin, DetailView):
    model = UserTestResult
    template_name = 'bmCourses/tests/test_result.html'
    context_object_name = 'result'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        result = self.object
        test = result.test

        breakdowns = []
        for question in test.questions.all():
            correct_answers = question.answers.filter(is_correct=True)
            user_selected = result.selected_answers.filter(question=question)
            user_input = (result.user_inputs or {}).get(str(question.id))

            breakdowns.append({
                'question': question,
                'correct': correct_answers,
                'user_selected': user_selected,
                'user_input': user_input,
            })

        context.update({
            'breakdowns': breakdowns,
            'total_questions': test.questions.count(),
            'percent_correct': round((result.score / test.questions.count()) * 100) if test.questions.count() else 0,
            'title': f'Результаты теста "{test.title}"',
            'test': test,
        })
        return {**context, **self.get_user_context()}