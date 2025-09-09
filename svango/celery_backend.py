from django.utils import timezone
from django_celery_results.backends.cache import CacheBackend


class SvangoCacheBackend(CacheBackend):

    def set(self, key:bytes|str, value:dict) -> None:
        status = value.get('status')
        if status == 'STARTED':
            value['date_start'] = timezone.now().isoformat()
        else:
            value['date_start'] = (self.get(key) or {}).get('date_start')
        super().set(key, value)
