from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    name = models.CharField(max_length=255)
    preview = models.ImageField(upload_to='previews/')
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='courses', default=1)
    # Предоставление значения по умолчанию

    def __str__(self):
        return self.name

class Lesson(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    preview = models.ImageField(upload_to='previews/')
    video_url = models.URLField()
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE,
                               related_name='lessons')
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='lessons')

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='subscriptions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='subscriptions')

    def __str__(self):
        return f"{self.user} subscribed to {self.course}"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='payments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True,
                                                null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.course} by {self.user}"
