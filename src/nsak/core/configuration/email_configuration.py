import dataclasses
import logging
from enum import Enum
from typing import Any, Self

logger = logging.getLogger(__name__)


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

    @classmethod
    def create(cls, data: dict[str, Any] | None) -> Self | None:
        """
        Tries to create the EmailConfig from data.

        :param data:
        :return:
        """
        if data is None:
            logger.info("Could not create EmailConfiguration object.")
            return None

        try:
            return cls(
                host=data.get("host"),  # type: ignore [arg-type]
                port=data.get("port"),  # type: ignore [arg-type]
                encryption=EmailEncryptionType(data.get("encryption")),
                username=data.get("username"),  # type: ignore [arg-type]
                password=data.get("password"),  # type: ignore [arg-type]
                sender=data.get("sender"),  # type: ignore [arg-type]
                receiver=data.get("receiver"),  # type: ignore [arg-type]
            )
        except ValueError as e:
            logger.info("Could create EmailConfiguration object.", exc_info=e)
            return None
