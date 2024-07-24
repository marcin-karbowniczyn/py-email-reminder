from datetime import date, timedelta

from apscheduler.schedulers.background import BackgroundScheduler

from core.models import Reminder
from reminders.emails import generate_reminder_email


def send_emails():
    """ Function for sending reminders and updating checks """
    print('Started sending reminders...')
    # Search for reminders that are 30 days from happening
    today = date.today()
    date_to_search = today + timedelta(days=30)
    reminders = Reminder.objects.filter(reminder_date__lte=date_to_search)

    for reminder in reminders:
        try:
            reminder_date = reminder.reminder_date
            days_until_reminder = (reminder_date - today).days

            # Send emails for reminders that are less or equal than 30 days to reminder date
            print(f'Reminder {reminder.id} is being processed.')
            if days_until_reminder > 7 and reminder.sent_check != 'month':
                generate_reminder_email(reminder, days_until_reminder).send()
                reminder.sent_check = 'month'
                reminder.save()

            elif 7 >= days_until_reminder > 3 and reminder.sent_check != 'week':
                generate_reminder_email(reminder, days_until_reminder).send()
                reminder.sent_check = 'week'
                reminder.save()

            elif 3 >= days_until_reminder > 1 and reminder.sent_check != 'three_days':
                generate_reminder_email(reminder, days_until_reminder).send()
                reminder.sent_check = 'three_days'
                reminder.save()

            elif days_until_reminder == 1 and reminder.sent_check != 'one_day':
                generate_reminder_email(reminder, days_until_reminder).send()
                reminder.sent_check = 'one_day'
                reminder.save()

            elif not days_until_reminder:
                generate_reminder_email(reminder, days_until_reminder).send()
                if reminder.permanent:
                    reminder.reminder_date = date(reminder_date.year + 1, reminder_date.month, reminder_date.day)
                    reminder.sent_check = 'None'
                    reminder.save()
                else:
                    reminder.delete()

        except Exception as error:
            print(error)

    print('Reminders have been sent.')


def delete_past_reminders():
    """ Function for deleting all reminders leftovers that hasn't been deleted for any reason """
    today = date.today()
    Reminder.objects.filter(reminder_date__lt=today, permanent=False).delete()
    print('Non-permanent reminders from the past has been deleted')


def start():
    scheduler = BackgroundScheduler(job_defaults={'max_instances': 2})
    # scheduler.add_job(send_emails, 'interval', seconds=6)
    # scheduler.add_job(delete_past_reminders, 'interval', hours=5)
    scheduler.start()
