class PaymentLink:
    """
    """

    def __init__(self, id: str, payment_link_url: str , paid_at: str, description: str) -> None:
        """
        Initializes the payment link object
        """
        self.id = id
        self.payment_link_url = payment_link_url
        self.paid_at = paid_at
        self.description = description

    def is_paid(self):
        """
        """
        if self.paid_at is None:
            return False
        else:
            return True