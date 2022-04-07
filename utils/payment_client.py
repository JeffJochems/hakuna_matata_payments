import requests
from mollie.api.client import Client
from utils.payment_link import PaymentLink

class PaymentClient:
    """
    """

    def __init__(self, mollie_api_url: str, mollie_api_key: str, mollie_api_partner_id: str, mollie_api_profile_id: str) -> None:
        """ 
        """
        self.mollie_api_url = mollie_api_url
        self.mollie_api_key = mollie_api_key
        self.mollie_api_partner_id = mollie_api_partner_id
        self.mollie_api_profile_id = mollie_api_profile_id

        self.mollie_api_headers = requests.structures.CaseInsensitiveDict()
        self.mollie_api_headers["Authorization"] = f"Bearer {self.mollie_api_key}"
        self.client = Client()
        self.client.set_api_key(self.mollie_api_key)
        self.default_amount = {"currency": "EUR", "value": "10.00"}

    def retrieve_payment_links(self) -> list:
        """
        TODO: Change to mollie client implementation
        """
        payment_links = []

        url = self.mollie_api_url + "/payment-links"
        payment_links_leftover = True
        while payment_links_leftover:
            # perform a mollie API request
            response = requests.get(url=url, headers=self.mollie_api_headers)
            json_response = response.json()

            # Create payment link object
            for payment_link_dict in json_response["_embedded"]["payment_links"]:
                payment_links.append(payment_link_dict_to_obj(payment_link_dict))
            
            if json_response["_links"]["next"] is None:
                payment_links_leftover = False
            else:
                url = json_response["_links"]["next"]

        return payment_links

    def create_payment_link(self, first_name, last_name, email) -> PaymentLink:
        """
        """
        description = f"Hakuna Matata zondag ticket inclusief eten voor: {first_name} {last_name} \n verstuurd naar {email}"
        payment_link_dict = self.client.payment_links.create({"description" : description, "amount" : self.default_amount, "expiresAt": "2022-06-07T11:00:00+00:00"})
        payment_link = payment_link_dict_to_obj(payment_link_dict)
        return payment_link


def payment_link_dict_to_obj(payment_link_dict: dict) -> PaymentLink:
    """
    """
    id = payment_link_dict["id"]
    payment_link_url = payment_link_dict["_links"]["paymentLink"]["href"]
    paid_at = payment_link_dict["paidAt"]
    description = payment_link_dict["description"]
    payment_link = PaymentLink(id, payment_link_url, paid_at, description)
    return payment_link