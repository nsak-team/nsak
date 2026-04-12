import dataclasses
from enum import Enum


class EmailEncryptionType(Enum):
    """
    Possible encryption options for the email backend.
    """

    NONE = 0
    TLS = 1
    SSL = 2


@dataclasses.dataclass(kw_only=True)
class EmailConfiguration:
    """
    SMTP Configuration for sending emails.
    """

    host: str
    port: int
    encryption: EmailEncryptionType = EmailEncryptionType.NONE
    username: str
    password: str
    sender: str
    receiver: str
