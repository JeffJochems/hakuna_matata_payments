"""
A ticket payment management system leveraging mailchimp subscriptions to provision ticket payment requests from mollie.
This script performs the following steps to send and register payments:

1. Collect the current mailchimp subscriptions
2. Collect the active mollie payment requests
3. For attendees that have a newly completed payment request: set the payment status as complete in mailchimp
4. For attendees that have a new subscription in mailchimp: collect a new payment request URL and register this URL in mailchimp
"""

import os
import logging
from logging.handlers import TimedRotatingFileHandler
from utils.mailchimp_client import MailchimpClient
from utils.payment_client import PaymentClient


# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s;%(levelname)s;%(message)s', "%Y-%m-%d %H:%M:%S")
logging_handler = TimedRotatingFileHandler(os.path.dirname(os.path.abspath(__file__)) + '/logs/hakuna_matata_payments_prod.log', when='d', interval=1, backupCount=14)
logging_handler.setLevel(logging.INFO)
logging_handler.setFormatter(formatter)
logger.addHandler(logging_handler)


def main():
    logging.info("-- Script started")

    # Get API credentials from environment variables
    mailchimp_api_server = os.getenv("MAILCHIMP_API_SERVER")
    mailchimp_api_key = os.getenv("MAILCHIMP_API_KEY")
    mailchimp_campaign_list_id = os.getenv("MAILCHIMP_CAMPAIGN_LIST_ID")
    mailchimp_verification_wf_id = os.getenv("MAILCHIMP_VERIFICATION_WF_ID")
    mailchimp_verification_wf_email_id = os.getenv("MAILCHIMP_VERIFICATION_WF_EMAIL_ID")
    mollie_api_url = os.getenv("MOLLIE_API_URL")
    mollie_api_key = os.getenv("MOLLIE_API_KEY")
    mollie_api_partner_id = os.getenv("MOLLIE_API_PARTNER_ID")
    mollie_api_profile_id = os.getenv("MOLLIE_API_PROFILE_ID")

    # Initialize API clients
    mailchimp_api_client = MailchimpClient(mailchimp_api_server, mailchimp_api_key, mailchimp_campaign_list_id, mailchimp_verification_wf_id, mailchimp_verification_wf_email_id)
    payment_api_client = PaymentClient(mollie_api_url, mollie_api_key, mollie_api_partner_id, mollie_api_profile_id) 

    # 1. Collect current mailchimp subscriptions
    attendees = mailchimp_api_client.retrieve_subscribed_attendees() 

    # 2. Collect payment links
    payment_links = payment_api_client.retrieve_payment_links()

    # 3. Set newly paid statuses
    register_complete_payments(mailchimp_api_client, attendees, payment_links)
    # mailchimp_api_client.register_paypal_payments(attendees, collected_payments)

    # 4. Send new payment requests and register payment pending statuses
    send_new_payment_requests(mailchimp_api_client, payment_api_client, attendees)

    logging.info("-- script completed")


def register_complete_payments(mailchimp_api_client: MailchimpClient, attendees: list, payment_links: list) -> None:
    """
    Registers complete payments as complete in mailchimp for attendees with a pending payment status and paid status of the payment link.
    :param mailchimp_api_clientL: The mailchimp API client facilitating communication with mailchimp
    :param attendees: The list of attendees to verify and register complete paiments for
    :param payment_links: The list of published payment links that are either pending or complete
    """
    performed_registration = False
    for attendee in attendees:
        if attendee.customer_journey == "payment pending":
            for payment_link in payment_links:
                if attendee.payment_link_id == payment_link.id and payment_link.is_paid():
                    mailchimp_api_client.register_complete_payment(attendee)
                    performed_registration = True

    if not performed_registration:
        logging.info("No new complete payments have been found")

def send_new_payment_requests(mailchimp_api_client: MailchimpClient, payment_api_client: PaymentClient, attendees: list) -> None:
    """
    Sends payment requests for new attendees.
    :param mailchimp_api_client: The mailchimp API client facilitating communication with mailchimp
    :param payment_api_client: The mollie payment API client facilitating communication with Mollie
    :param attendees: The list of attendees to check and possibly send new payment requests for
    """
    performed_new_payment_request = False
    for attendee in attendees:
        if attendee.customer_journey == "new" and attendee.amount_tickets > 0:
            payment_link = payment_api_client.create_payment_link(attendee.first_name, attendee.last_name, attendee.email, attendee.amount_tickets, attendee.value_tickets)
            mailchimp_api_client.register_pending_payment(attendee, payment_link)
            performed_new_payment_request = True
    
    if not performed_new_payment_request:
        logging.info("No new attendees have subscribed")

if __name__ == "__main__":
    main()
