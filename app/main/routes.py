from datetime import datetime

from flask import flash, redirect, url_for, request, current_app, g, render_template, jsonify
from flask_login import login_required, current_user
from langdetect import detect, LangDetectException

from app import db
from app.main import bp
from app.main.forms import PostForm, FollowForm, EditProfileForm, SearchForm
from app.models import Post
from app.services import add_post, get_post_stream, get_user_by_username_or_404, get_user_by_username
from flask_babel import lazy_gettext as _l, get_locale

from app.translate import translate


@bp.before_request
def before_request():
    """Set last seen time to the User and init SearchForm."""
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()

    g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        language = _detect_post_language(form.post.data)
        add_post(body=form.post.data, author=current_user, language=language)
        flash(_l('Your post is now live!'))
        return redirect(url_for('main.index'))

    posts, next_url, prev_url = _paginate_posts(current_user.all_posts)

    return render_template('index.html', title='Home',
                           form=form, posts=posts,
                           next_url=next_url, prev_url=prev_url)


def _detect_post_language(text):
    try:
        language = detect(text)
    except LangDetectException:
        language = ''
    return language


@bp.route('/explore')
@login_required
def explore():
    posts, next_url, prev_url = _paginate_posts(get_post_stream)
    return render_template('index.html', title='Explore', posts=posts,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = get_user_by_username_or_404(username=username)

    posts, next_url, prev_url = _paginate_posts(user.own_posts)

    form = FollowForm()
    return render_template('user.html', user=user,
                           posts=posts, form=form, next_url=next_url,
                           prev_url=prev_url)


def _paginate_posts(posts_query):
    """Return post list for  current page and next and prev urls
    if exists."""
    page = request.args.get('page', 1, type=int)
    posts = posts_query().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = (url_for('main.index', page=posts.next_num)
                if posts.has_next else None)
    prev_url = (url_for('main.index', page=posts.prev_num)
                if posts.has_prev else None)
    return posts.items, next_url, prev_url


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(original_username=current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_l('Your changes have been saved'))
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = FollowForm()
    if form.validate_on_submit():
        user = get_user_by_username(username)
        if not user:
            flash(_l(f'User %(username)s not found', username=username))
        if user == current_user:
            flash(_l('You cannot follow yourself!'))
            return redirect(url_for('main.user', username=username))

        current_user.follow(user)
        db.session.commit()
        flash(_l(f'You are following %(username)s', username=username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = FollowForm()
    if form.validate_on_submit():
        user = get_user_by_username(username)
        if not user:
            flash(_l(f'User %(username)s not found', username=username))
        if user == current_user:
            flash(_l('You cannot unfollow yourself!'))

        current_user.unfollow(user)
        db.session.commit()
        flash(_l(f'You are not following %(username)s', username=username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.index'))


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    """AJAX request"""
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['desc_language'])})


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])
    next_url = (url_for('main.search', q=g.search_form.q.data, page=page+1)
                if total > page * current_app.config['POSTS_PER_PAGE'] else None)
    prev_url = (url_for('main.search', q=g.search_form.q.data, page=page-1)
                if page > 1 else None)
    return render_template('search.html', title=_l('Search'), posts=posts,
                           next_url=next_url, prev_url=prev_url)
