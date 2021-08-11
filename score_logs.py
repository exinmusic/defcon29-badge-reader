from flask import Flask, render_template
import sqlite3
import json

app = Flask(__name__)

@app.route('/')
def scores_view():
	con = sqlite3.connect('badge-data.db3')
	cur = con.cursor()
	all_rows = [json.loads(row[1]) for row in cur.execute('SELECT * FROM badges')]
	pill_count = 0
	signal_count = 0
	alien_count = 0
	for row in all_rows:
		if row['ctf']['redpill']:
			pill_count +=1
		if row['ctf']['newsignal']:
			signal_count +=1
		if row['ctf']['aliens']:
			alien_count +=1
	row_count = len(all_rows)
	return render_template('index.html', scores=all_rows, row_count=row_count, pill_count=pill_count, signal_count=signal_count, alien_count=alien_count)