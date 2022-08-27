from kavenegar import *
from django.contrib.auth.mixins import UserPassesTestMixin


def send_otp_code(phone_number, code):  # with this function we connect to some services and use them for sending a SMS
    pass
    # try:
    #     api = KavenegarAPI('34796A5264374144466D773279316F36666A696F77522B32745942706F504C62507077356846534A4244733D')
    #     params = {
    #         'sender': '',
    #         'receptor': phone_number,
    #         'message': f'کد تایید شما{code}  '}
    #     response = api.sms_send(params)
    #     print(response)
    #
    # except APIException as e:
    #     print(e)
    # except HTTPException as e:
    #     print(e)


class UserIsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin
