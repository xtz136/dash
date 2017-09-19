import pytest
from mixer.backend.django import mixer
from django.contrib.admin.sites import AdminSite

pytestmark = pytest.mark.django_db

from .. import admin
from .. import models


class TestAdmin:
    def test_title(self):
        site = AdminSite()
        company_admin = admin.CompanyModelAdmin(models.Company, site)

        obj = mixer.blend('crm.Company', expire_at=None)
        result = company_admin.view_expired_at(obj)
        assert result is None, '应该返回空'
