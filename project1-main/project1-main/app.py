from flask import Flask,render_template,request,redirect,url_for
import pymysql

app=Flask(__name__)

db=pymysql.connect(user='root1',password='root',host='localhost', database='restarunt')

cursor = db.cursor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_dish', methods=['GET', 'POST', 'DELETE'])

def add_dish():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        category = request.form['category']

        query = "INSERT INTO dishes (name,price,category) VALUES (%s, %s, %s)"
        values = (name, price, category)

        cursor.execute(query, values)
        db.commit()
        return redirect(url_for('after_adding_dish'))
    return render_template('add_dish.html')

@app.route('/after_adding_dish')
def after_adding_dish():
    return render_template('after_adding_dish.html')

@app.route('/update_dish', methods=['GET', 'POST'])
def update_dish():
    if request.method == 'POST':
        dish_id = int(request.form['dish_id'])
        new_price = float(request.form['new_price'])

        query = "UPDATE dishes SET price = %s WHERE id = %s"
        values = (new_price, dish_id)
        cursor.execute(query,values)
        db.commit()
        return render_template('update_dish.html',message='Dish updated successfully')
    return render_template('update_dish.html')

@app.route('/remove_dish',methods=['GET', 'POST'])
def remove_dish():
    if request.method == 'POST':
        dish_id = int(request.form['dish_id'])
        query = 'DELETE FROM dishes WHERE id = %s'
        values = (dish_id,)
        cursor.execute(query, values)
        db.commit()
        return render_template('remove_dish.html',message='Dish removed successfully')
    return render_template('remove_dish.html')

@app.route('/display_dishes')
def display_dishes():
    query = "SELECT * FROM dishes"
    cursor.execute(query)
    dishes = cursor.fetchall()
    total_bill = sum(dish[2] for dish in dishes)
    return render_template('display_dish.html', dishes=dishes, total_bill=total_bill)

if __name__=='__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
