from django.db import models
from django.db.models import ForeignKey


class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PlayerCard(models.Model):
    name = models.CharField(max_length=100)
    team = ForeignKey(Team, on_delete=models.CASCADE, related_name="player_cards")
    is_collected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.team.name}"
