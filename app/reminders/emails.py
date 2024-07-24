from django.core.mail import EmailMessage


def how_many_days_to_reminder_string(days_until_reminder):
    if days_until_reminder < 1:
        return 'today'
    elif days_until_reminder == 1:
        return 'tomorrow'
    else:
        return f"in {days_until_reminder} days"


def generate_reminder_email(reminder, days_until_reminder):
    days_information = how_many_days_to_reminder_string(days_until_reminder)
    message_title = f"{reminder.title} happens {days_information}"

    message_body = f"""
Hi {reminder.user.name}!
We wanted to remind you, that {reminder.title} happens {days_information}, on {reminder.reminder_date}.

"""
    if reminder.description:
        message_body = message_body + '\n' + 'Reminder description' + '\n' + reminder.description + '\n'

    if reminder.permanent is False:
        message_body = message_body + '\n' + 'Important Note: This reminder is not permanent and will be deleted after the date of the reminder.'

    return EmailMessage(message_title, message_body, to=[reminder.user.email])
