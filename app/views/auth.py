from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    g,
)
from app.db import get_db, User
from werkzeug.security import check_password_hash, generate_password_hash
from app.validate import AccountForm, LoginForm
from functools import wraps

bp = Blueprint('auth', __name__, url_prefix='/<lang_code>/auth')

# 在每次收到 request 時檢查前端 session 是否帶有 user_id，有的話則將用戶存於 g.user
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db = get_db()
        g.user = User.query.filter_by(id=user_id).first()

# 建立一個 decorator 來驗證使用者是否已登入
def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = AccountForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        if User.query.filter_by(email=email).first() is not None:
            error = f"User {email} is already registered."

        if error is None:
            print('add a user')
            user = User(
                firstname,
                lastname,
                email,
                generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html', form=form)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        print('check')
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = User.query.filter_by(email=email).first()

        if user is None:
            error = 'User not found'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('users.index'))

        flash(error)

    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    print('logout')
    session.clear()
    return redirect(url_for('users.index'))