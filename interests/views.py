from django.contrib import messages
from django.core.signing import BadSignature
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views import generic

from .forms import RegisterInterestForm, UpdateInterestForm
from .models import Interest


class CreateView(generic.CreateView):
    template_name = 'home.html'
    form_class = RegisterInterestForm

    def get_success_url(self):
        return reverse('update-interest', kwargs={'token': self.object.token})

    def form_valid(self, form):
        msg = _("Thanks for signing up! We'll let you know when we have more "
                "information. In the meantime, you can update your name or "
                "leave us a message if you feel like it.")
        messages.success(self.request, msg)
        return super(CreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['interest_form'] = context['form']
        return context


class TokenMixin(object):
    def get_object(self):
        return Interest.objects.get_from_token(self.kwargs['token'])

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(TokenMixin, self).dispatch(request, *args, **kwargs)
        except BadSignature:
            return render(request, 'interests/token_error.html')


class UpdateView(TokenMixin, generic.UpdateView):
    template_name = 'interests/update.html'
    form_class = UpdateInterestForm

    def get_success_url(self):
        return reverse('update-interest', kwargs={'token': self.object.token})

    def form_valid(self, form):
        messages.success(self.request, _("Your information has been updated."))
        return super(UpdateView, self).form_valid(form)


class DeleteView(TokenMixin, generic.DeleteView):
    template_name = 'interests/delete.html'
    model = Interest
    success_url = reverse_lazy('home')
