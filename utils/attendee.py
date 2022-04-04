class Attendee:
    """
    An attendee which either has or has not payed his or her ticket
    """

    def __init__(self, id: str, name: str, payment_status: str) -> None:
        """
        Initializes the attendee object
        """
        self.id = id
        self.name = name
        self.payment_status = payment_status
    
    def has_payed(self) -> bool:
        """
        Checked whether or not the attendee has payed his or her ticket
        """
        if self.payment_status == "payed":
            return True
        else:
            return False

