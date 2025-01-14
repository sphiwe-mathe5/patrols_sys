# admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .models import Resident, PaymentStatus

@admin.register(PaymentStatus)
class PaymentStatusAdmin(admin.ModelAdmin):
    list_display = ('resident', 'month', 'is_paid', 'payment_status')
    list_filter = ('month', 'is_paid')
    search_fields = ('resident__surname',)
    actions = ['mark_as_paid', 'populate_next_month']
    
    def payment_status(self, obj):
        if obj.is_paid:
            return format_html('<span style="color: green;">Paid</span>')
        return format_html('<span style="color: red;">Pending</span>')
    
    def mark_as_paid(self, request, queryset):
        queryset.update(is_paid=True)
        self.message_user(request, f"{queryset.count()} payments marked as paid.")
    mark_as_paid.short_description = "Mark selected payments as paid"
    
    def populate_next_month(self, request, queryset):
        current_month = datetime.today().replace(day=1)
        next_month = current_month + relativedelta(months=1)
        
        # Get all residents
        residents = Resident.objects.all()
        
        # Check if next month entries already exist
        if PaymentStatus.objects.filter(month=next_month).exists():
            self.message_user(
                request, 
                "Payments for next month already exist!", 
                messages.WARNING
            )
            return
            
        # Create new payment status for each resident
        new_statuses = []
        for resident in residents:
            new_statuses.append(PaymentStatus(
                resident=resident,
                month=next_month,
                is_paid=False
            ))
        
        PaymentStatus.objects.bulk_create(new_statuses)
        self.message_user(
            request, 
            f"Successfully created {len(new_statuses)} payment entries for {next_month.strftime('%B %Y')}",
            messages.SUCCESS
        )
    populate_next_month.short_description = "Populate payments for next month"

@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ('surname', 'house_number', 'street_name', 'place_name')
    search_fields = ('surname', 'street_name', 'place_name')
    ordering = ('surname',)

