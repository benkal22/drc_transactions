from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from transactions.models import CustomUser
import random
import string

class Command(BaseCommand):
    help = 'Create 100 users with Congolese names'

    def handle(self, *args, **kwargs):
        noms = [
            "Alain", "Benoit", "Chantal", "Désiré", "Emilie", "François", "Georgette", "Hervé", "Isabelle", "Jacques",
            "Koffi", "Liliane", "Marc", "Nathalie", "Olivier", "Patricia", "Quentin", "René", "Simone", "Thierry",
            "Ursule", "Vincent", "William", "Xavier", "Yvette", "Zacharie", "Aimé", "Bernadette", "Claude", "Diana",
            "Etienne", "Fabienne", "Gaston", "Henriette", "Ivan", "Jean", "Karine", "Lucien", "Monique", "Noël",
            "Odile", "Pierre", "Quirina", "Roger", "Suzanne", "Thomas", "Urbain", "Véronique", "Willy", "Xénia",
            "Yvan", "Zoé", "Adolphe", "Brigitte", "Christophe", "Delphine", "Emmanuel", "Francine", "Gérard", "Hélène",
            "Irène", "Joseph", "Katia", "Laurent", "Michel", "Nadine", "Océane", "Pascal", "Quentin", "Roland",
            "Sylvie", "Tristan", "Ursule", "Valérie", "Wilfried", "Xavier", "Yvonne", "Zacharie", "Anne", "Bernard",
            "Claire", "Didier", "Estelle", "Félix", "Geneviève", "Hugues", "Inès", "Julien", "Kim", "Léon"
        ]

        for i, nom in enumerate(noms, start=1):
            username = f"{nom.lower()}{i}"
            email = f"user{i}@exemple.com"
            password = "Azert@123"

            # Add randomness to make usernames more unique
            username += ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))

            try:
                CustomUser.objects.create_user(username=username, email=email, password=password, first_name=nom, last_name="Congolais")
                self.stdout.write(self.style.SUCCESS(f'Successfully created user {username}'))
            except IntegrityError:
                self.stdout.write(self.style.WARNING(f'User {username} already exists. Skipping...'))

        self.stdout.write(self.style.SUCCESS('Finished creating users'))
