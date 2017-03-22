import json
import random

from django.http import Http404
from django.contrib import messages
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic.detail import DetailView
from django.template.loader import render_to_string
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView, UpdateView
from django.http import HttpResponseRedirect, Http404, HttpResponse

from braces.views import LoginRequiredMixin

from .models import Facemash
from .utils import calculate_rating
from .forms import FaceForm, FacemashUpdateForm
from .helpers import cache_hits, get_top_girls


class PlayView(FormView):
    template_name = 'facemash/facemash.html'
    form_class = FaceForm
    success_url = reverse_lazy("facemash:play")

    def form_valid(self, form):
        if self.request.is_ajax():
            winner = form.cleaned_data['winner']
            loser = form.cleaned_data['loser']
            calculate_rating(winner, loser)
            data = render_to_string("facemash/ajax.html", self.get_context_data())
            return HttpResponse(data)
        return super(PlayView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PlayView, self).get_context_data(**kwargs)
# ///////////////////////////////////////////////////////////////
        # contestants = Facemash.objects.all()
        # contestant_1 = random.choice(contestants)
        # contestant_2 = random.choice(contestants)
        # # A while loop to ensure that the contestants aren't same.
        # while contestant_1 == contestant_2:
        #     contestant_2 = random.choice(contestants)
# //////////////////////////////////////////////////////////////////
        # contestants = Facemash.objects.order_by('?')[:2]
        # contestant_1 = contestants.first()
        # contestant_2 = contestants.last()
        # # A while loop to ensure that the contestants aren't same.
        # while contestant_1 == contestant_2:
        #     contestant_2 = random.choice(contestants)
# //////////////////////////////////////////////////////
        # last = Facemash.objects.count() - 1
        last = 5170
        index1 = random.randint(0, last)
        # Here's one simple way to keep even distribution for
        # index2 while still gauranteeing not to match index1.
        index2 = random.randint(0, last - 1)
        if index2 == index1: index2 = last
        contestant_1 = Facemash.objects.all()[index1]
        contestant_2 = Facemash.objects.all()[index2]
# ///////////////////////////////////////////
        context['contestant_1'] = contestant_1
        context['contestant_2'] = contestant_2
        return context


class RatingsListView(ListView):
    template_name = 'facemash/ratings_page.html'

    def get_context_data(self, **kwargs):
        context = super(RatingsListView, self).get_context_data(**kwargs)
        context['sort_filter'] = self.get_sorting_filter()
        return context

    def order_queryset(self, qs):
        sort_filter = self.get_sorting_filter()
        if sort_filter == 'ratings':
            qs = qs.order_by('-ratings')[:100]
        elif sort_filter == 'views':
            qs = qs.filter(id__in=get_top_girls())
        else:
            qs = qs.order_by('-ratings')[:100]
        return qs

    def get_sorting_filter(self):
        if 'sort_by' in self.request.GET:
            return self.request.GET.get('sort_by')
        else:
            return None

    def get_queryset(self):
        qs = Facemash.objects.active()

        qs = self.order_queryset(qs)
        return qs


class GirlDetailView(DetailView):
    model = Facemash
    template_name = 'facemash/girl_detail.html'

    def get_object(self):
        try:
            girl_object = self.get_queryset().get(slug=self.kwargs['slug'])
            if girl_object.is_active:
                cache_hits(girl_object.id, self.request)
            return girl_object
        except Facemash.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(GirlDetailView, self).get_context_data(**kwargs)
        context['avarage'] = Facemash.objects.count_average()
        return context


class FacemashUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'facemash/facemash_update.html'
    form_class = FacemashUpdateForm

    def get_object(self):
        return self.request.user.facemash

    def get_success_url(self):
        messages.success(self.request, _('Фото оновлено вдало'))
        return reverse_lazy('accounts:profile_detail', kwargs={'slug': self.request.user.profile.slug})
