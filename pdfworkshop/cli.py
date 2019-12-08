#!/usr/bin/env python3

import click

from .pdfworkshop import PDFWorkshop

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def pdf_workshop(ctx):
    ctx.obj["app"] = PDFWorkshop()


@pdf_workshop.command()
@click.argument("option", type=click.Choice(['public_key', 'input_dir', 'output_dir', 'suffix', 'recursive']))
@click.argument("value")
@click.pass_context
def config(ctx, option, value):
    ctx.obj["app"].setup(option, value)


@pdf_workshop.command()
@click.pass_context
def list_config(ctx):
    ctx.obj["app"].list_config()


@pdf_workshop.command()
@click.pass_context
def run(ctx):
    ctx.obj["app"].run()


def start():
    pdf_workshop(obj={})
