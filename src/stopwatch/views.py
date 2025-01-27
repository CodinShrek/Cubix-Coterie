from django.shortcuts import render, redirect
from stopwatch.models import StopwatchEntry
from django.http import HttpResponse
import time
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Min, OuterRef, Subquery, Exists
from operator import attrgetter
from django.contrib import messages

from user.models import Account


def start_stopwatch(request):
    if request.user.is_authenticated:
        # Check if there is an active stopwatch entry (no end_time) for the user
        active_entry = StopwatchEntry.objects.filter(user=request.user, end_time__isnull=True).exists()

        if not active_entry:
            # If no active entry exists, create a new stopwatch entry
            StopwatchEntry.objects.create(user=request.user, start_time=timezone.now())
        else:
            # If there is already an active entry, notify the user
            messages.warning(request, "You already have an active stopwatch. Please stop it before starting a new one.")
    return redirect('stopwatch')

def stop_stopwatch(request):
    if request.user.is_authenticated:
        try:
            # Fetch the most recent StopwatchEntry for the user where end_time is still null (the stopwatch is running) #
            entry = StopwatchEntry.objects.filter(user=request.user, end_time__isnull=True).latest('start_time')
            # Set the end_time to the current time (stop the stopwatch) #
            entry.end_time = timezone.now()
            # Calculate the duration in total seconds (end_time - start_time) #
            entry.duration = (entry.end_time - entry.start_time).total_seconds()
            # Store the duration in seconds (additional step for clarity) #
            duration_seconds = entry.duration
            if duration_seconds > 11:
                entry.save()
                messages.success(request, f"Your cubing time is {duration_seconds:.2f} seconds.")
            else:
                # Optionally, delete the entry if the duration is too short
                entry.delete()
                messages.warning(request, "Cubing Duration is too short. You're Bluffing, aren't you!")
                
        except StopwatchEntry.DoesNotExist:
                print("No stopwatch entry found to stop.")  
    return redirect('stopwatch')

def history(request):
    user=request.user
    entries = request.user.stopwatchentry_set.order_by('-end_time')
    return render(request, 'stopwatch/table.html', {'entries': entries})

def stopwatch(request):
    return render(request, "stopwatch/stopwatchcontrol.html")

def result(request):
    return render(request, "stopwatch/result.html")

def leaderboard(request):
    context = {}

    # Get all stopwatch entries
    entries = [entry for entry in StopwatchEntry.objects.all() if entry.duration and entry.duration > 0]

    # Implementing Selection Sort based on 'duration'
    for i in range(len(entries)):
        min_id = i
        for j in range(i+1, len(entries)):
            if entries[j].duration < entries[min_id].duration:
                min_id = j
        
        # Swap the found minimum element with the first element
        entries[i], entries[min_id] = entries[min_id], entries[i]

    context['entries'] = entries

    return render(request, 'stopwatch/leaderboard.html', context)

def personal_best(request):
    context = {}

    # Get all stopwatch entries
    entries = [entry for entry in StopwatchEntry.objects.filter(user=request.user)]

    # Implementing Selection Sort based on 'duration'
    for i in range(len(entries)):
        min_id = i
        for j in range(i+1, len(entries)):
            if entries[j].duration < entries[min_id].duration:
                min_id = j
        
        # Swap the found minimum element with the first element
        entries[i], entries[min_id] = entries[min_id], entries[i]

    context['entries'] = entries

    return render(request, 'stopwatch/personalbest.html', {'entries': entries})    
    

def display_first_duration(request):
     # Define a subquery to check if a user has any StopwatchEntry records #
    stopwatch_exists = StopwatchEntry.objects.filter(
        user=OuterRef('pk') # Reference to the user's primary key #
    )
    
    # Filter users based on the existence of a StopwatchTiming entry
    users_with_stopwatch = Account.objects.annotate(
        has_stopwatch=Exists(stopwatch_exists)
    ).filter(has_stopwatch=True) # Only include users who have stopwatch entries #
    
    ordered_stopwatches = StopwatchEntry.objects.filter(
        user=OuterRef('pk')
    ).order_by('duration') # Order stopwatch entries by duration #

    users_with_first_duration = Account.objects.annotate(
        first_duration=Subquery(ordered_stopwatches.values('duration')[:1]) # Get the first duration (shortest) for each user #
    # Exclude users with no stopwatch duration and order by duration #
    ).filter(first_duration__isnull=False).order_by('first_duration')

    # Prepare the context dictionary to pass the filtered users to the template #
    context = {'users_with_first_duration': users_with_first_duration}
    return render(request, 'stopwatch/test.html', context)