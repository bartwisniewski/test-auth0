from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .forms import EntryForm
from .models import Entry


class IndexView(TemplateView):
    template_name = "cicdapp/index.html"


class EntryListView(ListView):
    """
    Entry list view with pagination
    """

    model = Entry
    template_name_suffix = "s_list"
    paginate_by = 10

    def get_queryset(self):
        return Entry.objects.all().order_by("-id")


class EntryDetailView(DetailView):
    """
    This View displays entry
    """

    model = Entry


class EntryCreateView(CreateView):
    """
    This View creates entry
    """

    model = Entry
    form_class = EntryForm
    success_url = reverse_lazy("entries")
