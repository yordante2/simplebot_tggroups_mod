"""extra command line subcommands for simplebot's CLI"""

import os

from simplebot import DeltaBot
from telethon import TelegramClient

from .util import get_session_path, getdefault, set_config, sync


# pylama:ignore=C0103
class telegram:
    """Configure Telegram settings."""

    def add_arguments(self, parser) -> None:
        parser.add_argument("--api-id", help="set the API ID")
        parser.add_argument("--api-hash", help="set the API hash")
        parser.add_argument("--phone", help="set the phone number")
        parser.add_argument(
            "--max-size", help="set the maximum attachment size allowed to be bridged"
        )

    def run(self, bot: DeltaBot, args, out) -> None:
        if args.max_size:
            set_config(bot, "max_size", args.max_size)
            out.line("Maximum attachment size updated.")
            return

        if args.api_id:
            set_config(bot, "api_id", args.api_id)
            out.line("API ID updated.")
        elif not getdefault(bot, "api_id"):
            set_config(bot, "api_id", input("Enter API ID: "))
            out.line("API ID updated.")

        if args.api_hash:
            set_config(bot, "api_hash", args.api_hash)
            out.line("API hash updated.")
        elif not getdefault(bot, "api_hash"):
            set_config(bot, "api_hash", input("Enter API hash: "))
            out.line("API hash updated.")

        if args.phone:
            set_config(bot, "phone", args.phone)
            path = get_session_path(bot)
            if os.path.exists(path):
                # remove session database to avoid conflicts with new token
                os.remove(path)
            out.line("phone number updated.")
        elif not getdefault(bot, "phone"):
            set_config(bot, "phone", input("Enter phone number: "))
            out.line("phone number updated.")

        _configure(bot)


@sync
async def _configure(dcbot) -> None:
    client = await TelegramClient(
        get_session_path(dcbot),
        api_id=getdefault(dcbot, "api_id"),
        api_hash=getdefault(dcbot, "api_hash"),
    ).start() #phone_number=getdefault(dcbot, "phone"))
    set_config(dcbot, "telegram_bot", (await client.get_me()).username)
