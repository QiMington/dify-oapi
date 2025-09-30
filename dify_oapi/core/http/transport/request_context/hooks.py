import logging

from .context import RequestContext

logger = logging.getLogger("retry")


def log_backoff(request_context: RequestContext, /, *, level: int = logging.INFO):
    def inner(details: dict):
        err_msg = "UNK"
        if isinstance((e := details.get("exception")), Exception):
            err_msg = f"{e.__class__.__name__}: {e!r}"
        logger.log(
            level,
            f"[Retrying] retry {details['tries']}, waiting {details['wait']:.1f}s"
            f", {request_context.log_str}"
            f", exp: {err_msg}",
        )

    return inner


def log_giveup(request_context: RequestContext, /, *, level: int = logging.ERROR):
    def inner(details: dict):
        err_msg = "UNK"
        if isinstance((e := details.get("exception")), Exception):
            err_msg = f"{e.__class__.__name__}: {e!r}"
        logger.log(
            level, f"[Give up] after {details['tries']} attempts" f", {request_context.log_str}" f", exp: {err_msg}"
        )

    return inner


def log_success(
    request_context: RequestContext, /, *, first_try_level: int = logging.DEBUG, retry_level: int = logging.INFO
):
    def inner(details: dict):
        tries = details["tries"]
        level = first_try_level
        if tries > 1:
            level = retry_level
        logger.log(level, f"[Success] after {details['tries']} attempts" f", {request_context.log_str}")

    return inner
