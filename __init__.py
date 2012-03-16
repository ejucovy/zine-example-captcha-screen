# -*- coding: utf-8 -*-
"""
    example_captcha_screen
    ~~~~~~~~~~~~~~~~~~~~~~

    Sample CAPTCHA on comments form.
"""

from zine.api import _
from zine.application import get_request
from zine.models import COMMENT_BLOCKED_SPAM

from os.path import join, dirname

TEMPLATES = join(dirname(__file__), 'templates')

FAILED_TEST_MSG = _("Failed the captcha -- it's a robot!")
SKIPPED_TEST_MSG = _('Neglected to attempt the captcha, maybe a robot')

choices = ["dog", "cat", "chicken"]
import random

def set_session_captcha(post):
    req = get_request()
    req.session['captcha'] = random.choice(choices)
    req.session['captcha_mangled'] = req.session['captcha'].replace("o", "0").replace("a", "A").replace("i", "1").replace("e", "3")

def validate_session_captcha(req, comment):
    req = get_request()
    if 'captcha' not in req.session:
        return
    captcha = req.session.pop("captcha")
    if 'captcha_mangled' in req.session:
        del req.session['captcha_mangled']
    if 'captcha' not in req.form:
        comment.status = COMMENT_BLOCKED_SPAM
        comment.blocked_msg = SKIPPED_TEST_MSG
        return
    if req.form['captcha'] != captcha:
        comment.status = COMMENT_BLOCKED_SPAM
        comment.blocked_msg = FAILED_TEST_MSG
        return
        
def setup(app, plugin):
    app.add_template_searchpath(TEMPLATES)
    app.connect_event('before-comment-editor-rendered', set_session_captcha)
    app.connect_event('before-comment-saved', validate_session_captcha)
