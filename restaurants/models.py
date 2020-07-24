import os
import requests
import urllib.request
from django.db import models
from django.utils.translation import gettext_lazy as _
from core import models as core_models
from bs4 import BeautifulSoup


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

    title = models.CharField(_("title"), max_length=40, blank=True)
    youtube = models.ManyToManyField("Youtube",
                                     related_name="restaurant",
                                     blank=True,
                                     verbose_name=_("youtube"))
    instagram_url = models.CharField(_("instagram url"),
                                     max_length=40,
                                     blank=True)
    channel = models.ManyToManyField(
        "Channel",
        related_name="restaurant",
        blank=True,
        verbose_name=_("channel"),
    )
    address = models.CharField(_("address"), max_length=30, blank=True)
    phone_number = models.CharField(_("phone number"),
                                    max_length=13,
                                    blank=True)
    category = models.ManyToManyField("Category",
                                      related_name="restaurant",
                                      blank=True,
                                      verbose_name=_("category"))
    price = models.CharField(_("price"), blank=True, max_length=20)
    biztime_start = models.TimeField(_("biztime start"), blank=True, null=True)
    biztime_end = models.TimeField(_("biztime end"), blank=True, null=True)
    biztime_24 = models.BooleanField(_("biztime 24"), default=False)
    biztime_desc = models.CharField(_("biztime_desc"),
                                    max_length=30,
                                    blank=True)
    breaktime = models.TextField(_("breaktime"), blank=True)
    holiday = models.CharField(_("holiday"),
                               choices=HOLIDAY_CHOICES,
                               max_length=10,
                               blank=True)
    info = models.TextField(_("info"), blank=True)
    menu = models.TextField(_("menu"), blank=True)
    tag_set = models.ManyToManyField("Tag",
                                     related_name="restaurant",
                                     blank=True,
                                     verbose_name=_("tag set"))
    naver_place_id = models.CharField(_("naver_place_id"),
                                      max_length=15,
                                      unique=True)
    blog_count = models.CharField(_("blog_count"), max_length=15, blank=True)
    tv_list = models.TextField(_("tv_list"), blank=True)
    comment = models.TextField(_("comment"), blank=True)
    x = models.FloatField(_("x"), blank=True, null=True)
    y = models.FloatField(_("y"), blank=True, null=True)

    def __str__(self):
        return self.title

    def scrap_restaurant_info(self):
        headers = {
            "User-Agent":
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
        }
        url = f"https://store.naver.com/restaurants/detail?id={self.naver_place_id}"
        result = requests.get(url, headers=headers)
        soup = BeautifulSoup(result.text, 'html.parser')

        biz_name = soup.find("div", {"class", "biz_name_area"})
        name = biz_name.find("strong").text
        blog_count = biz_name.find("a").text

        biz_info = soup.find("div", {"class": "list_bizinfo"})
        biztel = biz_info.find("div", {
            "class": "list_item_biztel"
        }).find("div").string
        address = biz_info.find("div", {
            "class": "list_item_address"
        }).find("div").find("li").find("span").string

        menu_list = ""
        menu = soup.find("div", {
            "class": "list_bizinfo"
        }).find_all("div", {"class": "list_menu_inner"})
        for i in menu[0:-1]:
            menu_name = i.find("span").string
            price = i.find("em").string
            menu_list += str(f"{menu_name} - {price}\n")

        tv_list = ""
        try:
            tv = soup.find("div", {
                "class": "list_item_tv"
            }).find_all("div", {"class": "tv"})
            for t in tv:
                tv_name = t.find("span", {"class": "item"}).text
                tv_list += (f"{tv_name}\n")
        except:
            tv = ""

        return {
            "name": name,
            "blog_count": blog_count,
            "biztel": biztel,
            "address": address,
            "menu_list": menu_list,
            "tv_list": tv_list,
        }

    def get_latlng(self):
        client_id = os.environ.get("NAVER_CLIENT_ID")
        client_secret = os.environ.get("NAVER_CLIENT_SECRET")
        encText = urllib.parse.quote(self.address)
        url = f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={encText}"  # json결과
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
        request.add_header("X-NCP-APIGW-API-KEY", client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            mystr = response_body.decode('utf-8')
            mystr = mystr.replace('true', "True")
            mystr = mystr.replace('false', "False")
            # string -> json 타입으로 바꾸자
            mydic = eval(mystr)
            x = mydic['addresses'][0]['x']
            y = mydic['addresses'][0]['y']
            return x, y
        else:
            print("Error Code:" + rescode)

    def save(self, *args, **kwargs):
        restaurant_info = self.scrap_restaurant_info()
        self.title = restaurant_info.get("name")
        self.address = restaurant_info.get("address")
        self.blog_count = restaurant_info.get("blog_count")
        self.phone_number = restaurant_info.get("biztel")
        self.menu = restaurant_info.get("menu_list")
        self.tv_list = restaurant_info.get("tv_list")
        self.x = self.get_latlng()[0]
        self.y = self.get_latlng()[1]
        super().save(*args, **kwargs)
