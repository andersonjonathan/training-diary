from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Activity


@login_required
def index(request):
    context = {'current_page': 'Activities', "activities": Activity.objects.filter(user=request.user)}

    return render(request, 'activities/index.html', context)


@login_required
def activity(request, pk):
    try:
        training_activity = Activity.objects.get(pk=pk, user=request.user)
    except Activity.DoesNotExist:
        raise Http404
    context = {'current_page': 'Activities', "activity": training_activity, "google_api_key": settings.GOOGLE_API_KEY}
    return render(request, 'activities/activity.html', context)
