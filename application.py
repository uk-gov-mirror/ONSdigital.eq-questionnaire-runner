#!/usr/bin/env python

import logging
import os
import sys
import googlecloudprofiler

from structlog import configure
from structlog.dev import ConsoleRenderer
from structlog.processors import JSONRenderer, format_exc_info
from structlog.processors import TimeStamper
from structlog.stdlib import LoggerFactory, add_log_level
from structlog.threadlocal import wrap_dict


def configure_logging():
    log_level = logging.INFO
    debug = os.getenv("FLASK_ENV") == "development"
    if debug:
        log_level = logging.DEBUG

    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setLevel(log_level)
    log_handler.addFilter(lambda record: record.levelno <= logging.WARNING)

    error_log_handler = logging.StreamHandler(sys.stderr)
    error_log_handler.setLevel(logging.ERROR)

    logging.basicConfig(
        level=log_level, format="%(message)s", handlers=[error_log_handler, log_handler]
    )

    # Set werkzeug logging level
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.setLevel(level=log_level)

    def parse_exception(_, __, event_dict):
        if debug:
            return event_dict
        exception = event_dict.get("exception")
        if exception:
            event_dict["exception"] = exception.replace('"', "'").split("\n")
        return event_dict

    # setup file logging
    renderer_processor = ConsoleRenderer() if debug else JSONRenderer()
    processors = [
        add_log_level,
        TimeStamper(key="created", fmt="iso"),
        add_service,
        format_exc_info,
        parse_exception,
        renderer_processor,
    ]

    configure(
        context_class=wrap_dict(dict),
        logger_factory=LoggerFactory(),
        processors=processors,
        cache_logger_on_first_use=True,
    )


def add_service(logger, method_name, event_dict):  # pylint: disable=unused-argument
    """
    Add the service name to the event dict.
    """
    event_dict["service"] = "eq-questionnaire-runner"
    return event_dict


def start_cloud_profiler():
    # Profiler initialization. It starts a daemon thread which continuously
    # collects and uploads profiles. Best done as early as possible.
    try:
        googlecloudprofiler.start(
            service='runner',
            service_version='1.0.1',
            # verbose is the logging level. 0-error, 1-warning, 2-info,
            # 3-debug. It defaults to 0 (error) if not set.
            verbose=3,
            # project_id must be set if not running on GCP.
            # project_id='census-eq-mark5',
        )
    except (ValueError, NotImplementedError) as exc:
        print(exc)  # Handle errors here


# Initialise logging before the rest of the application
start_cloud_profiler()
configure_logging()
from app.setup import create_app  # pylint: disable=wrong-import-position # NOQA

application = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    application.run(port=port, threaded=True)
