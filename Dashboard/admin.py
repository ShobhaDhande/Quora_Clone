from django.contrib import admin
from .models import QuestionModel,AnswerModel,LikeModel
# Register your models here.

admin.site.register(QuestionModel)
admin.site.register(AnswerModel)
admin.site.register(LikeModel)