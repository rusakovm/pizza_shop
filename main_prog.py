from flask import Flask, render_template, url_for, request,redirect
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user_name_G = "None"
user_name_U = "None"
user_name_W = True
Base = declarative_base()


class Buylist (Base):
    __tablename__ = "buylist"
    Id_pizza_list = Column("Id_pizza", Integer, primary_key=True)
    name_pizza_list = Column("name_pizza", String)
    quantity_list = Column ("quantity", Integer)
    customer_list = Column("customer", Integer, ForeignKey("login.Id_akk"))

    def __init__(self, name_pizza_list, quantity_list, customer_list):
        self.name_pizza_list = name_pizza_list
        self.quantity_list = quantity_list
        self.customer_list = customer_list

    def __repr__(self):
        return f"{self.name_pizza_list} {self.quantity_list} {self.customer_list}"




class Buykart (Base):
    __tablename__ = "buy_kart"
    Id_pizza = Column("Id_pizza", Integer, primary_key=True)
    name_pizza = Column("name_pizza", String)
    quantity = Column ("quantity", Integer)
    customer = Column("customer", Integer, ForeignKey("login.Id_akk"))

    def __init__(self, name_pizza, quantity, customer):
        self.name_pizza = name_pizza
        self.quantity = quantity
        self.customer = customer

    def __repr__(self):
        return f"{self.name_pizza} {self.quantity} {self.customer}"


class Login (Base):
    __tablename__ = "login"
    Id_akk = Column("Id_akk", Integer, primary_key=True)
    user_name = Column("user_name", String)
    user_passwod = Column("user_passwod", String)

    def __init__(self, user_name, user_passwod):
        self.user_name = user_name
        self.user_passwod = user_passwod

    def __repr__(self):
        return f"{self.user_name} {self.user_passwod}"


class Comment (Base):
    __tablename__ = "comment"
    Id_comment = Column("Id_comment", Integer, primary_key=True)
    comment = Column("comment", String)
    writer = Column("writer", Integer, ForeignKey("login.Id_akk"))

    def __init__(self, comment, writer):
        self.comment = comment
        self.writer = writer

    def __repr__(self):
        return f"{self.comment} writed by {self.writer}"


engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

session.commit()
app = Flask(__name__)





@app.route('/', methods = ['POST', 'GET'])
def Buy_Kart():
    global user_name_G
    global user_name_U
    if request.method == 'POST':
        Session = sessionmaker(autoflush=False, bind=engine, autocommit=False)
        session = Session()
        name_pizza = request.form['name_pizza']
        quantity = int(request.form['quantity'])
        try:
            if user_name_G == "None":
                return redirect("/voity")
            else:
                p = Buykart(name_pizza, quantity, user_name_G)
                session.add(p)
                session.commit()
                return redirect("/")
        except: 
            return "Ошибка со стороны сайта"
    else:
        return render_template("main/index.html", status=user_name_U)





@app.route('/createcomment', methods = ['POST', 'GET'])
def createcomment():
    global user_name_U
    if user_name_G == "None":
        return redirect("/voity")
    else:
        if request.method == 'POST':
            Session = sessionmaker(autoflush=False, bind=engine, autocommit=False)
            session = Session()
            comment = request.form['comment']
            try:
                p = Comment(comment, user_name_G)
                session.add(p)
                session.commit()
                return redirect("/")
            except:
                return "Ошибка со стороны сайта"
        else:
            return render_template("main/createcomment.html", status = user_name_U)





@app.route('/voity', methods = ['POST', 'GET'])
def voity():
    global user_name_G
    global user_name_U
    if request.method == 'POST':
        voity = request.form['voity']
        voity_pass = request.form['voity_pass']
        try:
            if session.query(Login.user_name).filter_by(user_name=voity, user_passwod=voity_pass).first() is not None:
                rt = session.query(Login.Id_akk, Login.user_name).filter_by(user_name=voity).first()
                user_name_G = str(rt[0])
                user_name_U = str(rt[1])
                return redirect("/")
            else:
                return "Введен либо не правильный пароль либо не правильный логин"
        except:
            return "Ошибка со стороны сайта"
    else:
        return render_template("main/voity.html")










@app.route('/cart', methods = ['POST', 'GET'])
def cart():
    global user_name_U
    global user_name_G
    global user_name_W
    if request.method == 'POST':
        id = request.form['id']
        print(id)
        try:
            session.query(Buykart).filter_by(Id_pizza=id).delete(synchronize_session='fetch')
            session.commit()
            return redirect("/cart")
        except:
            return "Ошибка со стороны сайта"
    else:
        cart_user = session.query(Buykart.name_pizza, Buykart.Id_pizza, Buykart.quantity).filter_by(customer=user_name_G)
        user_name_W = session.query(Buykart.customer).filter_by(customer = user_name_G).first() is None
        print(user_name_W)
        return render_template("main/cart.html", cart_user=cart_user, status=user_name_U, newcart = user_name_W)






# @app.route('/cart')
# def cart():
#     global user_name_U
#     cart_user = session.query(Buykart.name_pizza, Buykart.Id_pizza, Buykart.quantity).filter_by(customer=user_name_G)
#     return render_template("main/cart.html", cart_user=cart_user, status = user_name_U)


@app.route('/comment')
def coment():
    global user_name_U
    articles = session.query(Comment.comment, Login.user_name).filter(Comment.writer == Login.Id_akk)
    return render_template("main/coment_veiw.html", articles=articles, status = user_name_U)



@app.route('/createzakaz', methods = ['POST', 'GET'])
def createzakaz():
    global user_name_G
    global user_name_U
    if user_name_G == "None":
        return redirect("/voity")
    else:
        if request.method == 'POST':
            Session = sessionmaker(autoflush=False, bind=engine, autocommit=False)
            session = Session()

            try:
                res = session.query(Buykart.name_pizza, Buykart.quantity, Buykart.customer).filter_by(customer=user_name_G)
                for r in res:
                    yu = Buylist(r[0], r[1], r[2])
                    session.add(yu)
                    session.commit()

                session.query(Buykart).filter_by(customer=user_name_G).delete(synchronize_session='fetch')

                session.commit()


                return redirect("/")

            except:
                return "Ошибка со стороны сайта"
        else:
            Session = sessionmaker(autoflush=False, bind=engine, autocommit=False)
            session = Session()
            userres = session.query(Buykart.name_pizza, Buykart.quantity, Buykart.customer).filter_by(customer=user_name_G)
            sum = 0
            for i in userres:
                if i[0] == 'Пицца с грибами':
                    sum += i[1]*350
                elif i[0] == 'Пицца с колбасками и пепперони':
                    sum += i[1] * 540
                elif i[0] == 'Пицца с Сыром':
                    sum += i[1] * 700
            return render_template("main/createzakaz.html",userres = userres, status = user_name_U, sum = sum)



@app.route('/createAkk', methods = ['POST', 'GET'])
def createAkk():
    global user_name_G
    global user_name_U
    if request.method == 'POST':
        Session = sessionmaker(autoflush=False, bind=engine, autocommit=False)
        session = Session()
        user_name = request.form['user_name']
        user_passwod = request.form['user_passwod']
        try:
            if session.query(Login.user_name).filter_by(user_name=user_name).first() is None:
                p = Login(user_name, user_passwod)
                session.add(p)
                session.commit()
                rt = session.query(Login.Id_akk, Login.user_name).filter_by(user_name=user_name).first()
                user_name_G = str(rt[0])
                user_name_U = str(rt[1])
                return redirect("/")
            else:
                return "Не логин уже занят"
        except:
            return "Ошибка со стороны сайта"
    else:
        return render_template("main/createAkk.html")



@app.route('/buylist', methods = ['POST', 'GET'])
def buylist():
    global user_name_U
    global user_name_G
    global user_name_W
    if user_name_G == "None":
        return redirect("/voity")
    else:
        cart_user = session.query(Buylist.name_pizza_list, Buylist.Id_pizza_list, Buylist.quantity_list).filter_by(customer_list=user_name_G)
        user_name_W = session.query(Buylist.customer_list).filter_by(customer_list = user_name_G).first() is None
        return render_template("main/buylist.html", cart_user=cart_user, status=user_name_U, newcart = user_name_W)





app.run()