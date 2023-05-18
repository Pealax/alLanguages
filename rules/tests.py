from django.urls import reverse
from rest_framework.test import APIClient, APITestCase, APIRequestFactory
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from language.models import Language
from .models import *
from .views import *


class ListCreateCheckTestCase(APITestCase):

    def setUp(self):
        self.language = Language.objects.create(code=1, title="en", original="en")
        self.username = 'testuser@example.com'
        self.password = 'testpassword'
        self.user = User.objects.create_user(self.username, self.password, 
                    native=self.language, learn=self.language, is_active=True )
        self.token = str(AccessToken.for_user(self.user))

    def test_question_set(self):
        client = APIClient()
        url = '/api/rules/my/'
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        print(self.language.title)
        print(self.user)
        print('---')
        question = Question.objects.create(
            question="Вопрос", status='PR', user_id=1, native_id=1, learn_id=1)

    def test_question_check(self):
        client = APIClient()
        factory = APIRequestFactory()
        url = reverse('check-question')
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        user=self.user
        view = UserQuestionsCheck.as_view()
        print(self.language.title)
        print(user)
        print(url)
        user2 = User.objects.create_user(email='second@example.com', password='two', 
                    native=self.language, learn=self.language, is_active=True )
        question = Question.objects.create(
            question="Вопрос", status='PR', user=user2, native_id=1, learn_id=1)
        chek = Check.objects.create( flag=True, comment="text1", 
                                    question=question, user=user)
        print(question.user)
        print(chek.user)
        request = factory.get(url)
        #response = client.get(url)
        #assert response.status_code == 200
        #response = view(request)
        print(request)
