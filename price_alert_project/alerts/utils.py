# alerts/utils.py

from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_alert_email(alert, current_price):
    subject = f"Price Alert: {alert.cryptocurrency} has reached your target price!"
    message = f"""
    Dear {alert.user.username},

    Your price alert for {alert.cryptocurrency} has been triggered.

    Target Price: {alert.target_price} INR
    Current Price: {current_price:.2f} INR

    Initial Price: {alert.initial_price} INR
    
    Please log in to your account for more details.

    Best regards,
    Rohan Srivastav
    """
    
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [alert.user.email]
    
    try:
        send_mail(subject, message, from_email, recipient_list)
        logger.info(f"Alert email sent to {alert.user.email} for {alert.cryptocurrency}")
    except Exception as e:
        logger.error(f"Failed to send alert email to {alert.user.email}: {str(e)}")