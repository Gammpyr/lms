from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.test import APIClient, APITestCase

from lms.models import Course, Lesson
from users.models import CustomUser


class CourseAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username="test1", email="test1@test.ru", password="test1"
        )

        self.course1 = Course.objects.create(
            name="test_course1", description="test_desc1", owner=self.user1
        )
        self.course2 = Course.objects.create(
            name="test_course2", description="test_desc2", owner=self.user1
        )

        self.client = APIClient()

        # # Аутентифицируем пользователя
        # self.client.force_authenticate(user=self.user2)
        #
        # # Отправляем запрос на подписку
        # response = self.client.post(
        #     '/subscription/',
        #     {'course_id': self.course.id},
        #     format='json'
        # )
        #
        # # Проверяем результат
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['message'], 'Подписка добавлена')
        # self.assertTrue(response.data['subscribed'])
        #
        # # Проверяем, что подписка создалась в БД
        # self.assertTrue(
        #     CourseSubscription.objects.filter(
        #         user=self.user2,
        #         course=self.course
        #     ).exists()
        # )

    def test_get_list_courses(self):
        """
        Проверка получения списка курсов
        """
        self.client.force_authenticate(user=self.user1)

        response = self.client.get("/courses/")

        self.assertEqual(response.status_code, HTTP_200_OK)

        results = response.json()["results"]
        course1 = results[0]
        course2 = results[1]

        self.assertEqual(course1["description"], "test_desc1")
        self.assertEqual(course1["image"], None)
        self.assertEqual(course1["is_subscribed"], False)
        self.assertEqual(course1["lesson_count"], 0)
        self.assertEqual(course1["name"], "test_course1")
        self.assertEqual(course1["owner"], self.user1.id)
        self.assertEqual(course1["video_url"], None)

        self.assertEqual(course2["description"], "test_desc2")
        self.assertEqual(course2["image"], None)
        self.assertEqual(course2["is_subscribed"], False)
        self.assertEqual(course2["lesson_count"], 0)
        self.assertEqual(course2["name"], "test_course2")
        self.assertEqual(course2["owner"], self.user1.id)
        self.assertEqual(course2["video_url"], None)

        # self.assertEqual(
        #     results,
        #     [
        #         {'description': 'test_desc1',
        #          'id': 3,
        #          'image': None,
        #          'is_subscribed': False,
        #          'lesson_count': 0,
        #          'name': 'test_course1',
        #          'owner': 3,
        #          'video_url': None},
        #         {'description': 'test_desc2',
        #          'id': 4,
        #          'image': None,
        #          'is_subscribed': False,
        #          'lesson_count': 0,
        #          'name': 'test_course2',
        #          'owner': 3,
        #          'video_url': None}]
        #
        # )

    def test_delete_course(self):
        """
        Проверка удаления курса
        """
        self.client.force_authenticate(user=self.user1)

        response = self.client.delete(f"/courses/{self.course2.id}/")

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    def test_get_course(self):
        """
        Проверка получения курса
        """
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(f"/courses/{self.course1.id}/")

        self.assertEqual(response.status_code, HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "description": "test_desc1",
                "id": self.course1.id,
                "image": None,
                "is_subscribed": False,
                "lesson_count": 0,
                "lessons": [],
                "name": "test_course1",
                "notification_task_id": None,
                "owner": self.user1.id,
                "video_url": None,
            },
        )

    def test_put_course(self):
        """
        Проверка изменения курса
        """
        self.client.force_authenticate(user=self.user1)

        data = {
            "name": "test_course1",
            "description": "test_desc3",
            "owner": self.user1.id,
        }

        response = self.client.put(f"/courses/{self.course1.id}/", data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        self.assertEqual(response.json()["description"], "test_desc3")


class LessonAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username="test1", email="test1@test.ru", password="test1"
        )

        self.course1 = Course.objects.create(
            name="test_course1", description="test_desc1", owner=self.user1
        )

        self.lesson1 = Lesson.objects.create(
            name="test_lesson1",
            description="test_desc1",
            owner=self.user1,
            course=self.course1,
        )
        self.lesson2 = Lesson.objects.create(
            name="test_lesson2",
            description="test_desc2",
            owner=self.user1,
            course=self.course1,
        )

        self.client = APIClient()

    def test_get_list_lessons(self):
        """
        Проверка получения списка уроков
        """
        self.client.force_authenticate(user=self.user1)

        response = self.client.get("/lessons/")

        self.assertEqual(response.status_code, HTTP_200_OK)

        results = response.json()["results"]
        lesson1 = results[0]
        lesson2 = results[1]

        self.assertEqual(lesson1["description"], "test_desc1")
        self.assertEqual(lesson1["image"], None)
        self.assertEqual(lesson1["name"], "test_lesson1")
        self.assertEqual(lesson1["owner"], self.user1.id)
        self.assertEqual(lesson1["course"], self.course1.id)

        self.assertEqual(lesson2["description"], "test_desc2")
        self.assertEqual(lesson2["image"], None)
        self.assertEqual(lesson2["name"], "test_lesson2")
        self.assertEqual(lesson2["owner"], self.user1.id)
        self.assertEqual(lesson2["course"], self.course1.id)

    def test_delete_lesson(self):
        """
        Проверка удаления урока
        """
        self.client.force_authenticate(user=self.user1)

        response = self.client.delete(f"/lessons/delete/{self.lesson2.id}/")

        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    def test_get_lesson(self):
        """
        Проверка получения урока
        """
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(f"/lessons/{self.lesson1.id}/")

        self.assertEqual(response.status_code, HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "id": self.lesson1.id,
                "name": "test_lesson1",
                "image": None,
                "description": "test_desc1",
                "owner": self.user1.id,
                "course": self.course1.id,
            },
        )

    def test_put_lesson(self):
        """
        Проверка изменения урока
        """
        self.client.force_authenticate(user=self.user1)

        data = {
            "name": "test_course1",
            "description": "test_lesson_desc1",
            "owner": self.user1.id,
            "course": self.course1.id,
        }

        response = self.client.put(f"/courses/{self.course1.id}/", data)

        self.assertEqual(response.status_code, HTTP_200_OK)

        self.assertEqual(response.json()["description"], "test_lesson_desc1")


class CourseSubscriptionAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username="test1", email="test1@test.ru", password="test1"
        )

        self.course1 = Course.objects.create(
            name="test_course1", description="test_desc1", owner=self.user1
        )

        self.client = APIClient()

    def test_subscribe_course(self):
        self.client.force_authenticate(user=self.user1)

        data = {"course_id": self.course1.id}

        response = self.client.post("/subscription/", data)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена")
