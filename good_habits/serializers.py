from rest_framework import serializers

from good_habits.models import Habits


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habits
        fields = "__all__"

    def create(self, validated_data):
        habit = Habits(**validated_data)
        habit.clean()  # Вызов метода clean
        habit.save()
        return habit