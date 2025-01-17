#! /usr/bin/env python
import click
import os
import datetime

from ittools.config import load_issue_tracker_config, ReportOptions
from ittools.cfd.cumulative_flow_graph import CumulativeFlowGraph


DEFAULT_CONFIG_FILE = "~/issuetracker.yml"


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("-v", "--verbose", is_flag=True)
@click.option("-c", "--config", type=click.Path(exists=True))
@click.option(
    "-o",
    "--open-graph",
    is_flag=True,
    default=False,
    help="Open the graph after generation",
)
@click.option(
    "-t",
    "--today",
    default=None,
    type=click.DateTime(formats=["%Y-%m-%d"]),
    help="Override today's date",
)
@click.argument("project")
def cfd(
    verbose: bool,
    config: click.Path,
    open_graph: bool,
    today: click.DateTime,
    project: str,
) -> None:
    """Create a cumulative flow diagram for a given project

    Requires a project progress file (progress.csv) in the project directory. This is normally generated
    by the `it project` command
    """
    options = build_report_options(verbose, config)
    report_date = date_option_or_today(today)
    csv_file = f"{options.report_dir}/{project}/progress.csv"
    png_file = f"{options.report_dir}/{project}/cfd-{str(report_date)}.png"
    project_config = options.project_configs[project]
    CumulativeFlowGraph(project_config, csv_file, png_file, report_date).run(open_graph)


def build_report_options(verbose: bool, config_file: click.Path) -> ReportOptions:
    config_file = config_file or os.path.expanduser(DEFAULT_CONFIG_FILE)
    if verbose:
        print(f"Using config file '{config_file}'")
    config = load_issue_tracker_config(config_file)
    return ReportOptions(config, verbose)


def date_option_or_today(option: click.DateTime) -> datetime.date:
    if option:
        return option.date()
    return datetime.date.today()


if __name__ == "__main__":
    cfd()
