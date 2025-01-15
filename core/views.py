from django.utils import timezone
from datetime import datetime
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import ListView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import  IntegerField
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .models import Resident, PaymentStatus
from .forms import ResidentForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

def index(request):
    if request.method == 'POST':
        form = ResidentForm(request.POST)
        if form.is_valid():
            resident = form.save()

            current_month = datetime.today().replace(day=1)
            PaymentStatus.objects.create(
                resident=resident,
                month=current_month,
                is_paid=False
            )
            return redirect('resident_list')

    else:
        form = ResidentForm()

    return render(request, 'core/index.html', {'form': form})


class ResidentCreateView(CreateView):
    model = Resident
    form_class = ResidentForm
    template_name = 'core/create_resident.html'
    success_url = reverse_lazy('resident_list')

    def form_valid(self, form):
        response = super().form_valid(form)

        current_month = datetime.today().replace(day=1)
        PaymentStatus.objects.create(resident=self.object,
                                     month=current_month,
                                     is_paid=False)
        return response


class ResidentListView(ListView):
    model = PaymentStatus
    template_name = 'core/resident_list.html'
    context_object_name = 'payments'

    def get_queryset(self):

        month_str = self.request.GET.get('month')

        if month_str:
            try:
                current_month = datetime.strptime(month_str, '%Y-%m').replace(day=1)
            except ValueError:
                current_month = timezone.now().replace(day=1)
        else:
            current_month = timezone.now().replace(day=1)


        queryset = PaymentStatus.objects.filter(
            month=current_month
        ).select_related('resident')

        surname = self.request.GET.get('surname', '').strip()
        house_number = self.request.GET.get('house_number', '').strip()
        payment_status = self.request.GET.get('payment_status', '')

        if surname:
            queryset = queryset.filter(resident__surname__icontains=surname)
        if house_number:
            queryset = queryset.filter(resident__house_number__icontains=house_number)
        if payment_status:
            is_paid = payment_status == 'paid'
            queryset = queryset.filter(is_paid=is_paid)

        return queryset.order_by(
            'resident__street_name',
            Cast('resident__house_number', IntegerField())
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        month_str = self.request.GET.get('month')
        if month_str:
            try:
                current_month = datetime.strptime(month_str, '%Y-%m').replace(day=1)
            except ValueError:
                current_month = timezone.now().replace(day=1)
        else:
            current_month = timezone.now().replace(day=1)

        prev_month = current_month - relativedelta(months=1)
        next_month = current_month + relativedelta(months=1)

        context.update({
            'current_month': current_month,
            'prev_month': prev_month,
            'next_month': next_month,
            'prev_month_link': prev_month.strftime('%Y-%m'),
            'next_month_link': next_month.strftime('%Y-%m'),
            'has_next': PaymentStatus.objects.filter(month=next_month).exists(),
            'has_prev': PaymentStatus.objects.filter(month=prev_month).exists(),

            'search_surname': self.request.GET.get('surname', ''),
            'search_house_number': self.request.GET.get('house_number', ''),
            'search_payment_status': self.request.GET.get('payment_status', ''),
        })

        return context

class PaymentActionView(View):
    @method_decorator(require_POST)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, payment_id):
        payment = get_object_or_404(PaymentStatus, id=payment_id)
        payment.is_paid = True
        payment.save()
        current_month = request.GET.get('month', timezone.now().strftime('%Y-%m'))

        messages.success(request, f"Payment for {payment.resident.surname} has been marked as paid.")
        return redirect(f"{reverse('resident_list')}?month={current_month}")

class ResidentDeleteView(View):
    @method_decorator(require_POST)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, resident_id):
        resident = get_object_or_404(Resident, id=resident_id)
        resident_name = resident.surname
        resident.delete()

        current_month = request.GET.get('month', timezone.now().strftime('%Y-%m'))

        messages.success(request, f"Resident {resident_name} has been deleted.")
        return redirect(f"{reverse('resident_list')}?month={current_month}")


def is_admin(user):
    return user.is_staff
