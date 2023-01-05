from django.core.management.base import BaseCommand, CommandError
from markup_tool.telegram_bot import bot


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            bot.infinity_polling()
        except Exception as e:
            raise CommandError(f'The following error occurred while executing the command run_telegram_bot: {e}')
