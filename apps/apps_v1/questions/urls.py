from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.QuestionView.as_view(), name="questions"),
    url(r"^(?P<question_id>\d+)/$", views.QuestionDetailView.as_view(), name="question_detail"),
    url(r"^(?P<question_id>\d+)/comments/$", views.QuestionCommentView.as_view(), name="question_detail"),
    url(r"^(?P<question_id>\d+)/answers/$", views.AnswerView.as_view(), name="answers"),
    url(r"^(?P<question_id>\d+)/answers/(?P<answer_id>\d+)/$", views.AnswerDetailView.as_view(), name="answer_detail"),
    url(r"^(?P<question_id>\d+)/answers/(?P<answer_id>\d+)/comments/$", views.AnswerCommentView.as_view(),
        name="answer_comments"),
    url(r"^follows/$", views.QuestionFollowView.as_view(), name="follows"),
    url(r"^invitations/$", views.InvitationView.as_view(), name="invitations"),
    url(r"^invitations/users/$", views.HelperView.as_view(), name="who_can_help"),
    url(r"^comments/$", views.CommentView.as_view(), name="comments"),
    url(r"^votes/$", views.VoteView.as_view(), name="votes"),
]
