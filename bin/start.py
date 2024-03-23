#!/usr/bin/env python

import click
import uvicorn
import pathlib

ROOT = pathlib.Path(__file__).parent.parent


@click.command()
@click.option("--host", default="localhost", help="Host")
@click.option("--port", default=8000, help="Port")
@click.option("--reload", default=True, help="Reload")
def start(host, port, reload):
    uvicorn.run(
        "phone_number:app",
        host=host,
        port=port,
        app_dir=str(ROOT),
        reload=reload,
    )


if __name__ == "__main__":
    start()
