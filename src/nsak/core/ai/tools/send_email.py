from langchain.tools import tool

from nsak.core.email.email_backend import email_backend


@tool  # type: ignore[misc]
def send_email(
    subject: str,
    message: str,
    cc_recipients: list[str] | None = None,
    attachments: list[str] | None = None,
) -> None:
    """
    Send an email notification to the configured receiver.

    Use this tool to alert the human operator about findings, incidents, or
    completed tasks that require their attention outside the current session.

    Args:
        subject: A short, descriptive subject line for the email, which is added to the subject prefix `NSAK - AI Agent:`.
        message: The full body of the email.
        cc_recipients: Optional comma seperated list of emails, which should receive a carbon copy of the email.
        attachments: Optional list of absolute file paths to attach to the email (e.g. scan reports, captured files).
    """
    subject = f"NSAK - AI Agent: {subject}"
    email_backend.send(subject, message, cc_recipients, attachments)
