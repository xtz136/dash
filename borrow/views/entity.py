from ._base import ApiView


class Entity(ApiView):

    """Docstring for Entity. """

    template_name = 'entity.html'

    def api_empty(self, request, args):
        raise TypeError
        return self.success({'name': 'fff'})
