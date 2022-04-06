class Attendee:
    """
    An attendee which either has or has not payed his or her ticket
    """

    def __init__(self, id: str, email: str , first_name: str, last_name: str, customer_journey: str, unique_email_id: str, contact_id: str, payment_link: str, payment_link_id: str) -> None:
        """
        Initializes the attendee object
        """
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.customer_journey = customer_journey
        self.unique_email_id = unique_email_id
        self.customer_journey = customer_journey
        self.payment_link = payment_link
        self.payment_link_id = payment_link_id
    
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
