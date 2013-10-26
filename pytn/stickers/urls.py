from django.conf.urls.defaults import patterns, url


urlpatterns = patterns("pytn.stickers.views",
    url(r"^submit/$", "sticker_submit", name="sticker_submit"),
    url(r"^review/$", "sticker_review", name="sticker_review"),
    url(r"^detail/(\d+)/$", "sticker_detail", name="sticker_detail"),
    url(r"^vote/(\d+)/$", "sticker_vote", name="sticker_vote"),
)
