from django.core.mail import EmailMessage


def how_many_days_to_remainder_string(days_until_remainder):
    if days_until_remainder < 1:
        return 'today'
    elif days_until_remainder == 1:
        return 'tomorrow'
    else:
        return f"in {days_until_remainder} days"


def generate_remainder_email(remainder, days_until_remainder):
    days_information = how_many_days_to_remainder_string(days_until_remainder)
    message_title = f"{remainder.title} happens {days_information}"

    message_body = f"""
Hi {remainder.user.name}!
We wanted to remind you, that {remainder.title} happens {days_information}, on {remainder.remainder_date}.

Remainder description:
{remainder.description}
"""

    if remainder.permanent is False:
        message_body = message_body + '\n' + 'Important Note: This remainder is not permanent and will be deleted after the date of the remainder.'

    return EmailMessage(message_title, message_body, to=[remainder.user.email])
