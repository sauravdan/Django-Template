from __future__ import absolute_import
from django.db.models import Count
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import redirect
from braces import views
from . import models
from . import forms

class RestrictToUserMixin(object):
  def get_queryset(self):
    queryset = super(RestrictToUserMixin, self).get_queryset()
    queryset = queryset.filter(user=self.request.user)
    return queryset

class TalkListListView(
    views.LoginRequiredMixin,
    RestrictToUserMixin,
    generic.ListView
  ):
  model = models.TalkList

class TalkListDetailView(
    views.LoginRequiredMixin,
    views.PrefetchRelatedMixin,
    RestrictToUserMixin,
    generic.DetailView
  ):

  form_class = forms.TalkForm
  http_method_names = ['get', 'post']
  model = models.TalkList
  prefetch_related = ('talks',)

  def get_context_data(self, **kwargs):
    context = super(TalkListDetailView, self).get_context_data(**kwargs)
    context.update({'form':self.form_class(self.request.POST or None)})
    return context

  def post(self, request, *args, **kwargs):
    form = self.form_class(request.POST)
    if form.is_valid():
      obj = self.get_object()
      talk = form.save(commit=False)
      talk.talk_list = obj
      talk.save()
    else:
      return self.get(request, *args, **kwargs)
    return redirect(obj)

class TalkListCreateView(
    views.LoginRequiredMixin,
    views.SetHeadlineMixin,
    generic.CreateView
  ):
  form_class = forms.TalkListForm
  headline = 'Create'
  model = models.TalkList

  def form_valid(self, form):
    self.object = form.save(commit=False)
    self.object.user = self.request.user
    self.object.save()
    return super(TalkListCreateView, self).form_valid(form)

class TalkListUpdateView(
    RestrictToUserMixin,
    views.LoginRequiredMixin,
    views.SetHeadlineMixin,
    generic.UpdateView
  ):

  form_class = forms.TalkListForm
  headline = 'Update'
  model = models.TalkList



