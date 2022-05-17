import logging
import mailchimp_marketing as MailchimpMarketing

from utils.attendee import Attendee

class MailchimpClient:
    """
    A mailchimp client able to communicate with the mailchimp marketing API.
    This marketing api client is based on the following rest API documentation: https://github.com/mailchimp/mailchimp-marketing-python#installation--usage
    """

    def __init__(self, server, api_key, campaign_list_id, verification_wf_id, verification_wf_email_id) -> None:
        """
        Initializes the mailchimp marketeing API client.
        """
        self.server = server
        self.api_key = api_key
        self.campaign_list_id = campaign_list_id
        self.verification_wf_id = verification_wf_id
        self.verification_wf_email_id = verification_wf_email_id

        self.client = MailchimpMarketing.Client()
        self.client.set_config({
            "api_key": api_key,
            "server": server
        })

    def retrieve_subscribed_attendees(self) -> list:
        """
        Retrieves the subscirbed attendees from mailchimp
        :returns: a list of subscribed attendees
        """
        members_response = self.client.lists.get_list_members_info(list_id=self.campaign_list_id, count=1000)

        attendees = []

        for member in members_response["members"]:
            # Collect attendee properties
            id = member["id"]
            list_id = member["list_id"]
            unique_email_id = member["unique_email_id"]
            email = member["email_address"]
            first_name = member["merge_fields"]["FNAME"]
            last_name = member["merge_fields"]["LNAME"]
            payment_link = member["merge_fields"]["PAY_LINK"]
            payment_link_id = member["merge_fields"]["PAY_LINK_I"]
            amount_tickets = member["merge_fields"]["MERGE4"]
            customer_journey = customer_journey_from_mailchimp_tags(member["tags"])

            attendees.append(Attendee(id, list_id, email, first_name, last_name, unique_email_id, payment_link, payment_link_id, customer_journey, amount_tickets))

        logging.info(f"Retrieved a list of {len(attendees)} attendees")

        return attendees

    def test_connection(self) -> str:
        """
        Tests the API connection of the client
        """
        response = self.client.ping.get()
        print(response)

    def register_pending_payment(self, attendee, payment_link) -> None:
        """
        Registers a pending payment in mailchimp by updating the customer journey tags and payment link (id) fields
        :param attendee: the attendee to update
        :param payment_link: the payment link to register
        """
        # set payment link and payment link id
        self.client.lists.update_list_member(attendee.list_id, attendee.id, {"merge_fields": {"PAY_LINK": payment_link.payment_link_url, "PAY_LINK_I": payment_link.id}})
        logging.info(f"Configured a payment link for {attendee.first_name} {attendee.last_name} in mailchimp")

        # add payment pending tag
        self.client.lists.update_list_member_tags(attendee.list_id, attendee.id, {"tags": [{"name": "payment pending", "status": "active"}]})
        logging.info(f"Set the payment_pending tag of  {attendee.first_name} {attendee.last_name} in mailchimp to active")

    def register_complete_payment(self, attendee) -> None:
        """
        Registers a complete payment in mailchimp by updating the customer journey tags
        :param attendee: the attendee to update
        """
        # add paid tag
        self.client.lists.update_list_member_tags(attendee.list_id, attendee.id, {"tags": [
            {"name": "payment pending", "status": "inactive"},
            {"name": "payment complete", "status": "active"}
            ]})
        logging.info(f"Set the payment_pending tag of  {attendee.first_name} {attendee.last_name} in mailchimp to inactive and the payment_complete tag to active")

        # trigger thanks for paying event
        self.client.automations.add_workflow_email_subscriber(self.verification_wf_id, self.verification_wf_email_id, {"email_address": attendee.email})
        logging.info(f"Triggered a thanks for paying mail for  {attendee.first_name} {attendee.last_name} in mailchimp to active")


def customer_journey_from_mailchimp_tags(tags: list):
    """ 
    Comverts a list of mailchimp tags to the customer journey step
    :param tags: The tags associated with a member
    :returns: a customer journey step (string)
    """
    if len(tags) == 0:
        return "new"
    elif len(tags) == 1 and tags[0]['name'] == "payment pending":
        return "payment pending"
    elif len(tags) == 1 and tags[0]['name']  == "payment complete":
        return "payment complete"
    else:
        raise ValueError(f"Customer journey could not be obtained from mailchimp tags: {tags}")