from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from ._base import ApiView


# @method_decorator(csrf_exempt, name='dispatch')
class Entity(ApiView):

    """Docstring for Entity. """

    def api_empty(self, request, args):
        raise TypeError
        return self.success({'name': 'fff'})
