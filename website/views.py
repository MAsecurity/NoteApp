from flask import Blueprint , render_template, request, flash, redirect, url_for 
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)

@views.route("/home", methods=['GET','POST'])
@views.route("/", methods=['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")
        if len(note) < 1:
            flash("Note is too short!, add some data", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category="success")
    return render_template("home.html", user=current_user)


@views.route("/delete-note/<id>")
@login_required
def delete_note(id):
    note = Note.query.filter_by(id=id).first()
    if not note:
        flash("Note does not Exist", category="error")
    elif current_user.id != note.user_id:
        flash("You do not have permission to delete this!", category="error")
    else:
        db.session.delete(note)
        db.session.commit()
        flash("Post deleted", category="success")

    return redirect(url_for("views.home"))
