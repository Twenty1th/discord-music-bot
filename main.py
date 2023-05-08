import argparse

import uvicorn

from src.backend.app import app as api_service
from src.backend.core.settings import get_settings

settings = get_settings()

services = {
    "api": {
        "run": lambda: uvicorn.run(api_service, port=settings.api_port, workers=settings.workers, reload=True),
        "description": "Main module for starting all API services"
    },
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run modules')
    parser.add_argument('-m',
                        type=str,
                        required=True,
                        help=f'Service name to start'
                        )
    subparsers = parser.add_subparsers(help='Modules')
    for key in services.keys():
        subparsers.add_parser(key,
                              help=services[key]['description'])

    args = parser.parse_args()
    services[args.m]['run']()
