from django.db.models import Q
from inputtools.models import Wordlist
from inputtools.settings import suggestion_settings
from django.db.models.functions import Length

def suggest(text, dst_lang):
	queryset = Wordlist.objects.filter(
    Q(word__istartswith=text) | Q(word__icontains=text)
	).order_by(Length('word').asc())[:suggestion_settings.NUM_WORDS]
	return [obj.word for obj in queryset]
