from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newflask.db'
db = SQLAlchemy(app)

#Модель поста
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)

#Главная страница
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

#Все посты
@app.route('/posts')
def posts():
    all_posts = Post.query.all()
    return render_template('posts.html', posts=all_posts)

#Для перехода чтения полного поста 'Читать дальше'
@app.route('/post_detail/<int:id>')
def post_detail(id):
    post = Post.query.get_or_404(id)
    return render_template('post_detail.html', post=post)


#Для удаление поста
@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')



#Добавление нового поста
@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')

        if not title or not text:
            return 'Пожалуйста, заполните все поля!'


        new_post = Post(title=title, text=text)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')

    return render_template('create.html')



if __name__ == '__main__':
    app.run(debug=True)