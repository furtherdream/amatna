import os
from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    help = "This command creates superuser"

    def handle(self, *args, **options):
        admin = User.objects.get_or_none(username="hanhansss@naver.com")
        if not admin:
            User.objects.create_superuser("hanhansss@naver.com",
                                          "hanhansss@naver.com",
                                          os.environ.get("ADMIN_PASSWORD"))
            self.stdout.write(self.style.SUCCESS("Superuser Created"))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser Exists"))