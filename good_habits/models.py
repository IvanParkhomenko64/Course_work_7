from django.db import models
from django.utils import timezone

from good_habits.validators import (
    validate_related_habit_and_reward,
    validate_execution_time,
    validate_related_habit,
    validate_good_habit,
    validate_periodicity,
)
from users.models import NULLABLE, User


class Habits(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user",
        **NULLABLE,
        verbose_name="пользователь",
    )
    place = models.CharField(max_length=200, **NULLABLE, verbose_name="место")
    activity = models.CharField(max_length=300, **NULLABLE, verbose_name="действие")
    reward = models.CharField(max_length=200, **NULLABLE, verbose_name="награда")
    of_publicity = models.BooleanField(default=False, verbose_name="публичность")
    time = models.TimeField(
        default=timezone.now, verbose_name="Время выполнения привычки"
    )
    good_habit_sign = models.BooleanField(
        default=False, verbose_name="признак приятной привычки"
    )
    relted_habbit = models.ForeignKey(
        "self", on_delete=models.SET_NULL, verbose_name="Связанная привычка", **NULLABLE
    )
    periodicity = models.IntegerField(default=1, verbose_name="периодичность")
    execution_time = models.TimeField(
        default="00:02", verbose_name="время на выполнение"
    )

    def __str__(self):
        return f"{self.user}, {self.place}"

    def clean(self):
        """Проверка данных перед сохранением"""
        validate_related_habit_and_reward(self)
        validate_execution_time(self.execution_time)
        validate_related_habit(self)
        validate_good_habit(self)
        validate_periodicity(self.periodicity)

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"
        ordering = ["time"]