from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Bug



def index(request):
    latest_bug_list = Bug.objects.order_by("-report_date")[:15]
    context = {"latest_bug_list": latest_bug_list}
    return render(request, "bug/index.html", context)


def detail(request, bug_id):
    bug = get_object_or_404(Bug, pk=bug_id)
    return render(request, "bug/detail.html", {"bug":bug})

def register_bug(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        bug_type = request.POST.get('bug_type')
        report_date = request.POST.get('report_date')
        status = request.POST.get('status')
        bug = Bug(description=description, bug_type=bug_type, report_date=report_date, status=status)
        bug.save()
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'bug/register_bug.html')