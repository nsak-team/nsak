import logging
import smtplib
from email.message import EmailMessage

from lazy_object_proxy import Proxy

from nsak.core import EmailEncryptionType, config
from nsak.core._config import EmailConfig

logger = logging.getLogger(__name__)


class LoggerEmailBackend:
    """
    Dummy email backend, which just writes to the logger.
    """

    def send_message(self, msg: EmailMessage) -> None:
        """
        Log the email message.

        :return:
        """
        logger.info(str(msg))


class EmailBackend:
    """
    Email Backend used for sending mails via SMTP.
    """

    backend: smtplib.SMTP | LoggerEmailBackend

    def __init__(self, email_config: EmailConfig | None) -> None:
        """
        Set up the SMTP client with the correct configuration for encryption.
        """
        self.config = email_config
        self._init_backend()

    def _init_backend(self) -> None:
        """
        Init the email backend for sending mails.

        :return:
        """
        if self.config is None:
            self.backend = LoggerEmailBackend()
        else:
            match self.config.encryption:
                case EmailEncryptionType.NONE:
                    self.backend = smtplib.SMTP(self.config.host, self.config.port)
                case EmailEncryptionType.TLS:
                    self.backend = smtplib.SMTP(self.config.host, self.config.port)
                    self.backend.starttls()
                case EmailEncryptionType.SSL:
                    self.backend = smtplib.SMTP_SSL(self.config.host, self.config.port)

            self.backend.login(self.config.user, self.config.password)

    def _get_template(self) -> EmailMessage:
        """
        Get the email template.

        :return:
        """
        template = EmailMessage()
        if self.config is not None:
            template["From"] = self.config.sender
            template["To"] = self.config.receiver
        else:
            # For the LoggerEmailBacked
            template["From"] = "dummy@example.com"
            template["To"] = "dummy@example.com"

        return template

    def send(self, subject: str, message: str) -> None:
        """
        Send email message.

        :return:
        """
        email = self._get_template()
        email.set_content(message)
        email["Subject"] = subject
        self.backend.send_message(email)


email_backend: EmailBackend = Proxy(lambda: EmailBackend(config.email))
