from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.test import APITestCase

from good_habits.models import Habits

from good_habits.views import (
    HabitListAPIView,
    HabitRetrieveAPIView,
    HabitDestroyAPIView,
    HabitUpdateAPIView,
)
from users.models import User


class HabitsTestCase(APITestCase):
    def setUp(self) -> None:
        """Общие данные"""

        self.user = User.objects.create(
            email="4@admin.ru", password="spartak67", is_active=True, is_superuser=True
        )
        self.user.save()
        self.client.force_authenticate(user=self.user)

        self.habit = Habits.objects.create(
            id=10,
            place="Город",
            time="00:00",
            activity="Гулять",
            good_habit_sign=False,
            periodicity=2,
            reward="",
            execution_time="00:01:00",
            of_publicity=False,
            user=self.user,
            relted_habbit=None,
        )
        self.habit.save()

    def test_create_habit(self):
        """Тест создания привычки"""

        data = {
            "place": "Деревня",
            "time": "00:00",
            "activity": "Пить",
            "good_habit_sign": False,
            "periodicity": 1,
            "reward": "",
            "execution_time": "00:02:00",
            "of_publicity": True,
            "user": self.user.id,
        }
        response = self.client.post("/habbit/habit/create/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_habit(self):
        """Тест получения списка привычек"""
        # Временно изменяем разрешения на AllowAny
        original_permissions = HabitListAPIView.permission_classes
        HabitListAPIView.permission_classes = [AllowAny]

        response = self.client.get("/habbit/habit/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # возвращаем обратно
        HabitListAPIView.permission_classes = original_permissions

    def test_retrieve_habit(self):
        """Тест получения информации о привычке"""
        # Временно изменяем разрешения на AllowAny
        original_permissions = HabitRetrieveAPIView.permission_classes
        HabitRetrieveAPIView.permission_classes = [AllowAny]

        response = self.client.get(f"/habbit/habit/detail/{self.habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # возвращаем обратно
        HabitRetrieveAPIView.permission_classes = original_permissions

    def test_update_habit(self):
        """Тест обновления информации о привычке"""

        updated_data = {
            "id": 2,
            "place": "Деревня",
            "time": "00:00",
            "activity": "есть",
            "good_habit_sign": False,
            "periodicity": 4,
            "reward": "",
            "execution_time": "00:02:00",
            "of_publicity": True,
            "user": self.user.id,
        }
        # Временно изменяем разрешения на AllowAny
        original_permissions = HabitUpdateAPIView.permission_classes
        HabitUpdateAPIView.permission_classes = [AllowAny]

        response = self.client.put(
            f"/habbit/habit/update/{self.habit.id}/", data=updated_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка, что данные действительно обновились
        updated_habit = Habits.objects.get(id=self.habit.id)
        self.assertEqual(updated_habit.activity, updated_data["activity"])
        self.assertEqual(updated_habit.periodicity, updated_data["periodicity"])
        HabitRetrieveAPIView.permission_classes = original_permissions

    def test_delete_habit(self):
        """Тест удаления привычки"""
        # Временно изменяем разрешения на AllowAny
        original_permissions = HabitDestroyAPIView.permission_classes
        HabitDestroyAPIView.permission_classes = [AllowAny]

        response = self.client.delete(f"/habbit/habit/delete/{self.habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Возвращаем оригинальные разрешения
        HabitDestroyAPIView.permission_classes = original_permissions

    def test_validate_related_habit_and_reward(self):
        """Тест  -Нельзя одновременно выбрать связанную привычку и указание вознаграждения"""
        data = {
            "place": "Город",
            "time": "00:00",
            "activity": "Гулять",
            "good_habit_sign": False,
            "periodicity": 2,
            "reward": "Some Reward",
            "execution_time": "00:01:00",
            "of_publicity": False,
            "user": self.user.id,
            "relted_habbit": 1,
        }
        response = self.client.post("/habbit/habit/create/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_related_habit(self):
        """Тест В связанные привычки могут попадать только привычки с признаком приятной привычки"""
        data = {
            "place": "Город",
            "time": "00:00",
            "activity": "Гулять",
            "good_habit_sign": False,
            "periodicity": 2,
            "reward": "",
            "execution_time": "00:01:00",
            "of_publicity": False,
            "user": self.user.id,
            "relted_habbit": 1,  # Assuming there is a related habit with id 1
        }
        response = self.client.post("/habbit/habit/create/", data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_validate_periodicity(self):
        """Тест Привычку нельзя выполнять реже, чем 1 раз в 7 дней."""

        data = {
            "place": "Деревня",
            "time": "00:00",
            "activity": "Пить",
            "good_habit_sign": False,
            "periodicity": 10,
            "reward": "",
            "execution_time": "00:02:00",
            "of_publicity": True,
            "user": self.user.id,
        }
        with self.assertRaises(ValidationError) as context:
            self.client.post("/habbit/habit/create/", data=data)

        self.assertEqual(
            context.exception.messages[0],
            "Привычку нельзя выполнять реже, чем 1 раз в 7 дней.",
        )

    def test_validate_execution_time(self):
        """Тест: Время выполнения не может быть больше 120 секунд."""
        data = {
            "place": "Деревня",
            "time": "00:00",
            "activity": "Пить",
            "good_habit_sign": False,
            "periodicity": 4,
            "reward": "",
            "execution_time": "00:03:00",
            "of_publicity": True,
            "user": self.user.id,
        }

        with self.assertRaises(ValidationError) as context:
            self.client.post("/habbit/habit/create/", data=data)

        self.assertEqual(
            context.exception.messages[0],
            "Время выполнения не может быть больше 120 секунд.",
        )
