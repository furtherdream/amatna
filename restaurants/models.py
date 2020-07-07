from django.db import models
from django.utils.translation import gettext_lazy as _
from core import models as core_models


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(_("name"), max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Channel(core_models.TimeStampedModel):

    """ Channel Model Definition """

    class Meta:
        verbose_name = _("channel")
        verbose_name_plural = _("channels")

    name = models.CharField(_("name"), max_length=20, unique=True)
    description = models.TextField(_("description"),)
    thumbnail = models.ImageField(
        _("thumbnail"), upload_to="channel_thumbnails", blank=True
    )
    image = models.ImageField(_("image"), upload_to="channel_images")
    youtube_link = models.CharField(_("youtube link"), max_length=40, blank=True)
    instagram_link = models.CharField(_("instagram link"), max_length=40, blank=True)
    rank = models.PositiveSmallIntegerField(_("rank"), blank=True, default="0")

    def __str__(self):
        return self.name


class Category(AbstractItem):

    """ Category Model Definitioin """

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    class Meta:
        verbose_name = _("photo")
        verbose_name_plural = _("photos")

    caption = models.CharField(_("caption"), max_length=80, blank=True)
    file = models.ImageField(_("file"), upload_to="restaurant_photos")
    restaurant = models.ForeignKey(
        "Restaurant",
        related_name="photos",
        on_delete=models.CASCADE,
        verbose_name=_("restaurant"),
    )

    def __str__(self):
        return self.caption


class Youtube(core_models.TimeStampedModel):

    """ Youtube Model Definition """

    class Meta:
        verbose_name = _("youtube ID")
        verbose_name_plural = _("youtube IDs")

    name = models.CharField(_("name"), max_length=80, default="")
    video_id = models.CharField(_("video ID"), max_length=20, blank=True)

    def __str__(self):
        return self.name


class Tag(core_models.TimeStampedModel):

    """ Tag Model Definition """

    class Meta:
        verbose_name = _("tag")
        verbose_name_plural = _("tags")

    name = models.CharField(_("name"), max_length=20, unique=True)

    def __str__(self):
        return self.name


class Restaurant(core_models.TimeStampedModel):

    """ Restaurant Model Definition """

    HOLIDAY_MON = "월요일"
    HOLIDAY_TUE = "화요일"
    HOLIDAY_WED = "수요일"
    HOLIDAY_THU = "목요일"
    HOLIDAY_FRI = "금요일"
    HOLIDAY_SAT = "토요일"
    HOLIDAY_SUN = "일요일"

    HOLIDAY_CHOICES = (
        (HOLIDAY_MON, _("Monday")),
        (HOLIDAY_TUE, _("Tuesday")),
        (HOLIDAY_WED, _("Wednesday")),
        (HOLIDAY_THU, _("Thursday")),
        (HOLIDAY_FRI, _("Friday")),
        (HOLIDAY_SAT, _("Saturday")),
        (HOLIDAY_SUN, _("Sunday")),
    )

    class Meta:
        verbose_name = _("restaurant")
        verbose_name_plural = _("restaurants")

    title = models.CharField(_("title"), max_length=40, default="")
    youtube = models.ManyToManyField(
        "Youtube", related_name="restaurant", blank=True, verbose_name=_("youtube")
    )
    instagram_url = models.CharField(_("instagram url"), max_length=40, blank=True)
    channel = models.ManyToManyField(
        "Channel", related_name="restaurant", blank=True, verbose_name=_("channel"),
    )
    address = models.CharField(_("address"), max_length=30, default="")
    phone_number = models.CharField(
        _("phone number"), max_length=13, default="", unique=True
    )
    category = models.ManyToManyField(
        "Category", related_name="restaurant", blank=True, verbose_name=_("category")
    )
    price = models.CharField(_("price"), blank=True, max_length=20)
    biztime_start = models.TimeField(_("biztime start"), blank=True, null=True)
    biztime_end = models.TimeField(_("biztime end"), blank=True, null=True)
    biztime_24 = models.BooleanField(_("biztime 24"), default=False)
    breaktime = models.TextField(_("breaktime"), blank=True)
    holiday = models.CharField(
        _("holiday"), choices=HOLIDAY_CHOICES, max_length=10, default=None, blank=True
    )
    info = models.TextField(_("info"), blank=True)
    menu = models.TextField(_("menu"), blank=True)
    tag_set = models.ManyToManyField(
        "Tag", related_name="restaurant", blank=True, verbose_name=_("tag set")
    )

    def __str__(self):
        return self.title
