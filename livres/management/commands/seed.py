from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Alias de seed_role_users (déploiement Render, CI, etc.)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            default=None,
            help="Transmis à seed_role_users (sinon mot de passe démo du projet).",
        )

    def handle(self, *args, **options):
        kwargs = {}
        if options.get("password"):
            kwargs["password"] = options["password"]
        call_command("seed_role_users", *args, **kwargs)
