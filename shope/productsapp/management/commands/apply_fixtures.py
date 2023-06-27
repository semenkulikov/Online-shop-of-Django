from django.core.management import BaseCommand
from django.db.utils import IntegrityError
import os


class Command(BaseCommand):
    """
    Applies all fixtures to the database
    """
    def handle(self, *args, **options):
        self.stdout.write("=" * 40 +
                          "\nApply all fixtures to the database\n\n")
        paths = [
            "authapp/fixtures/users-fixtures.json",
            "profileapp/fixtures/profiles-fixtures.json",
            "productsapp/fixtures/productsapp-fixture.json",
            "productsapp/fixtures/tag_fixtures.json",
            "orderapp/fixtures/orders_fixtures.json",
            "productsapp/fixtures/banners_fixtures.json",
            "productsapp/fixtures/images-fixtures.json",
            "productsapp/fixtures/sliders_fixtures.json",
            "productsapp/fixtures/products-fixture.json",
            "productsapp/fixtures/categories-fixtures.json",
            "productsapp/fixtures/discounts_fixtures.json",
            "coreapp/fixtures/configs.json"
        ]
        for path in paths:
            try:
                os.system(f"python manage.py loaddata {path}")
            except IntegrityError as error:
                self.stdout.write(self.style.ERROR(
                    f"ERROR! {path} - {error}\n\n"
                ))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f"Fixture {path} applied successfully\n\n"
                ))

        self.stdout.write(self.style.SUCCESS(
            "Fixtures applied successfully\n" + "=" * 40))
