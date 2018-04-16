import pytest

from ..views import entity_list
from ..perm_types import entity_list_perm
from .test_base import BaseApiView

pytestmark = pytest.mark.django_db


class TestEntityListApiView(BaseApiView):

    _view = entity_list.EntityListApiView
    _view_url = 'api.entity_list'
    _perm = entity_list_perm
    _test_api_chain = (
        ('api_filter', 'view_codename', True),
        ('api_filter_all', 'view_codename', False),
    )
