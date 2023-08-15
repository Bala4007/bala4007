from flask import Flask, render_template,request,flash,redirect,url_for,session
import sqlite3

app = Flask(__name__)
app.secret_key="123"

con=sqlite3.connect("database.db")
con.execute("create table if not exists customer(pid integer primary key,name text,password text,contact integer,mail text)")
con.execute("create table if not exists flight1(fid integer primary key,flightnumber integer, fname text,start text,end text,date DATE,time text,availableseet text)")
con.execute("create table if not exists admin1(pid integer primary key,adminname text,password text,contact integer,mail text)")
con.close()

@app.route('/')
def main():
    return render_template('index1.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from customer where name=? and password=?",(name,password))
        data=cur.fetchone()

        if data:
            session["name"]=data["name"]
            session["mail"]=data["mail"]
            return redirect("customer")
        else:
            flash("Username and Password Mismatch","danger")
    return redirect(url_for("index"))

@app.route('/signin',methods=["GET","POST"])
def signin():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from admin1 where adminname=? and password=?",(name,password))
        data=cur.fetchone()
        if data:
            session["name"]=data["adminname"]
            session["mail"]=data["mail"]
            return redirect("adminlogin")
        else:
            flash("Username and Password Mismatch","danger")
    return redirect(url_for("admin"))

@app.route('/adminlogin',methods=["GET","POST"])
def adminlogin():
    return render_template("adminlogin.html")

@app.route('/customer',methods=["GET","POST"])
def customer():
    return render_template("customer.html")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            name=request.form['name']
            password=request.form['password']
            contact=request.form['contact']
            mail=request.form['mail']
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("insert into customer(name,password,contact,mail)values(?,?,?,?)",(name,password,contact,mail))
            con.commit()
            flash("Record Added  Successfully","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:
            return redirect(url_for("index"))
            con.close()

    return render_template('register.html')

@app.route('/Add',methods=['GET','POST'])
def Add():
    if request.method=='POST':
        try:
            name=request.form['name']
            password=request.form['password']
            contact=request.form['contact']
            mail=request.form['mail']
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("insert into admin1(adminname,password,contact,mail)values(?,?,?,?)",(name,password,contact,mail))
            con.commit()
            flash("Record Added  Successfully","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:
            return redirect(url_for("admin"))
            con.close()

    return render_template('admin register.html')

@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=='POST':
        start=request.form['From']
        end=request.form['to']
        date1=request.form['date1']
        time1=request.form['time1']
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from flight1 where start=? and end=? and time=? and date=?",(start,end,time1,date1))
        data=cur.fetchall()
        con.close()
        for i in data:
            if data and int(i["availableseet"])>0:
                return render_template("flight.html",data=data)
            else:
                flash("flight not available","danger")
    
    return render_template("customer.html")

@app.route('/book/<string:fid>/<string:avl>',methods=['GET','POST'])
def book(fid,avl):
    con=sqlite3.connect("database.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("select * from flight1 where fid=?",(fid))
    data=cur.fetchone()
    con.close()
    if request.method=='POST':
        try:
            n=request.form['n']
            avl1=int(avl)-int(n)
            d="deccan"
            if avl1>=0:
                con = sqlite3.connect("database.db")
                cur = con.cursor()
                cur.execute("UPDATE flight1 SET availableseet=? where fid=?",(avl1,fid))
                con.commit()
                flash("Ticket Booked successfully Successfully","success")
            else:
                flash("please eenter valid number","danger")
        except:
            flash("Error in Update Operation","danger")
        finally:
            return redirect(url_for("customer"))
            con.close()
    return render_template("passenger.html",data=data)

@app.route('/flight')
def flight():
    return render_template('flight.html')

@app.route('/update',methods=['GET','POST'])
def update():
    if request.method=='POST':
        try:
            number=request.form['flight number']
            name=request.form['flightname']
            start=request.form['from']
            end=request.form['to']
            date=request.form['date']
            time=request.form['time']
            available=request.form['Avl']
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("insert into flight1(flightnumber,fname,start,end,date,time,availableseet)values(?,?,?,?,?,?,?)",(number,name,start,end,date,time,available))
            con.commit()
            flash("Record Added  Successfully","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:
            return redirect(url_for("adminlogin"))
            con.close()
    return render_template('adminlogin.html')

@app.route('/remove',methods=['GET','POST'])
def remove():
    if request.method=='POST':
        try:
            name=request.form['flightname']
            number=request.form['flightnumber']
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("DELETE from flight1 where fname=? and flightnumber=?",(name,number))
            con.commit()
            flash("Record deleted  Successfully","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:
            return redirect(url_for("adminlogin"))
            con.close()
    return render_template('adminlogin.html')

@app.route('/details',methods=['GET','POST'])
def details():
    if request.method=='POST':
        name=request.form['flightname']
        time=request.form['flighttime']
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from flight1 where fname=? and time=?",(name,time))
        data=cur.fetchall()
        con.close()
        if data:
            return render_template("details.html",data=data)
        else:
            flash("flight not available","danger")
    return redirect(url_for("adminlogin"))
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("main"))
if __name__ == '__main__':
    app.run(debug=True)
