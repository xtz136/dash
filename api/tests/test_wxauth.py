from django.urls import reverse
from django.test import TestCase


class WeChatTestCase(TestCase):
    def test_login(self):
        # without code should return 302
        resp = self.client.get(reverse('api:wechat_authorize'))
        self.assertEqual(resp.status, 302)
