class Attendee:
    """
    An attendee which either has or has not payed his or her ticket
    """

    def __init__(self, id: str, list_id: str, email: str , first_name: str, last_name: str, unique_email_id: str, payment_link: str, payment_link_id: str, customer_journey: str, amount_tickets: int) -> None:
        """
        Initializes the attendee object
        """
        self.id = id
        self.list_id = list_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.unique_email_id = unique_email_id
        self.payment_link = payment_link
        self.payment_link_id = payment_link_id
        self.customer_journey = customer_journey
        self.amount_tickets = amount_tickets
        self.value_tickets = (8.5 * self.amount_tickets) + 0.30
    
    def has_payed(self) -> bool:
        """
        Checked whether or not the attendee has payed his or her ticket
        """
        if self.customer_journey == "payed":
            return True
        else:
            return False

    def has_payment_link(self) -> bool:
        """
        Checked whether or not the attendee has payed his or her ticket
        """
        if self.customer_journey == "payed" or self.customer_journey == "payment_pending":
            return True
        else:
            return False
