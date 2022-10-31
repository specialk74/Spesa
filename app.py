from flask import Flask, render_template, redirect, request, json
import os
import sqlite3
import pathlib
import click
from argparse import ArgumentParser

app = Flask(__name__)
parser = ArgumentParser()
parser.add_argument('--port')
parser.add_argument('--path')
args = parser.parse_args()

def connect():
    connection = sqlite3.connect(args.path + '/database.db')
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/spesa')
def index():
    connection = connect()

    #for item in products:
    #    print (item['name'])
    #    print (item['count'])
    spesa = connection.execute('SELECT * FROM spesa ORDER BY category').fetchall()
    num_take = connection.execute('SELECT COUNT(*) FROM spesa WHERE toTake=1').fetchone()[0]
        
    connection.close()

    return render_template('index.html', spesa=spesa, num_take=num_take)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    connection = connect()
    cur = connection.cursor()
    
    search = request.args.get('q')
    #query = db_session.query(Movie.title).filter(Movie.title.like('%' + str(search) + '%'))
    
    cur.execute('SELECT name FROM spesa WHERE toTake=0 and name LIKE ? ORDER BY count', ('%'+search+'%',))
    data = dict(result=[dict(r) for r in cur.fetchall()])
    #print(data)
    return json.jsonify(matching_results=data)

@app.route('/<int:idx>/add' , methods=('POST',))
def add(idx):
    connection = connect()

    data = request.get_json()
    #print(idx)
    #print(data)
    #print(data['data']['category'])
    #print(data.data.name)
    #print(data.data.quantity)
    
    name = data['data']['name']
    if len(name) == 0:
        connection.execute('DELETE FROM spesa WHERE id=?', (idx,))
        connection.commit()

        connection.close()
        
        return redirect('/spesa')
        
    quantity = data['data']['quantity']
    new_category = data['data']['category']

    values = connection.execute('SELECT count, category FROM spesa WHERE id=?', (idx,)).fetchall()
    count = values[0]['count']
    category = values[0]['category']
    count += 1
    connection.execute('UPDATE spesa SET toTake=1, name=?, quantity=?, category=?, count=? WHERE id=?', (name, quantity, new_category, count, idx,))
    connection.commit()

    if int(new_category) != int(category):
        connection.close()
        return redirect('/spesa')
    num_take = connection.execute('SELECT COUNT(*) FROM spesa WHERE toTake=1').fetchone()[0]
    
    connection.close()

    #return jsonify(data=data)
    return json.jsonify({"num_take": num_take})
    
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
    data = request.get_json()
    
    quantity = data['data']['quantity']
    new_category = data['data']['category']

    values = connection.execute('SELECT category FROM spesa WHERE id=?', (idx,)).fetchall()
    category = values[0]['category']

    connection.execute('UPDATE spesa SET quantity=?, category=? WHERE id=?', (quantity, new_category, idx))
    connection.commit()    

    connection.close()

    print(new_category)
    print(category)
    if int(new_category) != int(category):
        print("update redirect")
        return redirect('/spesa')
        
    return json.jsonify({})

@app.route('/update', methods=('POST',))
def update2():
    #print(request.form['id'])
    #print(request.form['quantity'])
    #print(request.form['category'])
    connection = connect()
    connection.execute('UPDATE spesa SET quantity=?, category=? WHERE id=?', (request.form['quantity'], request.form['category'], request.form['id']))
    connection.commit()    

    connection.close()
    #return redirect('/spesa')
    return jsonify({})
    
@app.route('/<int:idx>/take', methods=('POST',))
def take(idx):
    connection = connect()
    
    connection.execute('UPDATE spesa SET toTake=0 WHERE id=?', (idx,))
    connection.commit()

    #return redirect('/spesa')
    num_take = connection.execute('SELECT COUNT(*) FROM spesa WHERE toTake=1').fetchone()[0]
    connection.close()

    return json.jsonify({"num_take": num_take})

if __name__ == '__main__':
    print(args)
    #port = int(os.getenv("PORT", 9080))
    print("Port: " + args.port)
    print("Path: " + args.path)
    app.run(host='0.0.0.0', port=args.port, threaded=True)

