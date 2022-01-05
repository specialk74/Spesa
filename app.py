from flask import Flask, render_template, redirect, request, jsonify
import os
import sqlite3

app = Flask(__name__)
port = int(os.getenv("PORT", 9090))

def connect():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/spesa')
def index():
    connection = connect()

    products = connection.execute('SELECT * FROM spesa WHERE toTake=0 ORDER BY count, category').fetchall()
    spesa = connection.execute('SELECT * FROM spesa WHERE toTake=1 ORDER BY category').fetchall()
    
    connection.close()

    return render_template('index.html', products=products, spesa=spesa)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    connection = connect()
    cur = connection.cursor()
    
    search = request.args.get('q')
    #query = db_session.query(Movie.title).filter(Movie.title.like('%' + str(search) + '%'))
    
    cur.execute('SELECT name FROM spesa WHERE toTake=0 and name LIKE ? ORDER BY count', ('%'+search+'%',))
    data = dict(result=[dict(r) for r in cur.fetchall()])
    print(data)
    return jsonify(matching_results=data)

@app.route('/<int:idx>/add', methods=('POST',))
def add(idx):
    connection = connect()

    name = request.form['name']
    if len(name) == 0:
        connection.execute('DELETE FROM spesa WHERE id=?', (idx,))
        connection.commit()

        connection.close()
        
        return redirect('/spesa')
        
    quantity = request.form['quantity']
    category = request.form['category']

    cur = connection.cursor()
    count = cur.execute('SELECT count FROM spesa WHERE id=?', (idx,)).fetchone()[0]
    count += 1
    connection.execute('UPDATE spesa SET toTake=1, name=?, quantity=?, category=?, count=? WHERE id=?', (name, quantity, category, count, idx,))
    connection.commit()

    connection.close()
    return redirect('/spesa')
    
@app.route('/new', methods=('POST',))
def new():
    connection = connect()
        
    idValue = request.form['id']
    name = request.form['name']
    quantity = request.form['quantity']
    category = request.form['category']
    
    cur = connection.cursor()
    
    if idValue is not -1 and name == "":
        connection.execute('DELETE FROM spesa WHERE id=?', (idValue,))        
    else:        
        values = connection.execute('SELECT id,count FROM spesa WHERE name=?', (name,)).fetchall()
        if len(values) > 0:
            idValue = values[0]['id']
            count = values[0]['count']
            count += 1
            connection.execute('UPDATE spesa SET toTake=1, quantity=?, category=?, count=? WHERE id=?', (quantity, category, count, idValue))        
        else:
            connection.execute('INSERT INTO spesa (name, quantity, category, count, toTake) VALUES (?,?,?,0,1)', (name, quantity, category))
    
    connection.commit()    

    connection.close()
    return redirect('/spesa')

@app.route('/<int:idx>/update', methods=('POST',))
def update(idx):
    connection = connect()
    connection.execute('UPDATE spesa SET quantity=?, category=? WHERE id=?', (request.form['quantity'], request.form['category'], idx))
    connection.commit()    

    connection.close()
    return redirect('/spesa')

@app.route('/update', methods=('POST',))
def update2():
    #print(request.form['id'])
    #print(request.form['quantity'])
    #print(request.form['category'])
    connection = connect()
    connection.execute('UPDATE spesa SET quantity=?, category=? WHERE id=?', (request.form['quantity'], request.form['category'], request.form['id']))
    connection.commit()    

    connection.close()
    return redirect('/spesa')
    
@app.route('/<int:idx>/take', methods=('POST',))
def take(idx):
    connection = connect()
    
    connection.execute('UPDATE spesa SET toTake=0 WHERE id=?', (idx,))
    connection.commit()

    connection.close()
    return redirect('/spesa')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, threaded=True)

