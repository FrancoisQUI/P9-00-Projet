from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2038, blank=True)
    user: User = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='books_cover')
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.title} - {self.user.username}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('ticket_detail', kwargs={'pk': self.pk})


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)),
        default=3
    )
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user: User = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.ticket.title} - {self.user.username}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('review_detail', kwargs={'pk': self.pk})


class UserFollows(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name='followed_by')

    def __str__(self):
        return f"{self.id} - {self.user} -> {self.followed_user}"

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user',)
