import click

from nsak.core.ai.ai_agent import create_ai_agent

ai_agent_group = click.Group("ai_agent")


@ai_agent_group.command("run")
@click.argument("prompt")
def run_ai_agent(prompt: str) -> None:
    """
    Run the AI-agent with the given prompt.
    """
    ai_agent = create_ai_agent(True)
    for line in ai_agent.run(prompt):
        click.echo(line)
