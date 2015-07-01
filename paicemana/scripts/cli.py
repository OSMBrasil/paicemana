import time
import datetime

import click

from paicemana.textdownload import MarkdownDownload
from paicemana.mdanalyzer import MarkdownAnalyzer
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
        download = MarkdownDownload(archive)
        analyzer = MarkdownAnalyzer(download.filename)
        organizer = analyzer.getOrganizer()
        translators = ['alexandre-mbm', 'jgpacker', 'vgeorge']
        organizer.distribute_for(translators)
        print('\n%s\n\n%s\n' % (organizer, organizer.scores()))
    except HTTPError as e:
        click.echo(e)

