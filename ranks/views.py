from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Rank


@login_required(login_url='/login/')
def index(request):
    """
    Show ranks for the logged-in user. If the user has a linked MartialArtist
    profile, show only that person's ranks. Staff see all ranks.
    """
    martial_artist = getattr(request.user, 'martial_artist_profile', None)
    if request.user.is_staff and martial_artist is None:
        ranks = Rank.objects.select_related(
            'martial_artist', 'rank_type', 'rank_type__style'
        ).order_by('-award_date')
        scope_message = 'Showing all ranks (staff view).'
    elif martial_artist is not None:
        ranks = Rank.objects.filter(martial_artist=martial_artist).select_related(
            'martial_artist', 'rank_type', 'rank_type__style'
        ).order_by('-award_date')
        scope_message = f'Your ranks ({martial_artist}).'
    else:
        ranks = Rank.objects.none()
        scope_message = (
            'No martial artist profile is linked to your account. '
            'Ask an administrator to link your user account to your martial artist record.'
        )
    return render(request, 'ranks/index.html', {
        'ranks': ranks,
        'scope_message': scope_message,
        'martial_artist': martial_artist,
    })
