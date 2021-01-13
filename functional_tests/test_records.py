from django.conf import settings
from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore

from . import FunctionalTest

User = get_user_model()


class PacksTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        # help(SESSION_KEY)
        # No Python documentation found for '_auth_user_id'.
        # 此“SESSION_KEY”，非彼“session.session_key”
        session[SESSION_KEY] = user.pk
        # help(BACKEND_SESSION_KEY)
        # No Python documentation found for '_auth_user_backend'.
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        # 执行“save”前，“session.session_key”的值为空
        session.save()
        # 执行 save 后，“session.session_key”值才产生
        # 如，'3eljowzg64id33ocj0ikz8803gabu632'
        # 即浏览器“cookie”中保存的键“sessionid” 对应的值。

        # 设置“cookie”前，先访问该网站
        # 404 页的响应最快
        self.browser.get(self.live_server_url + '/404_no_such_url/')
        # SESSION_COOKIE_NAME 的默认值是“sessionid”
        self.browser.add_cookie(
            dict(
                name=settings.SESSION_COOKIE_NAME,
                value=session.session_key,
                path='/'
            )
        )