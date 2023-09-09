from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.test import APITestCase


from users.models import User
from users.views import UserDestroyAPIView, UserUpdateAPIView


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        """Общие данные"""

        self.user = User.objects.create(
            email="3@admin.ru", password="spartak67", is_active=True, is_superuser=True
        )
        self.user.save()
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        """Тест создания пользователя"""

        data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "123456789",
            "country": "USA",
            "comment": "Test user",
            "password": "spartak67",
            "is_active": True,
            "is_superuser": True,
        }
        response = self.client.post("/user/create/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_users(self):
        """Тест получения списка пользователей"""

        response = self.client.get("/user/list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user(self):
        """Тест получения информации о пользователе"""

        response = self.client.get(f"/user/deteil/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        """Тест обновления информации о пользователе"""

        updated_data = {
            "email": "test@example.com",
            "first_name": "Updated",
            "last_name": "User",
            "phone": "987654321",
            "country": "Canada",
            "comment": "Updated user info",
            "is_active": False,
            "password": "spartak67",
        }
        # Временно изменяем разрешения на AllowAny
        original_permissions = UserUpdateAPIView.permission_classes
        UserUpdateAPIView.permission_classes = [AllowAny]

        response = self.client.put(f"/user/update/{self.user.id}/", data=updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка, что данные действительно обновились
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.first_name, updated_data["first_name"])
        self.assertEqual(updated_user.last_name, updated_data["last_name"])
        self.assertEqual(updated_user.phone, updated_data["phone"])
        self.assertEqual(updated_user.country, updated_data["country"])
        self.assertEqual(updated_user.comment, updated_data["comment"])
        self.assertEqual(updated_user.is_active, updated_data["is_active"])
        UserUpdateAPIView.permission_classes = original_permissions

    def test_delete_user(self):
        """Тест удаления пользователя"""
        # Временно изменяем разрешения на AllowAny
        original_permissions = UserDestroyAPIView.permission_classes
        UserDestroyAPIView.permission_classes = [AllowAny]

        response = self.client.delete(f"/user/delete/{self.user.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Возвращаем оригинальные разрешения
        UserDestroyAPIView.permission_classes = original_permissions
