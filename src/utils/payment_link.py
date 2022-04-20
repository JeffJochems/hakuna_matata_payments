class PaymentLink:
    """
    A payment link
    """

    def __init__(self, id: str, payment_link_url: str , paid_at: str, description: str) -> None:
        """
        Initializes the payment link object.
        :param id: the payment link ID
        :param payment_link_url: a url that can be used to pay a ticket using mollie
        :param paid_at: the date of payment (None if payment is not yet complete)
        :param description: The payment request description reffering to buyer
        """
        self.id = id
        self.payment_link_url = payment_link_url
        self.paid_at = paid_at
        self.description = description

    def is_paid(self):
        """
        Checks the payment status of a payment link.
        :returns: wheter or not a ticket has been paid
        """
        if self.paid_at is None:
            return False
        else:
            return True