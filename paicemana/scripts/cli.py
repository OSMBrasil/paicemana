import time
import datetime

import click

from paicemana.textdownload import MarkdownDownload
from urllib.error import HTTPError


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-g', '--archive', type=int,
    help='Number in permalink like www.weeklyosm.eu/archives/4205')
def cli(archive):
    """A helper script for works at OSMBrasil/semanario"""
    if not archive:
        raise click.UsageError('try the -h/--help option')
    try:
        MarkdownDownload(archive)
    except HTTPError as e:
        click.echo(e)

