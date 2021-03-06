from .services import encrypt_vote_id
import xlsxwriter
from .services import get_vote_results
from voting.models import Candidate, Voted, Ballot
import io
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.


class VerificationAPI(APIView):
    def get(self, request, *args, **kwargs):
        data = request.user
        response = {"verified": data.voting_verified}
        return Response(data=response)

    def put(self, request, *args, **kwargs):
        data = request.user
        data.voting_verified = True
        data.save()
        return Response(data={"verified": data.voting_verified})


class VoteResultAPI(APIView):
    def get(self, request, *args, **kwargs):
        vote_details = get_vote_results()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        votes = workbook.add_worksheet()
        for row, data in enumerate(vote_details):
            for coll, cell in enumerate(data):
                votes.write(row, coll, cell)
        workbook.close()
        output.seek(0)
        filename = 'Vote_Results.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response


class CandidateAPI(APIView):
    def get(self, request, *args, **kwargs):
        candidates = Candidate.objects.all()
        response = []
        for candidate in candidates:
            response.append({"id": candidate.id, "name": candidate.name,
                            "display_picture": candidate.display_picture, "motto": candidate.motto})
        return Response(data=response)


class VoteAPI(APIView):
    def get(self, request, *args, **kwargs):
        data = request.user
        if Voted.objects.filter(user=data):
            vote = True
        else:
            vote = False
        return Response(data={"voted": vote})

    def post(self, request):
        user = request.user
        if user.voting_verified and not Voted.objects.filter(user=user).exists():
            id = encrypt_vote_id(user.id, user)
            candidate_id = request.data["candidate_id"]
            candidate = Candidate.objects.get(id=candidate_id)

            _ = Ballot.object.create(id=id, candidate=candidate)
            vote = Voted.objects.create(user=user)
            return Response(data={"voted": True})
        else:
            return Response(data={"error": "You are not authorized to vote"})


class VoteDetailsAPI(APIView):
    def delete(self, request, id):
        if request.user.is_staff and Voted.objects.filter(user=request.user).exists():
            user = request.user
            vote = Voted.objects.get(user=user)

            id = encrypt_vote_id(user.id, user)
            ballot = Ballot.objects.get(id=id)

            ballot.delete()
            vote.delete()
            return Response(data={"voted": False})
        else:
            return Response(data={"error": "You are not authorized to delete this vote"})
