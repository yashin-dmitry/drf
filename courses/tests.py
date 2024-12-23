from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Subscription

User = get_user_model()

class CourseTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com',
                                             password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='Test Course',
                                            description='Test Description',
                                            owner=self.user)
        self.lesson = Lesson.objects.create(name='Test Lesson',
                                            description='Test Description',
                                            video_url='https://www.youtube.com'
                                                      '/watch?v=dQw4w9WgXcQ',
                                            course=self.course, owner=self.user)

    def test_create_course(self):
        url = reverse('course-list')
        data = {'name': 'New Course', 'description': 'New Description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(Course.objects.get(id=response.data['id']).name,
                         'New Course')

    def test_create_lesson(self):
        url = reverse('lesson-list-create')
        data = {'name': 'New Lesson', 'description': 'New Description',
                'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'course': self.course.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(Lesson.objects.get(id=response.data['id']).name,
                         'New Lesson')

    def test_subscription(self):
        url = reverse('subscription')
        data = {'course_id': self.course.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertEqual(Subscription.objects.count(), 1)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertEqual(Subscription.objects.count(), 0)
