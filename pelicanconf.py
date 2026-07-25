AUTHOR = 'Piotr Kierzek'
SITENAME = '>_ siupnij.se'
SITEURL = "http://127.0.0.1:8000"
# SITEURL = "https://siupnij.se"

PATH = "content"

TIMEZONE = 'Europe/Warsaw'

DEFAULT_LANG = 'pl'

DEFAULT_DATE_FORMAT = "%Y-%m-%d"

COPYRIGHT = """Wszelkie treści opublikowane na tej stronie są udostępniane na <a href="https://fedoraproject.org/wiki/Licensing:MIT?rd=Licensing/MIT#NTP_variant">licencji MIT</a>, chyba, że sprecyzowane jest inaczej."""
DISCLAIMER = """Motyw <a href="https://kura.gg/eevee/" title="Eevee">Eevee</a> autorstwa <a href="https://kura.gg/" title="kura.gg">kura.gg</a>. Hosting zapewnia <a href="https://neocities.org">Neocities</a>."""

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = [
]

# Social widget
SOCIAL = [
]

DEFAULT_PAGINATION = False

# ustawienia motywu
THEME = "eevee"
THEME_PRIMARY = "purple"
THEME_ACCENT = "pink"

USE_AUTHOR_CARD = True
AUTHOR_CARD_AVATAR = "/images/ja_transparent.png"
AUTHOR_CARD_DESCRIPTION = "Profesjonalny idiota (w sensie dostojewiczowskim)."
TWITTER_USERNAME = "whoate"

SOCIAL = [
  ("Twitter (X)", "https://x.com/WhoAte"),
]

AUTHOR_CARD_SOCIAL = [
    ("""<i class="fa fa-github" aria-hidden="true"></i>""", "https://github.com/kierzekp"),
    ("""<i class="fa fa-twitter" aria-hidden="true"></i>""", "https://x.com/WhoAte"),
    ("""<i class="fa fa-youtube" aria-hidden="true"></i>""", "https://www.youtube.com/@PiotrKierzek"),
    ("""<i class="fa fa-lastfm" aria-hidden="true"></i>""", "https://libre.fm/user/whoatemymusic"),
    ("""<i class="fa fa-at" aria-hidden="true"></i>""", "mailto:kierzek@siupnij.se"),
]

MEGA_FOOTER = False

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

ARTICLE_URL = "{date:%Y}/{date:%m}/{date:%d}/{slug}/"
ARTICLE_SAVE_AS = "{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html"
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
TAG_URL = "tag/{slug}/"
TAG_SAVE_AS = "tag/{slug}/index.html"
TAGS_URL = "tags/"
TAGS_SAVE_AS = "tags/index.html"
CATEGORY_URL = "category/{slug}/"
CATEGORY_SAVE_AS = "category/{slug}/index.html"
CATEGORIES_URL = "categories/"
CATEGORIES_SAVE_AS = "categories/index.html"
AUTHOR_URL = "authors/{slug}/"
AUTHOR_SAVE_AS = "authors/{slug}/index.html"