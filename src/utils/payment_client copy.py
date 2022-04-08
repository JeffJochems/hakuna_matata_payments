import requests

class PaymentClient:
    """
    """

    def __init__(self, server_url, client_id, api_secret) -> None:
        """ 
        """
        self.url = server_url
        self.client_id = client_id
        self.api_secret = api_secret
        self.generate_next_invoice_nr()

    def generate_next_invoice_nr(self):
        """
        """
        url = self.url + "/invoicing/generate-next-invoice-number"
        headers = {"Content-Type": "application/json", "Accept-Language": "en_US"}
        auth = (self.client_id, self.api_secret)
        response = requests.post(url=url, headers=headers, auth=auth)
        print(response.content)