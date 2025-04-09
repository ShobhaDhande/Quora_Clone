from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class QuestionModel(models.Model):
    question_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.question
    
    
class AnswerModel(models.Model):
    answer_id = models.AutoField(primary_key=True)
    question_id = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.answer
    

class LikeModel(models.Model):
    CHOICES = (
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    vote_type = models.CharField(max_length=7, choices=CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
    