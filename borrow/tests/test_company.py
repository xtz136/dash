import pytest

from ..views import company
from ..perm_types import company_perm
from .test_base import BaseApiView

pytestmark = pytest.mark.django_db


class TestCompanyApiView(BaseApiView):

    _view = company.CompanyApiView
    _view_url = 'api.company'
    _perm = company_perm
    _test_api_chain = (
        ('api_list', 'view_codename', True),
        ('api_filter', 'view_codename', True),
    )
