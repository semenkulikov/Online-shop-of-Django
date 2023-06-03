from django.core.management import BaseCommand
from django.db.utils import IntegrityError
import os


class Command(BaseCommand):
    """
    Applies all fixtures to the database
    """
    def handle(self, *args, **options):
        self.stdout.write("Apply all fixtures to the database")
        paths = [
            "authapp/fixtures/users-fixtures.json",
            "profileapp/fixtures/profiles-fixtures.json",
            "productsapp/fixtures/productsapp-fixture.json",
            "productsapp/fixtures/tag_fixtures.json",
            "orderapp/fixtures/orders_fixtures.json",
            "productsapp/fixtures/banners_fixtures.json",
            "productsapp/fixtures/images-fixtures.json",
            "productsapp/fixtures/sliders_fixtures.json",
        ]
        for path in paths:
            try:
                os.system(f"python manage.py loaddata {path}")
            except IntegrityError as error:
                self.stdout.write(self.style.ERROR(
                    f"ERROR! {path} - {error}"
                ))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f"Fixture {path} applied successfully"
                ))

        self.stdout.write(self.style.SUCCESS("Fixtures applied successfully"))


if __name__ == "__main__":
    test = Command()
    test.handle(None)
