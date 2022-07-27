from voting.models import Ballot, Candidate
from cryptography.fernet import Fernet


def get_vote_results():
    candidates_data = Candidate.objects.all()
    ballots_data = Ballot.objects.all()
    total_votes = {}
    for candidate in candidates_data:
        total_votes[candidate.name] = 0
    for ballot in ballots_data:
        total_votes[ballot.candidate] += 1
    worksheet_headers = [["Candidate", "Vote Count"]]
    worksheet_list = []
    for i in total_votes:
        worksheet_list.append([i, total_votes[i]])
    return worksheet_headers+worksheet_list


def encrypt_vote_id(vote_id, user):
    id = vote_id
    id = str(id).encode("utf-8")

    key = user.voting_secret_key
    f = Fernet(key)

    id = f.encrypt(id)
    return id
