from django.urls import path
from .views import DashboardView,PostQuestionView,PostCommentView,VoteView
urlpatterns = [
    path('',DashboardView.as_view(),name='dashboard'),
    path('post-question',PostQuestionView.as_view(),name='post-question'),
    path('post-comment',PostCommentView.as_view(),name='post-comment'),
    path('like-dislike-question-answer',VoteView.as_view(),name='like-question-answer')
]
