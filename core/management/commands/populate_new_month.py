# Create a management command to populate new month
# management/commands/populate_new_month.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta
from core.models import Resident, PaymentStatus

class Command(BaseCommand):
    help = 'Populates payment status for all residents for the new month'

    def handle(self, *args, **options):
        current_month = datetime.today().replace(day=1)
        next_month = current_month + relativedelta(months=1)
        
        # Get all residents
        residents = Resident.objects.all()
        
        # Create new payment status for each resident
        new_statuses = []
        for resident in residents:
            new_statuses.append(PaymentStatus(
                resident=resident,
                month=next_month,
                is_paid=False
            ))
        
        PaymentStatus.objects.bulk_create(new_statuses)
        self.stdout.write(self.style.SUCCESS(f'Successfully populated {len(new_statuses)} payment statuses for {next_month.strftime("%B %Y")}'))