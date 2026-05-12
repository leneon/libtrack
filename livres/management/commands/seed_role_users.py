from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from etablissement.models import Etablissement
from livres.models import Profile

DEFAULT_PASSWORD = "Password123!"
DEMO_ETAB_CODE = "LIBTRACK"

ACCOUNTS = (
    {
        "email": "super_admin@libtrack.edu",
        "role": "super_admin",
        "is_superuser": True,
        "is_staff": True,
        "needs_etablissement": False,
    },
    {
        "email": "admin@libtrack.edu",
        "role": "admin",
        "is_superuser": False,
        "is_staff": True,
        "needs_etablissement": True,
    },
    {
        "email": "bibliothecaire@libtrack.edu",
        "role": "bibliothecaire",
        "is_superuser": False,
        "is_staff": True,
        "needs_etablissement": True,
    },
)


class Command(BaseCommand):
    help = (
        "Crée ou met à jour un utilisateur par rôle (e-mail = identifiant de connexion), "
        f"mot de passe par défaut : {DEFAULT_PASSWORD!r}."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            default=DEFAULT_PASSWORD,
            help="Mot de passe à appliquer (défaut : celui des comptes démo).",
        )

    def handle(self, *args, **options):
        password = options["password"]
        User = get_user_model()

        etab, _ = Etablissement.objects.get_or_create(
            code=DEMO_ETAB_CODE,
            defaults={
                "nom": "LibTrack — établissement démo",
                "adresse": "Local",
                "email": "contact@libtrack.edu",
            },
        )

        for spec in ACCOUNTS:
            email = spec["email"]
            etablissement = etab if spec["needs_etablissement"] else None

            user = User.objects.filter(username=email).first()
            if user is None:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    is_staff=spec["is_staff"],
                    is_superuser=spec["is_superuser"],
                )
                created = True
            else:
                user.email = email
                user.is_staff = spec["is_staff"]
                user.is_superuser = spec["is_superuser"]
                user.set_password(password)
                user.save()
                created = False

            Profile.objects.update_or_create(
                user=user,
                defaults={"role": spec["role"], "etablissement": etablissement},
            )

            action = "Créé" if created else "Mis à jour"
            self.stdout.write(
                self.style.SUCCESS(
                    f"{action}: {email} (rôle {spec['role']!r}) — connexion avec cet e-mail comme identifiant."
                )
            )

        self.stdout.write(
            self.style.NOTICE(
                f"Établissement démo pour admin / bibliothécaire : [{etab.code}] {etab.nom}"
            )
        )
