from django.core.mail import EmailMessage


def generate_remainder_email(remainder, days_until_remainder):
    message_title = f"{remainder.title} happens in {days_until_remainder} days"
    message_body = f"""
Hi {remainder.user.name}!
We wanted to remind you, that {remainder.title} happens in {days_until_remainder} days, on {remainder.remainder_date}.

Remainder description:
{remainder.description}
"""

    if remainder.permanent is False:
        message_body = message_body + '\n' + 'Important Note: This remainder is not permanent and will be deleted after the date of the remainder.'

    return EmailMessage(f'{message_title}', message_body, to=[remainder.user.email])
