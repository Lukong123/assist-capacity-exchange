from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Bug



class IndexView(generic.ListView):
    template_name = "bug/index.html"
    context_object_name = "latest_bug_list"

    def get_queryset(self):
        """Return the last five published bug."""
        return Bug.objects.order_by("-report_date")[:5]



class DetailView(generic.DetailView):
    model = Bug
    template_name = "bug/detail.html"

class RegisterBugView(generic.CreateView):
    model = Bug
    fields = ["description", "bug_type", "report_date", "status"]
    template_name = 'bug/register_bug.html'

    def get_success_url(self):
        return reverse("index")