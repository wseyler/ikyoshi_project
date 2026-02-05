from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import MartialArtist


@login_required(login_url='/login/')
def index(request):
    """
    Show the logged-in user's martial artist profile when linked.
    Staff without a linked profile see the full list of active martial artists.
    """
    martial_artist = getattr(request.user, 'martial_artist_profile', None)
    if request.user.is_staff and martial_artist is None:
        people = MartialArtist.objects.filter(active=True).select_related(
            'sponsor', 'payment_plan'
        ).prefetch_related('styles').order_by('last_name', 'first_name')
        scope_message = 'All active martial artists (staff view).'
        return render(request, 'people/index.html', {
            'people': people,
            'scope_message': scope_message,
            'single_profile': None,
        })
    elif martial_artist is not None:
        scope_message = 'Your profile.'
        return render(request, 'people/index.html', {
            'people': [martial_artist],
            'scope_message': scope_message,
            'single_profile': martial_artist,
        })
    else:
        return render(request, 'people/index.html', {
            'people': [],
            'scope_message': (
                'No martial artist profile is linked to your account. '
                'Ask an administrator to link your user account to your martial artist record.'
            ),
            'single_profile': None,
        })
