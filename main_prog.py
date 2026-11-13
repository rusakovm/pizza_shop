import os
from flask import Flask, render_template, request, redirect, url_for, session as browser_session, flash
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()
class Buylist(Base):
    __tablename__ = 'buylist'
    Id_pizza_list = Column('Id_pizza', Integer, primary_key=True)
    name_pizza_list = Column('name_pizza', String)
    quantity_list = Column('quantity', Integer)
    customer_list = Column('customer', Integer, ForeignKey('login.Id_akk'))
    def __init__(self, name_pizza_list, quantity_list, customer_list):
        self.name_pizza_list, self.quantity_list, self.customer_list = name_pizza_list, quantity_list, customer_list
class Buykart(Base):
    __tablename__ = 'buy_kart'
    Id_pizza = Column('Id_pizza', Integer, primary_key=True)
    name_pizza = Column('name_pizza', String)
    quantity = Column('quantity', Integer)
    customer = Column('customer', Integer, ForeignKey('login.Id_akk'))
    def __init__(self, name_pizza, quantity, customer):
        self.name_pizza, self.quantity, self.customer = name_pizza, quantity, customer
class Login(Base):
    __tablename__ = 'login'
    Id_akk = Column('Id_akk', Integer, primary_key=True)
    user_name = Column('user_name', String, unique=True)
    user_passwod = Column('user_passwod', String)
    def __init__(self, user_name, user_passwod):
        self.user_name, self.user_passwod = user_name, user_passwod
class Comment(Base):
    __tablename__ = 'comment'
    Id_comment = Column('Id_comment', Integer, primary_key=True)
    comment = Column('comment', String)
    writer = Column('writer', Integer, ForeignKey('login.Id_akk'))
    def __init__(self, comment, writer):
        self.comment, self.writer = comment, writer

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'local-dev-only-change-before-deployment')
engine = create_engine('sqlite:///' + os.path.join(os.path.dirname(__file__), 'mydb.db'))
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
PIZZAS = [
 {'name':'Маргарита','description':'Томаты, моцарелла, базилик и фирменный соус','price':490,'image':'margherita.png','tag':'Классика'},
 {'name':'Пепперони','description':'Пикантная пепперони, моцарелла и томатный соус','price':590,'image':'pepperoni.png','tag':'Хит продаж'},
 {'name':'Четыре сыра','description':'Моцарелла, чеддер, дорблю и пармезан','price':650,'image':'cheese.png','tag':'Нежная'},
]
def current_user():
    return browser_session.get('user_id')
@app.context_processor
def inject_user():
    return {'logged_in': current_user() is not None}
@app.route('/', methods=['GET','POST'])
def Buy_Kart():
    if request.method == 'POST':
        if not current_user():
            flash('Для заказа войдите или зарегистрируйтесь.', 'error')
            return redirect(url_for('voity'))
        name = request.form.get('name_pizza','')
        try: quantity = int(request.form.get('quantity','1'))
        except ValueError: quantity = 0
        if name not in [p['name'] for p in PIZZAS] or not 1 <= quantity <= 20:
            flash('Проверьте название и количество.', 'error')
            return redirect(url_for('Buy_Kart'))
        with Session.begin() as db:
            db.add(Buykart(name, quantity, current_user()))
        flash('Пицца добавлена в корзину!', 'success')
        return redirect(url_for('hello_world1'))
    return render_template('main/index.html', pizzas=PIZZAS)
@app.route('/voity', methods=['GET','POST'])
def voity():
    if request.method == 'POST':
        username=request.form.get('voity','').strip()
        password=request.form.get('voity_pass','')
        with Session.begin() as db:
            user=db.query(Login).filter_by(user_name=username).first()
            valid = bool(user and (check_password_hash(user.user_passwod,password) if user.user_passwod.startswith(('scrypt:', 'pbkdf2:')) else user.user_passwod == password))
            if valid:
                if not user.user_passwod.startswith(('scrypt:', 'pbkdf2:')):
                    user.user_passwod=generate_password_hash(password)
                browser_session.clear(); browser_session['user_id']=user.Id_akk
                return redirect(url_for('Buy_Kart'))
        flash('Неверный логин или пароль.', 'error')
    return render_template('main/voity.html')
@app.route('/createAkk', methods=['GET','POST'])
def createAkk():
    if request.method == 'POST':
        name=request.form.get('user_name','').strip(); password=request.form.get('user_passwod','')
        if len(name)<3 or len(password)<8:
            flash('Логин от 3 символов, пароль от 8.', 'error')
        else:
            with Session.begin() as db:
                if db.query(Login).filter_by(user_name=name).first():
                    flash('Логин уже занят.', 'error')
                else:
                    user=Login(name,generate_password_hash(password));db.add(user);db.flush()
                    browser_session.clear();browser_session['user_id']=user.Id_akk
                    return redirect(url_for('Buy_Kart'))
    return render_template('main/createAkk.html')
@app.route('/logout',methods=['POST'])
def logout():
    browser_session.clear();return redirect(url_for('Buy_Kart'))
@app.route('/shopbuy')
def hello_world1():
    if not current_user():return redirect(url_for('voity'))
    with Session() as db:
        items=db.query(Buykart).filter_by(customer=current_user()).all()
        rows=[{'name':i.name_pizza,'quantity':i.quantity,'price':next((p['price'] for p in PIZZAS if p['name']==i.name_pizza),0)} for i in items]
    return render_template('main/shop_buy.html',items=rows,total=sum(x['price']*x['quantity'] for x in rows))
@app.route('/createAkg',methods=['GET','POST'])
def createAkg():
    if not current_user():return redirect(url_for('voity'))
    if request.method=='POST':
        with Session.begin() as db:
            items=db.query(Buykart).filter_by(customer=current_user()).all()
            if not items:
                flash('Корзина пуста.', 'error')
            else:
                for item in items:db.add(Buylist(item.name_pizza,item.quantity,current_user()));db.delete(item)
                flash('Демонстрационный заказ оформлен!', 'success')
        return redirect(url_for('hello_world1'))
    return render_template('main/createAkg.html')
@app.route('/createcomment',methods=['GET','POST'])
def createcomment():
    if not current_user():return redirect(url_for('voity'))
    if request.method=='POST':
        value=request.form.get('comment','').strip()
        if 3<=len(value)<=500:
            with Session.begin() as db:db.add(Comment(value,current_user()))
            flash('Отзыв опубликован!', 'success');return redirect(url_for('coment'))
        flash('Отзыв должен содержать от 3 до 500 символов.', 'error')
    return render_template('main/createcomment.html')
@app.route('/coment')
def coment():
    with Session() as db:
        rows=db.query(Comment,Login.user_name).outerjoin(Login,Comment.writer==Login.Id_akk).order_by(Comment.Id_comment.desc()).all()
        articles=[{'comment':c.comment,'author':name or 'Гость'} for c,name in rows]
    return render_template('main/coment_veiw.html',articles=articles)
if __name__=='__main__':app.run(debug=False)
