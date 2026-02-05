from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.urls import reverse


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'


# Pages shown on the post-login dashboard. Each tuple: (label, url_name_or_path, permission).
# url_name_or_path: URL name (e.g. 'home') or path starting with '/' (e.g. '/people/').
# permission is None (any authenticated user), 'staff' (is_staff), or a perm codename e.g. 'auth.add_user'.
DASHBOARD_PAGES = [
    ('Home', 'home', None),
    ('About', 'about', None),
    ('People', '/people/', None),
    ('Ranks', '/ranks/', None),
    ('Styles', '/styles/', None),
    ('Blog', '/blog/', None),
    ('Site administration', 'admin:index', 'staff'),
]


def _user_can_access(user, permission):
    if permission is None:
        return True
    if permission == 'staff':
        return user.is_staff
    return user.has_perm(permission)


def _resolve_url(url_name_or_path):
    """Return URL path. If argument starts with '/', return as-is; else reverse by name."""
    if url_name_or_path.startswith('/'):
        return url_name_or_path
    return reverse(url_name_or_path)


def _get_dashboard_section_data(label, url_name_or_path):
    """
    Fetch summary data for a dashboard section. Returns dict with 'items' (list of display dicts)
    and 'count', or None if this section has no data (link only).
    """
    from people.models import MartialArtist
    from ranks.models import Rank
    from styles.models import Style
    from blog.models import Post

    try:
        if url_name_or_path == '/people/':
            qs = MartialArtist.objects.filter(active=True).order_by('last_name', 'first_name')[:8]
            count = MartialArtist.objects.filter(active=True).count()
            items = [{'text': str(ma), 'url': None} for ma in qs]
            return {'items': items, 'count': count}
        if url_name_or_path == '/ranks/':
            qs = Rank.objects.select_related('martial_artist', 'rank_type').order_by('-award_date')[:8]
            count = Rank.objects.count()
            items = [
                {'text': f'{r.martial_artist} — {r.rank_type.title}', 'sub': r.award_date.strftime('%Y-%m-%d'), 'url': None}
                for r in qs
            ]
            return {'items': items, 'count': count}
        if url_name_or_path == '/styles/':
            qs = Style.objects.all().order_by('title')[:15]
            count = Style.objects.count()
            items = [{'text': s.title, 'url': None} for s in qs]
            return {'items': items, 'count': count}
        if url_name_or_path == '/blog/':
            qs = Post.published.all().order_by('-publish')[:5]
            count = Post.published.count()
            items = [
                {'text': p.title, 'url': reverse('post_detail', kwargs={'slug': p.slug})}
                for p in qs
            ]
            return {'items': items, 'count': count}
    except Exception:
        pass
    return None


@login_required(login_url='/login/')
def user_dashboard(request):
    """Show dashboard with links and summary data for each section the user can access."""
    sections = []
    for label, url_name_or_path, permission in DASHBOARD_PAGES:
        if not _user_can_access(request.user, permission):
            continue
        try:
            url = _resolve_url(url_name_or_path)
        except Exception:
            continue
        data = _get_dashboard_section_data(label, url_name_or_path)
        if data:
            sections.append({
                'label': label,
                'url': url,
                'items': data['items'],
                'count': data['count'],
            })
        else:
            sections.append({'label': label, 'url': url, 'items': [], 'count': None})
    return render(request, 'pages/user_dashboard.html', {'sections': sections})


@require_http_methods(["GET", "POST"])
def signupuser(request):
    """Optimized signup view using Django forms properly"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('home')
            except IntegrityError:
                form.add_error('username', 'That username has already been taken. Please choose a new username.')
        # Form is invalid or IntegrityError occurred
        return render(request, 'pages/signupuser.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'pages/signupuser.html', {'form': form})


@require_http_methods(["POST"])
def logoutuser(request):
    """Optimized logout view - POST only"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@require_http_methods(["GET", "POST"])
def loginuser(request):
    """Optimized login view using Django forms properly"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                if user.is_superuser:
                    return redirect('admin:index')
                return redirect('user_dashboard')
        # Invalid credentials
        messages.error(request, 'Username and password did not match.')
    else:
        form = AuthenticationForm()
    return render(request, 'pages/loginuser.html', {'form': form})
