"""
Link a Django user to a MartialArtist so they see their own ranks, profile, and styles.

Usage:
  python manage.py link_user_to_martial_artist USERNAME LAST_NAME
  python manage.py link_user_to_martial_artist wseyler Seyler

  Or by martial artist ID:
  python manage.py link_user_to_martial_artist USERNAME --id MARTIAL_ARTIST_ID
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from people.models import MartialArtist


class Command(BaseCommand):
    help = 'Link a Django user to a MartialArtist by username and last name (or by ID).'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Django user username (e.g. wseyler)')
        parser.add_argument(
            'last_name',
            nargs='?',
            type=str,
            default=None,
            help='Martial artist last name (e.g. Seyler). First match is used.',
        )
        parser.add_argument(
            '--id',
            type=int,
            metavar='PK',
            help='Martial artist primary key instead of last name.',
        )

    def handle(self, *args, **options):
        User = get_user_model()
        username = options['username']
        last_name = options['last_name']
        ma_id = options.get('id')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'User "{username}" does not exist.'))
            return

        if ma_id is not None:
            try:
                ma = MartialArtist.objects.get(pk=ma_id)
            except MartialArtist.DoesNotExist:
                self.stderr.write(self.style.ERROR(f'MartialArtist with id={ma_id} does not exist.'))
                return
        elif last_name:
            qs = MartialArtist.objects.filter(last_name__iexact=last_name.strip())
            if not qs.exists():
                self.stderr.write(self.style.ERROR(
                    f'No MartialArtist with last name "{last_name}". '
                    'Use --id PK to specify by primary key.'
                ))
                return
            ma = qs.first()
            if qs.count() > 1:
                self.stdout.write(
                    self.style.WARNING(f'Multiple martial artists with last name "{last_name}"; using first: {ma}.')
                )
        else:
            self.stderr.write(self.style.ERROR('Provide either last_name or --id.'))
            return

        if ma.user_id and ma.user_id != user.pk:
            self.stdout.write(self.style.WARNING(
                f'MartialArtist {ma} was linked to user "{ma.user.username}". Overwriting.'
            ))
        ma.user = user
        ma.save()
        self.stdout.write(self.style.SUCCESS(f'Linked user "{username}" to martial artist: {ma}.'))
