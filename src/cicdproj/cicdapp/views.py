import json
from authlib.integrations.django_client import OAuth
from urllib.parse import quote_plus, urlencode

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .forms import EntryForm
from .models import Entry


oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )


def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token

    return redirect(request.build_absolute_uri(reverse("index")))


def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )


class IndexView(TemplateView):
    template_name = "cicdapp/index.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["session"] = request.session.get("user")
        return self.render_to_response(context)


class OAuthSessionMixin:

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get("user"):
            return HttpResponseRedirect(reverse_lazy("index"))
        return super().dispatch(request, *args, **kwargs)


class EntryListView(OAuthSessionMixin, ListView):
    """
    Entry list view with pagination
    """

    model = Entry
    template_name_suffix = "s_list"
    paginate_by = 10

    def get_queryset(self):
        return Entry.objects.all().order_by("-id")


class EntryDetailView(OAuthSessionMixin, DetailView):
    """
    This View displays entry
    """

    model = Entry


class EntryCreateView(OAuthSessionMixin, CreateView):
    """
    This View creates entry
    """

    model = Entry
    form_class = EntryForm
    success_url = reverse_lazy("entries")
