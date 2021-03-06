from flask import session, redirect, url_for, flash
from functools import wraps
#登陆验证
def login_check(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not session.get('user'):
            flash('请登陆后再来操作', 'warning')
            return redirect(url_for('admin.login'))
        return func(*args, **kwargs)
    return inner

# 管理员验证
def rule_check(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not session.get('user') == 'admin':
            flash('你没有权限访问,请使用管理员账号登录！', 'warning')
            return redirect(url_for('admin.manage'))
        return func(*args, **kwargs)
    return inner

