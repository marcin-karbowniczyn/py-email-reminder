from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import EmailMessage


def send_emails():
    print('Starting sending remainders...')

    try:
        EmailMessage('Test email', 'Test email', to=['marcin.karbowniczyn@gmail.com']).send()
    except Exception as error:
        print(str(error))

    print('Remainders has been sent.')


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_emails, 'interval', seconds=30)
    scheduler.start()
