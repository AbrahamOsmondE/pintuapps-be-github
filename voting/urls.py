from django.urls import path
from . import views

urlpatterns = [
    path("verification/", views.VerificationAPI.as_view(), name="verification"),
    path("vote_results/", views.VoteResultAPI.as_view(), name="vote_results"),
    path("candidate/", views.CandidateAPI.as_view(), name="candidate"),
    path("vote/", views.VoteAPI.as_view(), name="vote"),
    path("vote/<int:id>/", views.VoteDetailsAPI.as_view(), name="vote_details"),
]
