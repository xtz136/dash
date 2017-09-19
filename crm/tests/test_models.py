import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db


class TestCompany:
    def test_init(self):
        obj = mixer.blend('crm.Company')
        assert obj.pk == 1, 'Should save an instance'

    def test_title(self):
        obj = mixer.blend('crm.Company', title='我是标题')
        assert obj.title == '我是标题', '应该返回我是标题'
