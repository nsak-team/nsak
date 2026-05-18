from langchain.tools import tool

from nsak.core.configuration import config
from nsak.core.email.email_backend import email_backend

# Hardcoded for now!
grafana_link_template = "https://grafana.hiube.ch/a/grafana-lokiexplore-app/explore/nsak_run_uuid/{run_uuid}/logs?var-ds=P8E80F9AEF21F6940&var-filters=nsak_run_uuid|%3D|{run_uuid}&patterns=[]&var-lineFormat=&var-fields=&var-levels=&var-metadata=&var-jsonFields=&var-patterns=&var-lineFilterV2=&var-lineFilters=caseSensitive,0|__gfp__~|\\[(AI)__gfp__(Prompt)__gfp__(Tool)\\]&timezone=browser&var-all-fields=&userDisplayedFields=false&displayedFields=[]&urlColumns=[]&visualizationType=%22logs%22&prettifyLogMessage=true&sortOrder=%22Ascending%22&wrapLogMessage=true"
template = """
Scenario: %(scenario)s\n
Run ID: %(run_uuid)s\n
Datetime: %(datetime)s\n
\n
See logs in Grafana: %(grafana_link)s\n
\n
---------------------------------------------\n
\n
%(message)s\n
\n
"""


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
    grafana_link = grafana_link_template.format(run_uuid=config.run_uuid)
    content = template % {
        "scenario": config.running_scenario,
        "run_uuid": config.container.id,
        "datetime": config.datetime,
        "grafana_link": grafana_link,
        "message": message,
    }
    email_backend.send(subject, content, cc_recipients, attachments)
