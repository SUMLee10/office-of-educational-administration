import base64

import fernet as fernet
from aiohttp import web


from serv.config import web_routes, home_path

import serv.error_views
import serv.main_views
import serv.grade_views
import serv.student_views
import serv.grade_actions
import serv.course_views
import serv.login_views
import serv.login_actions
import serv.course_actions
from cryptography import fernet
from aiohttp import web
from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage

app = web.Application()
app.add_routes(web_routes)
app.add_routes([web.static("/", home_path / "static")])

if __name__ == "__main__":
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, EncryptedCookieStorage(secret_key))
    web.run_app(app, port=8080)
