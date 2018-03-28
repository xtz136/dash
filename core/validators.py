import re
from django.core.exceptions import ValidationError

phone_pat = re.compile(r'^1[3,4,5,7,8]\d{9}$')


def validate_phone(value):
    """
    /**
     * 手机号码: 
     * 13[0-9], 14[5,7, 9], 15[0, 1, 2, 3, 5, 6, 7, 8, 9], 17[0-9], 18[0-9]
     * 移动号段: 134,135,136,137,138,139,147,150,151,152,157,158,159,170,178,182,183,184,187,188
     * 联通号段: 130,131,132,145,155,156,170,171,175,176,185,186
     * 电信号段: 133,149,153,170,173,177,180,181,189
     */
     """
    if not phone_pat.match(value):
        raise ValidationError('请输入有效的手机号码')
    return value
