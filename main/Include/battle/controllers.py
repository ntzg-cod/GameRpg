"""Player input handling (SRP/DIP).

The engine never calls ``input()``: it asks a ``PlayerController`` for an
action code. ``ConsolePlayerController`` keeps the exact prompts of the
original game, and validates against whatever actions are registered.
"""

from __future__ import annotations

from collections.abc import Mapping

from .actions import Action


class ConsolePlayerController:
    """Read the player's choice from the console, re-prompting on error."""

    def __init__(self, input_fn=input) -> None:
        self._input = input_fn

    def choose_action(self, valid_codes: Mapping[str, Action]) -> str:
        codes = "/".join(valid_codes)
        selection = self._input(f"It's your turn... ({codes}): ").lower()
        while selection not in valid_codes:
            options = ", ".join(f"({code}){action.label}" for code, action in valid_codes.items())
            selection = self._input(f"Invalid. Choose {options}: ").lower()
        return selection


__all__ = ["ConsolePlayerController"]
