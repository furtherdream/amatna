from django.core.management.base import BaseCommand
from restaurants import models as restaurants_models


class Command(BaseCommand):
    help = "this command create categories"

    def handle(self, *args, **options):
        categories = [
            "한식",
            "중식",
            "일식",
            "카페",
            "술집",
            "고기집",
            "횟집",
            "해산물",
            "분식",
            "백반집",
            "패스트푸드",
            "파스타",
            "뷔페",
            "국물요리",
            "면요리",
            "아시안",
            "세계음식",
            "이색요리",
            "도전먹방",
        ]

        for c in categories:
            restaurants_models.Category.objects.create(name=c)

        self.style.SUCCESS(f"{len(categories)} categories are created")
