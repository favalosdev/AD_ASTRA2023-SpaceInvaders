from textos import NEWSProcessor;

news = NEWSProcessor()

news.ner_from_url("https://www.eltiempo.com/tecnosfera/novedades-tecnologia/que-es-clubhouse-la-red-social-de-audio-que-esta-de-moda-564734", "output.json")
