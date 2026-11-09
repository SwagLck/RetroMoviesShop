from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Genre(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=200)
    year = models.IntegerField(null=True, blank=True)
    overview = models.TextField(blank=True)
    poster_path = models.CharField(max_length=200, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)

class TvShow(models.Model):
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)
    title = models.CharField(max_length=200)
    year = models.IntegerField(null=True, blank=True)
    toyear = models.IntegerField(null=True, blank=True)
    overview = models.TextField(blank=True)
    poster_path = models.CharField(max_length=200, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comments"
    )
    tvshow = models.ForeignKey(
        TvShow,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comments"
    )
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_hidden = models.BooleanField(default=False)

    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 11)],
        null=False,
        blank=False
    )

    class Meta:
        ordering = ["-created_at"]
        permissions = [
            ("can_delete_comments", "Can delete any comment"),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "movie"],
                name="one_review_per_user_movie"
            ),
            models.UniqueConstraint(
                fields=["user", "tvshow"],
                name="one_review_per_user_tvshow"
            ),
        ]

    def __str__(self):
        return f"{self.user.username}: {self.text[:30]}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography=models.CharField(max_length=300)
    favorite_genre=models.CharField(max_length=50)

    class Meta:
        permissions = [("can_block_users", "Can block and unblock users")]

class Report(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="reports")
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports_made")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["comment", "reporter"], name="one_report_per_user_per_comment"),
        ]

    def __str__(self):
        return f"Reported by {self.reporter.username} on comment {self.comment_id}"
