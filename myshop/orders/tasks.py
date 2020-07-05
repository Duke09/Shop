from celery import task, shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task(bind=True, max_retries=3, default_retry_delay=2*60, ignore_result=True)
def order_created(self, order_id):
    """
    Task to send an email notification
    when an order is successfully created.
    """
    try:
        order = Order.objects.get(id=order_id)
        subject = f'Order no. {order.id}'
        message = f'Dear {order.first_name},\n\n'\
                  f'You have successfully placed an order.'\
                  f'Your order ID is {order.id}.'
        
        res = send_mail(
            subject,
            message,
            'monday.ent9@gmail.com',
            [order.email],
            fail_silently=False
        )
    except Exception as exc:
        raise self.retry(exc=exc)