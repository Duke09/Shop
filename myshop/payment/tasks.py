from io import BytesIO
from celery import task, shared_task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from orders.models import Order

@task(bind=True, max_retries=3, default_retry_delay=2*60, ignore_result=True)
def payment_completed(self, order_id):
    """
    Task to send an e-mail notification when an order
    is successfully created.
    """
    try:
        order = Order.objects.get(id=order_id)
        # create invoice e-mail
        subject = f'My Shop -- EE Invoice no. {order.id}'
        message = 'Please, find attached incvoce for your recent purchase'
        email = EmailMessage(subject,
                            message,
                            'admin@myshop.com',
                            [order.email])

        # generate PDF
        html = render_to_string(
            'orders/order/pdf.html',
            {
                'order': order
            }
        )
        out = BytesIO()
        stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
        weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

        # addtach PDF file
        email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')

        # send e-mail
        email.send()
    except Exception as exc:
        raise self.retry(exc=exc)