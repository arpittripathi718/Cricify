from django.db import models
from django.utils.text import slugify


class Team(models.Model):
    name = models.CharField(max_length=120)
    short_name = models.CharField(max_length=10)
    logo = models.ImageField(upload_to='teams/', blank=True, null=True)
    country = models.CharField(max_length=120, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    ROLE_CHOICES = [
        ('Batsman', 'Batsman'),
        ('Bowler', 'Bowler'),
        ('All-Rounder', 'All-Rounder'),
        ('Wicket-Keeper', 'Wicket-Keeper'),
    ]

    name = models.CharField(max_length=120)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    batting_style = models.CharField(max_length=120, blank=True, null=True)
    bowling_style = models.CharField(max_length=120, blank=True, null=True)
    image = models.ImageField(upload_to='players/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Match(models.Model):
    STATUS_CHOICES = [
        ('Live', 'Live'),
        ('Upcoming', 'Upcoming'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1_matches')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2_matches')
    venue = models.CharField(max_length=200)
    date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Upcoming')
    score_team1 = models.CharField(max_length=50, blank=True, null=True)
    score_team2 = models.CharField(max_length=50, blank=True, null=True)
    result = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    thumbnail = models.ImageField(upload_to='news/', blank=True, null=True)
    summary = models.TextField()
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class PointsTable(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    matches = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)
    net_run_rate = models.FloatField(default=0.0)

    class Meta:
        ordering = ['-points', '-net_run_rate']

    def __str__(self):
        return f"{self.team.name} - {self.points}"
