import mailchimp_marketing as MailchimpMarketing

from utils.attendee import Attendee

class MailchimpClient:
    """
    A mailchimp client able to communicate with the mailchimp marketing API.
    This marketing api client is based on the following rest API documentation: https://github.com/mailchimp/mailchimp-marketing-python#installation--usage
    """

    def __init__(self, server, api_key, campaign_list_id) -> None:
        """
        Initializes the mailchimp marketeing API client.
        """
        self.server = server
        self.api_key = api_key
        self.campaign_list_id = campaign_list_id

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
        members_response = self.client.lists.get_list_members_info(list_id=self.campaign_list_id)
        attendees = []
        for member in members_response["members"]:
            # TODO: Fill attendee info
            id = ""
            name = ""
            payment_status = ""
            attendees.append(Attendee(id, name, payment_status))
        print(attendees)
        return attendees

    def test_connection(self) -> str:
        """
        Tests the API connection of the client
        """
        response = self.client.ping.get()
        print(response)