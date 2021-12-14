from flask import Flask, render_template, redirect, request
import os
import sqlite3

app = Flask(__name__)
port = int(os.getenv("PORT", 9090))

def connect():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/')
def index():
    connection = connect()

    products = connection.execute('SELECT * FROM spesa WHERE toTake=0 ORDER BY count').fetchall()
    spesa = connection.execute('SELECT * FROM spesa WHERE toTake=1 ORDER BY category').fetchall()
    
    connection.close()

    return render_template('index.html', products=products, spesa=spesa)

@app.route('/<int:idx>/add', methods=('POST',))
def add(idx):
    connection = connect()

    name = request.form['name']
    if len(name) == 0:
        connection.execute('DELETE FROM spesa WHERE id=?', (idx,))
        connection.commit()

        connection.close()
        
        return redirect('/')
        
    quantity = request.form['quantity']
    category = request.form['category']

    cur = connection.cursor()
    count = cur.execute('SELECT count FROM spesa WHERE id=?', (idx,)).fetchone()[0]
    count += 1
    connection.execute('UPDATE spesa SET toTake=1, name=?, quantity=?, category=?, count=? WHERE id=?', (name, quantity, category, count, idx,))
    connection.commit()

    connection.close()
    return redirect('/')
    
@app.route('/new', methods=('POST',))
def new():
    connection = connect()
        
    name = request.form['name']
    quantity = request.form['quantity']
    category = request.form['category']
    
    connection.execute('INSERT INTO spesa (name, quantity, category, count, toTake) VALUES (?,?,?,0,1)', (name, quantity, category))
    connection.commit()    

    connection.close()
    return redirect('/')

@app.route('/<int:idx>/update', methods=('POST',))
def update(idx):
    connection = connect()
    print(request.form['quantity'])
    connection.execute('UPDATE spesa SET quantity=? WHERE id=?', (request.form['quantity'], idx))
    connection.commit()    

    connection.close()
    return redirect('/')

@app.route('/<int:idx>/take', methods=('POST',))
def take(idx):
    connection = connect()
    
    connection.execute('UPDATE spesa SET toTake=0 WHERE id=?', (idx,))
    connection.commit()

    connection.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, threaded=True)

