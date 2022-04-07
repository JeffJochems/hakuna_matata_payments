"""
A ticket payment management system leveraging mailchimp subscriptions to provision ticket requests
This script performs the following steps to send and register payments:

1. Retrieve subscribed attendees from mailchimp

TODO: rewrite documentation of payment process
2. Send payment requests:
    2.1. Check if these attendees have complete or pending payment status
    2.2. Send payment request to attendees without payment and set their payment status to pending (set their payment request link)

3. Register collected payments:
    3.1. Check if paypal payment is complete
    3.2. If payment is complete set payment status to complete
"""

import os
from utils.mailchimp_client import MailchimpClient
from utils.payment_client import PaymentClient


def main():
    # Get api credentials from operating system
    mailchimp_api_server = os.getenv("MAILCHIMP_API_SERVER")
    mailchimp_api_key = os.getenv("MAILCHIMP_API_KEY")
    mailchimp_campaign_list_id = os.getenv("MAILCHIMP_CAMPAIGN_LIST_ID")
    # paypal_server_url = os.getenv("PAYPAL_SERVER_URL")
    # paypal_client_id = os.getenv("PAYPAL_CLIENT_ID")
    # paypal_api_secret = os.getenv("PAYPAL_API_SECRET")
    mollie_api_url = os.getenv("MOLLIE_API_URL")
    mollie_api_key = os.getenv("MOLLIE_API_KEY")
    mollie_api_partner_id = os.getenv("MOLLIE_API_PARTNER_ID")
    mollie_api_profile_id = os.getenv("MOLLIE_API_PROFILE_ID")

    # Initialize API clients
    mailchimp_api_client = MailchimpClient(mailchimp_api_server, mailchimp_api_key, mailchimp_campaign_list_id)
    payment_api_client = PaymentClient(mollie_api_url, mollie_api_key, mollie_api_partner_id, mollie_api_profile_id) 

    # 1. Collect current mailchimp subscriptions
    attendees = mailchimp_api_client.retrieve_subscribed_attendees() 

    # 2. Collect payment links
    payment_links = payment_api_client.retrieve_payment_links()

    # 3. Set newly paid statuses
    register_complete_payments(mailchimp_api_client, attendees, payment_links)
    # mailchimp_api_client.register_paypal_payments(attendees, collected_payments)

    # # 4. Send new payment requests and register payment pending statuses
    send_new_payment_requests(mailchimp_api_client, payment_api_client, attendees)
    # new_payment_requests = paypal_api_client.get_payment_requests(attendees)
    # payment_api_client.create_payment_link("Testvoornaam", "Testachternaam", "Testemail@mail.com")
    # mailchimp_api_client.set_payment_requests(attendees, new_payment_requests)


def register_complete_payments(mailchimp_api_client, attendees, payment_links):
    """
    """
    for attendee in attendees:
        if attendee.customer_journey == "payment pending":
            for payment_link in payment_links:
                if attendee.payment_link_id == payment_link.id and payment_link.is_paid():
                    mailchimp_api_client.register_complete_payment(attendee)

def send_new_payment_requests(mailchimp_api_client, payment_api_client, attendees):
    """
    """
    for attendee in attendees:
        if attendee.customer_journey == "new":
            payment_link = payment_api_client.create_payment_link(attendee.first_name, attendee.last_name, attendee.email)
            mailchimp_api_client.register_pending_payment(attendee, payment_link)

if __name__ == "__main__":
    main()
