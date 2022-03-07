import json
import os
import urllib
from pathlib import Path

from data_sources.data_source import DataSource


class Bulbapedia(DataSource):
    # API help https://bulbapedia.bulbagarden.net/w/api.php?action=help&modules=query
    source_urls = {
        "https://bulbapedia.bulbagarden.net/w/api.php?action=query&list=categorymembers&cmtitle=Category:English%20promotional%20cards"


    }