from optparse import Values
import requests
import logging
from mollie.api.client import Client
from utils.payment_link import PaymentLink

class PaymentClient:
    """
    A mollie payments client able to communicate with the mollie API.
    This marketing api client is based on the following rest API documentation: https://docs.mollie.com
    """

    def __init__(self, mollie_api_url: str, mollie_api_key: str, mollie_api_partner_id: str, mollie_api_profile_id: str) -> None:
        """ 
        Initializes the mollie payment client api and configures its parameters.
        :param mollie_api_url: The url of the mollie api server
        :param mollie_api_key: The API key of the mollie user
        :param mollie_api_partner_id: The user partner id of the mollie user 
        :param mollie_api_profile_id: The user profile id of the mollie user
        """
        self.mollie_api_url = mollie_api_url
        self.mollie_api_key = mollie_api_key
        self.mollie_api_partner_id = mollie_api_partner_id
        self.mollie_api_profile_id = mollie_api_profile_id

        self.mollie_api_headers = requests.structures.CaseInsensitiveDict()
        self.mollie_api_headers["Authorization"] = f"Bearer {self.mollie_api_key}"
        self.client = Client()
        self.client.set_api_key(self.mollie_api_key)

    def retrieve_payment_links(self) -> list:
        """
        Retrieves the active payment links from mollie.
        """
        response_payment_links = self.client.payment_links.list()
        payment_links = [payment_link_dict_to_obj(payment_link_dict) for payment_link_dict in response_payment_links["_embedded"]["payment_links"]]
        logging.info(f"Retrieved a list of {len(payment_links)} payment links from Mollie")

        return payment_links

    def create_payment_link(self, first_name: str, last_name: str, email: str, amount: int, value: float) -> PaymentLink:
        """
        Creates a new payment link for a new attendee.
        :param first_name: The first name of the new attendee
        :param last_name: The last name of the new attendee
        :param email: The email adress of the new attendee
        """
        payment_amount = {"value": "{:.2f}".format(value), "currency": "EUR"}
        description = f"{amount} Hakuna Matata zondag tickets inclusief eten ({value} eu) voor: {first_name} {last_name} \n verstuurd naar {email}"
        payment_link_dict = self.client.payment_links.create({"description" : description, "amount" : payment_amount, "expiresAt": "2022-06-07T11:00:00+00:00"})
        payment_link = payment_link_dict_to_obj(payment_link_dict)
        logging.info(f"Created a mollie payment link for {first_name} {last_name}, {email}, {amount} tickets, {value} eu")

        return payment_link


def payment_link_dict_to_obj(payment_link_dict: dict) -> PaymentLink:
    """
    Collects the information from a payment link dictionairy and instantiates a payment link object.
    :param payment_link_dict: The dictionairy to instantiate an object from
    """
    id = payment_link_dict["id"]
    payment_link_url = payment_link_dict["_links"]["paymentLink"]["href"]
    paid_at = payment_link_dict["paidAt"]
    description = payment_link_dict["description"]
    payment_link = PaymentLink(id, payment_link_url, paid_at, description)
    return payment_link