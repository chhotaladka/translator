from django.conf import settings
from django.test.signals import setting_changed

DEFAULTS = {
    'BACKEND': 'dummy',
    'NUM_WORDS': 5,
    }

class SuggestionSettings(object):
    def __init__(self, defaults=None):
        self.defaults = defaults or DEFAULTS
        self._cached_attrs = set()
           
    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid API setting: '%s'" % attr)

        val = self.defaults[attr]
        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()

if settings.SUGGESTION:
    suggestion_settings = SuggestionSettings(settings.SUGGESTION)
else:         
    suggestion_settings = SuggestionSettings(DEFAULTS)

def reload_api_settings(*args, **kwargs):
    setting = kwargs['setting']
    if setting == 'SUGGESTION':
        suggestion_settings.reload()


setting_changed.connect(reload_api_settings)
