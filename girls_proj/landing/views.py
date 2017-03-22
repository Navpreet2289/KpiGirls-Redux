from django.utils.translation import ugettext as _
from django.views.generic import ListView, TemplateView

from watson import search as watson


class SearchListView(ListView):
    template_name = 'landing/search_page.html'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        context['q'] = self.get_search_query()
        return context

    def get_search_query(self):
        if 'q' in self.request.GET:
            return self.request.GET.get('q')
        else:
            return None

    def get_queryset(self):
        search_query = self.get_search_query()
        if search_query is not None:
            search_results = watson.search(search_query)
            return search_results
        return []


class AboutPage(TemplateView):
    template_name = 'landing/about.html'
