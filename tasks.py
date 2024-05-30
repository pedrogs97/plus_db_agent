"""Invoke tasks for the project"""

from invoke import task


@task
def makemigrations(cmd, message):
    """Generate migrations for the database."""
    cmd.run(f"aerich migrate --name '{message}'")


@task
def migrate(cmd):
    """Apply migrations to the database."""
    cmd.run("aerich upgrade")


@task
def initdb(cmd):
    """Create the database tables."""
    cmd.run("aerich init -t database_agent.config.DATABASE_CONFIG")
    cmd.run("aerich init-db")


@task
def runtest(cmd, file=None):
    """Run tests."""
    if file:
        cmd.run(f"pytest tests/{file}.py")
    else:
        cmd.run("pytest tests")
