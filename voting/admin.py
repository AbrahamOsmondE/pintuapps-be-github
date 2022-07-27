from django.contrib import admin
from .models import Voted, Ballot, Candidate
# Register your models here.

class VotedAdmin(admin.ModelAdmin):
    list_display=('id','user')

    def id(self,obj):
        return obj.user.id

class BallotAdmin(admin.ModelAdmin):
    list_display=('id','candidate')

    def id(self,obj):
        return obj.candidate
    
class CandidateAdmin(admin.ModelAdmin):
    list_display=('id','name')

    def id(self,obj):
        return obj.name

admin.site.register(Voted, VotedAdmin)
admin.site.register(Ballot, BallotAdmin)
admin.site.register(Candidate, CandidateAdmin) 
