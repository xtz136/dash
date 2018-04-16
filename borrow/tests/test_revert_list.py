import pytest

from ..views import revert_list
from ..perm_types import revert_list_perm
from .test_base import BaseApiView

pytestmark = pytest.mark.django_db


class TestRevertListApiView(BaseApiView):

    _view = revert_list.RevertListApiView
    _view_url = 'api.revert_list'
    _perm = revert_list_perm
    _test_api_chain = (
        ('api_filter', 'view_codename', True),
    )
