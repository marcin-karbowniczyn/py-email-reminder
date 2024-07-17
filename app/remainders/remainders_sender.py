from datetime import date, timedelta

from apscheduler.schedulers.background import BackgroundScheduler

from core.models import Remainder
from remainders.emails import generate_remainder_email


def send_emails():
    print('Started sending remainders...')
    # Search for remainders that are 30 days from happening
    today = date.today()
    date_to_search = today + timedelta(days=30)
    remainders = Remainder.objects.filter(remainder_date__lte=date_to_search)

    for remainder in remainders:
        try:
            remainder_date = remainder.remainder_date
            days_until_remainder = (remainder_date - today).days

            # Send emails for remainders that are less or equal than 30 days to remainder date
            print(f'Remainder {remainder.id} is being processed.')
            if days_until_remainder > 7 and remainder.sent_check != 'month':
                generate_remainder_email(remainder, days_until_remainder).send()
                remainder.sent_check = 'month'
                remainder.save()

            elif 7 >= days_until_remainder > 3 and remainder.sent_check != 'week':
                generate_remainder_email(remainder, days_until_remainder).send()
                remainder.sent_check = 'week'
                remainder.save()

            elif 3 >= days_until_remainder > 1 and remainder.sent_check != 'three_days':
                generate_remainder_email(remainder, days_until_remainder).send()
                remainder.sent_check = 'three_days'
                remainder.save()

            elif days_until_remainder == 1 and remainder.sent_check != 'one_day':
                generate_remainder_email(remainder, days_until_remainder).send()
                remainder.sent_check = 'one_day'
                remainder.save()

            elif not days_until_remainder:
                generate_remainder_email(remainder, days_until_remainder).send()
                if remainder.permanent:
                    remainder.remainder_date = date(remainder_date.year + 1, remainder_date.month, remainder_date.day)
                    remainder.sent_check = 'None'
                    remainder.save()
                else:
                    remainder.delete()

        except Exception as error:
            print(error)

    print('Remainders have been sent.')


def start():
    scheduler = BackgroundScheduler(job_defaults={'max_instances': 2})
    scheduler.add_job(send_emails, 'interval', seconds=10)
    scheduler.start()
