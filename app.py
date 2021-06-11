from flask import Flask, render_template,request,redirect,url_for,session

import mysql.connector


app=Flask(__name__)
@app.route('/')
def home():
	return redirect(url_for("pview"))



#product loading...
@app.route('/add',methods=['POST','GET'])
def add():
	db = mysql.connector.connect(host='127.0.0.1',user='root',password='',database='inventory')
	cursor = db.cursor()
	if request.method=='POST':
		product_id=request.form['product_id']
		product_name=request.form['product_name']
		warehouse=request.form['warehouse']
		quantity=request.form['quantity']
		cursor.execute("INSERT INTO product (product_id,product_name,warehouse,quantity) VALUES (%s,%s,%s,%s)",(product_id,product_name,warehouse,quantity))
		db.commit()
		cursor.close()
		return redirect(url_for("pview"))

	return render_template('add.html')


@app.route('/pdelete',methods=['GET','POST'])
def pdelete():
	db = mysql.connector.connect(host='127.0.0.1',user='root',password='',database='inventory')
	cursor = db.cursor()
	product_id =request.args.get('product_id')
	sql="DELETE FROM product WHERE product_id=%s"
	cursor.execute(sql,(product_id,))
	db.commit()
	cursor.close()
	return redirect(url_for("pview"))



@app.route('/pupdate',methods=['GET','POST'])
def pupdate():
	db = mysql.connector.connect(host='127.0.0.1',user='root',password='',database='inventory')
	cursor = db.cursor()
	product_id =request.args.get('product_id')
	if request.method=='POST':
		product_id=request.form['product_id']
		product_name=request.form['product_name']
		warehouse=request.form['warehouse']
		quantity=request.form['quantity']
		cursor.execute("UPDATE product SET product_name=%s,warehouse=%s,quantity=%s WHERE product_id=%s",(product_name,warehouse,quantity,product_id))
		db.commit()
	sql="SELECT * FROM product WHERE product_id=%s"
	cursor.execute(sql,(product_id,))
	result=cursor.fetchone()
	return render_template("pupdate.html",result=result)


@app.route('/pview')
def pview():
	db = mysql.connector.connect(host='127.0.0.1',user='root',password='',database='inventory')
	cursor = db.cursor()
	cursor.execute("SELECT product_id,product_name,warehouse,quantity FROM product")
	result=cursor.fetchall()
	return render_template('home.html',result=result)

#location loading...
@app.route('/ladd',methods=['POST','GET'])
def ladd():
	db = mysql.connector.connect(host='127.0.0.1',user='root',password='',database='inventory')
	cursor = db.cursor()
	if request.method=='POST':
		location_id=request.form['location_id']
		location_name=request.form['location_name']
		discription=request.form['discription']
		cursor.execute("INSERT INTO location (location_id,location_name,discription) VALUES (%s,%s,%s)",(location_id,location_name,discription))
		db.commit()
		cursor.close()
		return redirect(url_for("pview"))
	return render_template('ladd.html')



@app.route('/ldelete',methods=['GET','POST'])
def ldelete():
	db = mysql.connector.connect(host='127.0.0.1',user='root',password='',database='inventory')
	cursor = db.cursor()
	location_id =request.args.get('location_id')
	sql="DELETE FROM location WHERE location_id=%s"
	cursor.execute(sql,(location_id,))
	db.commit()
	cursor.close()
	return redirect(url_for("lview"))

@app.route('/lupdate',methods=['GET','POST'])
def lupdate():
	db = mysql.connector.connect(host='127.0.0.1',user='root',password='',database='inventory')
	cursor = db.cursor()
	location_id =request.args.get('location_id')
	if request.method=='POST':
		location_id=request.form['location_id']
		location_name=request.form['location_name']
		discription=request.form['discription']
		cursor.execute("UPDATE location SET location_name=%s,discription=%s WHERE location_id=%s"(location_name,location_id,discription))
		db.commit()
		cursor.close()
		return "success"
		cursor=db.connection.cursor()
	sql="SELECT * FROM location WHERE location_id=%s"
	cursor.execute(sql,(location_id,))
	result=cursor.fetchone()
	return render_template("lupdate.html",result=result)


@app.route('/lview')
def lview():
	db = mysql.connector.connect(host='127.0.0.1',user='root',password='',database='inventory')
	cursor = db.cursor()
	cursor.execute("SELECT location_id,location_name,discription FROM location")
	result=cursor.fetchall()
	return render_template('lhome.html',result=result)


#movement loading..


@app.route('/madd',methods=['POST'])
def madd():
	db = mysql.connector.connect(host='127.0.0.1',user='root',password='',database='inventory')
	cursor = db.cursor()
	movement_id=request.form['movement_id']
	from_location=request.form['from_location1']
	to_location=request.form['to_location']
	product_name=request.form['product_name']
	quantity=request.form['quantity']
	cursor.execute("INSERT INTO movement (movement_id,from_location,to_location,product_name,quantity) VALUES (%s,%s,%s,%s,%s)",(movement_id,from_location,to_location,product_name,quantity))
	db.commit()
	tq=int(quantity)
	cursor.execute("UPDATE product SET quantity=quantity-("+str(tq)+") WHERE product_name=%s and warehouse=%s ",(product_name,from_location))
	db.commit()
	cursor.close()
	return redirect(url_for("mview"))

@app.route('/movementadd')
def movementadd():
	return render_template('madd.html')


@app.route('/mdelete',methods=['GET','POST'])
def mdelete():
	db = mysql.connector.connect(host='127.0.0.1',user='root',password='',database='inventory')
	cursor = db.cursor()
	movement_id =request.args.get('movement_id')
	sql="DELETE FROM movement WHERE movement_id=%s"
	cursor.execute(sql,(movement_id,))
	db.commit()
	cursor.close()
	return redirect(url_for("mview"))


@app.route('/mupdate',methods=['GET','POST'])
def mupdate():
	db = mysql.connector.connect(host='127.0.0.1',user='root',password='',database='inventory')
	cursor = db.cursor()
	movement_id =request.args.get('movement_id')
	if request.method=='POST':
		movement_id=request.form['movement_id']
		ltimestamp=request.form['ltimestamp']
		from_location=request.form['from_location']
		to_location=request.form['to_location']
		product_name=request.form['product_name1']
		quantity=request.form['quantity']
		cursor.execute("UPDATE movement SET ltimestamp=%s,from_location=%s,to_location=%s,product_name=%s,quantity=%s WHERE movement_id=%s",(ltimestamp,from_location,to_location,product_name,quantity,movement_id))
		db.commit()
		return redirect(url_for("mview"))
	sql="SELECT * FROM movement WHERE movement_id=%s"
	cursor.execute(sql,(movement_id,))
	result=cursor.fetchone()
	return render_template("mupdate.html",result=result)


@app.route('/mview')
def mview():
	db = mysql.connector.connect(host='127.0.0.1',user='root',password='',database='inventory')
	cursor = db.cursor()
	cursor.execute("SELECT movement_id,ltimestamp,from_location,to_location,product_name,quantity FROM movement")
	result=cursor.fetchall()
	return render_template('mhome.html',result=result)


app.run(debug=True)
