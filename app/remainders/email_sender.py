from datetime import date

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
    print('Started to send emails...')
    remainders = Remainder.objects.all()

    for remainder in remainders:
        remainder_date = remainder.remainder_date
        days_to_remainder = (remainder_date - date.today()).days

        # Send emails for remainders that are less or equal than 30 days to remainder date
        if days_to_remainder <= 30:
            try:
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
                        remainder.sent_check = None
                        remainder.save()
                    else:
                        remainder.delete()

            except Exception as error:
                print(error)

    print('Remainders have been sent.')


def start():
    scheduler = BackgroundScheduler(job_defaults={'max_instances': 3})
    # Later change to hours=6
    scheduler.add_job(send_emails, 'interval', hours=5)
    scheduler.start()

# TODO
# - Stworzyć komendę do tworzenia remaindera na dzisiaj
# - Przeprojektować remaindery, robić query tylko remainderów, które są maks na 30 dni wprzód, a nie wszystkie
# - Zmieniłem interwał na godziny
# - Może jakiś refacktoring, email generator do osobnego modułu
# - Może zrobić całkowicie nową appkę dla email?
