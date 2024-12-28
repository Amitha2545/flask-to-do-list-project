from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__,template_folder="/home/amitha/Documents/MAD/templates")
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Todo(db.Model):
    S_no=db.Column(db.Integer,primary_key=True)
    TO_DO_TITLE=db.Column(db.String(200),nullable=False)
    DESCRIPTION=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self)->str:
        return f"{self.S_no}-{self.TO_DO_TITLE}"
    # Create database tables
with app.app_context():
    db.create_all()

# @app.route('/admin')
# def admin():
#     return 'hello admin'
# @app.route('/student')
# def student():
#     return 'hello students'
# @app.route('/staff')
# def staff():
#     return 'hello staff'
# @app.route('/user/<name>')
# def user(name):
#     if name=='admin':
#         return redirect(url_for('admin'))
#     if name=='student':
#         return redirect(url_for('student'))
#     if name=='staff':
#         return redirect(url_for('staff'))

@app.route('/', methods=['GET', 'POST'])
def template():
    if request.method == 'POST':
        Title = request.form.get('todoTitle')
        description = request.form.get('todoDescription')
        todo = Todo(TO_DO_TITLE=Title, DESCRIPTION=description)
        db.session.add(todo) 
        db.session.commit()
        return redirect('/')
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/show')
def show():
    
    
    return "this is my show page"
@app.route('/Delete/<int:S_no>')
def delete(S_no):
    todo=Todo.query.filter_by(S_no=S_no).first()
    
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
@app.route('/Update/<int:S_no>',methods=['GET','POST'])
def Update(S_no):
    if request.method=='POST':
        TO_DO_TITLE=request.form['TO_DO_TITLE']
        DESCRIPTION=request.form['todoDescription']
        todo=Todo.query.filter_by(S_no=S_no).first()
        todo.TO_DO_TITLE=TO_DO_TITLE
        todo.DESCRIPTION=DESCRIPTION
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo=Todo.query.filter_by(S_no=S_no).first()
    return render_template('update.html', todo=todo)

    
if __name__=='__main__':
    app.run(debug=True,port=5000)