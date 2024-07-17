from datetime import date, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import EmailMessage

from core.models import Remainder


def generate_email_msg(remainder):
    message_body = f"""
Hi {remainder.user.name}!
We wanted to remaind you, that {remainder.title} happens on {remainder.remainder_date}.

Remainder description:
{remainder.description}
"""

    if remainder.permanent is False:
        message_body = message_body + 'This remainder is not permanent and will be deleted after the date of the remainder.'

    return EmailMessage(f'{remainder.title}', message_body, to=[remainder.user.email])


def send_emails():
    print('Started sending emails...')
    # Search for remainders that are 30 days from happening
    today = date.today()
    date_to_search = today + timedelta(days=30)
    remainders = Remainder.objects.filter(remainder_date__lte=date_to_search)

    for remainder in remainders:
        try:
            remainder_date = remainder.remainder_date
            days_to_remainder = (remainder_date - today).days

            # Send emails for remainders that are less or equal than 30 days to remainder date
            print(f'Remainder {remainder.id} is being processed.')
            if days_to_remainder > 7 and remainder.sent_check != 'month':
                generate_email_msg(remainder).send()
                remainder.sent_check = 'month'
                remainder.save()

            elif 7 >= days_to_remainder > 3 and remainder.sent_check != 'week':
                generate_email_msg(remainder).send()
                remainder.sent_check = 'week'
                remainder.save()

            elif 3 >= days_to_remainder > 1 and remainder.sent_check != 'three_days':
                generate_email_msg(remainder).send()
                remainder.sent_check = 'three_days'
                remainder.save()

            elif days_to_remainder == 1 and remainder.sent_check != 'one_day':
                generate_email_msg(remainder).send()
                remainder.sent_check = 'one_day'
                remainder.save()

            elif not days_to_remainder:
                generate_email_msg(remainder).send()
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

# Notatki
# - Przeprojektować remaindery, robić query tylko remainderów, które są maks na 30 dni wprzód, a nie wszystkie
# - Może jakiś refacktoring, email generator do osobnego modułu
#   Może zrobić tak, że będę robił query do bazy danych o każdy step, 7 dni, 3 dni itd, zamiast if else
# - Może zamiast permanent dać is_active? Żeby go od razu nie usuwać, tylko dezaktywować?
