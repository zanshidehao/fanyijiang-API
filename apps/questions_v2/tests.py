from django.test import TestCase
from django.urls import reverse

from apps import common_prepare
from apps.labels_v2.models import Label
from apps.questions_v2.models import Question


class QuestionViewPostTest(TestCase):
    def setUp(self):
        common_prepare(self)
        self.label1 = Label.objects.create(name="标签1")
        self.label2 = Label.objects.create(name="标签2")
        self.path = reverse("questions_v2:root")
        self.data = {"title": "问题标题", "content": "进一步描述", "labels": [self.label1.pk, self.label2.pk]}

    def test_no_login(self):
        response = self.client.post(self.path, self.data)
        data = response.json()
        self.assertNotEqual(data["code"], 0)

    def test_title_exist(self):
        self.assertEqual(Question.objects.count(), 0)
        self.client.post(self.path, self.data, **self.headers)
        self.assertEqual(Question.objects.count(), 1)
        data = self.data.copy()
        data["content"] = "不同的内容"
        response = self.client.post(self.path, data, **self.headers)
        data = response.json()
        self.assertNotEqual(data["code"], 0)
        self.assertEqual(Question.objects.count(), 1)

    def test_no_label(self):
        data = self.data.copy()
        data["labels"] = [self.label1.pk + self.label2.pk]
        self.assertEqual(Question.objects.count(), 0)
        response = self.client.post(self.path, data, **self.headers)
        data = response.json()
        self.assertNotEqual(data["code"], 0)
        self.assertEqual(Question.objects.count(), 0)


class OneQuestionViewPutTest(TestCase):
    def setUp(self):
        common_prepare(self)
        self.label1 = Label.objects.create(name="标签1")
        self.label2 = Label.objects.create(name="标签2")
        self.question = Question.objects.create(title="问题1", content="内容1", author=self.users["zhang"])
        self.question.labels.add(self.label1)
        self.data = {"title": "问题标题", "content": "进一步描述", "labels": [self.label1.pk, self.label2.pk]}
        self.path = reverse("questions_v2:one_question", kwargs={"question_id": self.question.pk})

    def test_no_login(self):
        response = self.client.put(self.path, self.data)
        data = response.json()
        self.assertNotEqual(data["code"], 0)

    def test_question_not_exist(self):
        path = reverse("questions_v2:one_question", kwargs={"question_id": self.question.pk + 1})
        response = self.client.put(path, self.data, **self.headers)
        data = response.json()
        self.assertNotEqual(data["code"], 0)

    def test_not_author(self):
        question = Question.objects.create(title="问题2", content="内容2", author=self.users["zhao"])
        question.labels.add(self.label2)
        self.assertEqual(Question.objects.count(), 2)
        path = reverse("questions_v2:one_question", kwargs={"question_id": question.pk})
        response = self.client.put(path, self.data, **self.headers)
        data = response.json()
        self.assertNotEqual(data["code"], 0)

    def test_no_label(self):
        data = self.data.copy()
        data["labels"] = [self.label1.pk + self.label2.pk]
        response = self.client.put(self.path, data, **self.headers)
        data = response.json()
        self.assertNotEqual(data["code"], 0)
        self.assertEqual(self.question.labels.count(), 1)

    def test_title_unchanged(self):
        data = self.data.copy()
        data["title"] = self.question.title
        response = self.client.put(self.path, data, **self.headers)
        data = response.json()
        self.assertEqual(data["code"], 0)
