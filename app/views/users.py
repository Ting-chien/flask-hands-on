from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect
)
from app.db import get_db, User
from app.views.auth import login_required

bp = Blueprint('users', __name__, url_prefix='/<lang_code>/users')

@bp.route('/')
def index():
    db = get_db()
    users = User.query.all()

    return render_template('users/index.html', users=users)

@bp.route('/delete/<int:user_id>', methods=('GET', 'POST'))
@login_required
def delete_user(user_id):
    if request.method == 'POST':
        db = get_db()
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('users.index'))

    return render_template('users/index.html')