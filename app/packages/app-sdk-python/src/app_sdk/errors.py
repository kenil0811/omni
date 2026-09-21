"""Stable, safe failures an App can raise."""

from __future__ import annotations


class AppError(Exception):
    """Base class. The message is shown to the user, so keep it plain."""

    retryable = False


class InvalidInput(AppError):
    """The supplied input cannot be processed. Not retryable."""


class UnsupportedInput(AppError):
    """A format or shape this App does not handle. Explain what is supported."""


class ExternalUnavailable(AppError):
    """A required external route failed. Retryable."""

    retryable = True
