from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Style


@login_required(login_url='/login/')
def index(request):
    """
    Show styles for the logged-in user when they have a linked MartialArtist
    (only the styles they study). Staff without a linked profile see all styles.
    """
    martial_artist = getattr(request.user, 'martial_artist_profile', None)
    if request.user.is_staff and martial_artist is None:
        styles = Style.objects.all().order_by('title')
        scope_message = 'All styles (staff view).'
    elif martial_artist is not None:
        styles = martial_artist.styles.all().order_by('title')
        scope_message = f'Your styles ({martial_artist}).'
    else:
        styles = Style.objects.none()
        scope_message = (
            'No martial artist profile is linked to your account. '
            'Ask an administrator to link your user account to your martial artist record.'
        )
    return render(request, 'styles/index.html', {
        'styles': styles,
        'scope_message': scope_message,
        'martial_artist': martial_artist,
    })
