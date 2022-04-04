"""
A ticket payment management system leveraging mailchimp subscriptions to provision ticket requests
This script performs the following steps to send and register payments:

1. Retrieve subscribed attendees from mailchimp

2. Send payment requests:
    2.1. Check if these attendees have complete or pending payment status
    2.2. Send payment request to attendees without payment and set their payment status to pending (set their payment request link)

3. Register collected payments:
    3.1. Check if paypal payment is complete
    3.2. If payment is complete set payment status to complete
"""

import os
from utils.mailchimp_client import MailchimpClient
from utils.paypal_client import PaypalClient


def main():
    # Get api credentials from operating system
    mailchimp_api_server = os.getenv("MAILCHIMP_API_SERVER")
    mailchimp_api_key = os.getenv("MAILCHIMP_API_KEY")
    mailchimp_campaign_list_id = os.getenv("MAILCHIMP_CAMPAIGN_LIST_ID")
    paypal_server_url = os.getenv("PAYPAL_SERVER_URL")
    paypal_client_id = os.getenv("PAYPAL_CLIENT_ID")
    paypal_api_secret = os.getenv("PAYPAL_API_SECRET")

    # Initialize API clients
    mailchimp_api_client = MailchimpClient(mailchimp_api_server, mailchimp_api_key, mailchimp_campaign_list_id)
    paypal_api_client = PaypalClient(paypal_server_url, paypal_client_id, paypal_api_secret)

    # 1. Collect current mailchimp subscriptions
    attendees = mailchimp_api_client.retrieve_subscribed_attendees() 

    # # 2. Register collected payments
    # collected_payments = paypal_api_client.retrieve_collected_payments(attendees)
    # mailchimp_api_client.register_paypal_payments(attendees, collected_payments)

    # # 3. Send payment requests
    # new_payment_requests = paypal_api_client.get_payment_requests(attendees)
    # mailchimp_api_client.set_payment_requests(attendees, new_payment_requests)


if __name__ == "__main__":
    main()
