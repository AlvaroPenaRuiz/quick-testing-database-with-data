import os
import pymysql
from flask import Flask, request, jsonify

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_PORT = int(os.environ.get('DB_PORT', 3306))
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'Learning')
RESET_TOKEN = os.environ.get('RESET_TOKEN', 'changeme')
INIT_DIR = os.environ.get('INIT_DIR', '/init')


def connect(database=None):
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=database,
        charset='utf8mb4',
        autocommit=True,
    )


def run_sql_file(cursor, filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    for statement in content.split(';'):
        stmt = statement.strip()
        if stmt:
            cursor.execute(stmt)


@app.route('/')
def index():
    return jsonify({
        'service': 'DB Reset API',
        'endpoints': {
            'GET /health': 'Check database connectivity',
            'POST /reset': 'Reset DB to initial state (requires X-Reset-Token header)',
        },
        'adminer_url': 'https://test-db.alvaropenaruiz.com/adminer',
    })


@app.route('/health')
def health():
    try:
        conn = connect(database=DB_NAME)
        conn.close()
        return jsonify({'status': 'ok', 'db': 'reachable'})
    except Exception as e:
        return jsonify({'status': 'error', 'db': str(e)}), 500


@app.route('/reset', methods=['POST'])
def reset():
    token = request.headers.get('X-Reset-Token', '')
    if token != RESET_TOKEN:
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute(f'DROP DATABASE IF EXISTS `{DB_NAME}`')
        cursor.execute(
            f'CREATE DATABASE `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'
        )
        cursor.execute(f'USE `{DB_NAME}`')

        init_files = sorted(
            os.path.join(INIT_DIR, f)
            for f in os.listdir(INIT_DIR)
            if f.endswith('.sql')
        )
        for filepath in init_files:
            run_sql_file(cursor, filepath)

        cursor.close()
        conn.close()
        return jsonify({'status': 'ok', 'message': 'Database reset successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
