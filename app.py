

from flask import Flask, request, render_template, redirect, url_for, flash
from scripts.get_token import get_token_env
from scripts.connect_to_server import RemoteSQLExecutor


app = Flask(__name__)
app.secret_key = get_token_env("FLASK_SECRET_KEY")
remote_sql_executor = RemoteSQLExecutor()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form['search_query']
        
        # Ищем пользователя по user_id или username
        sql_query = f"SELECT * FROM user_usage WHERE user_id = '{search_query}' OR username = '{search_query}';"
        result = remote_sql_executor.execute(sql_query)
        
        if result:
            user_data = result.strip().split('|')
            user = {
                'id': user_data[0],
                'user_id': user_data[1],
                'username': user_data[2],
                'is_admin': user_data[3],
                'is_premium': user_data[4],
                'is_blocked': user_data[5],
                'usage_count': user_data[6],
                'created_at': user_data[7]
            }
            return redirect(url_for('edit_user', user_id=user['user_id']))
        else:
            flash("User not found", "error")
            return render_template('index.html'), 404
    
    return render_template('index.html')


@app.route('/block/<int:user_id>', methods=['POST'])
def block_user(user_id):
    # Блокируем пользователя
    sql_update = f"UPDATE user_usage SET is_blocked = 1 WHERE user_id = {user_id};"
    remote_sql_executor.execute(sql_update)
    return redirect(url_for('index'))


@app.route('/unblock/<int:user_id>', methods=['POST'])
def unblock_user(user_id):
    # Разблокируем пользователя
    sql_update = f"UPDATE user_usage SET is_blocked = 0 WHERE user_id = {user_id};"
    remote_sql_executor.execute(sql_update)
    return redirect(url_for('index'))


@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'POST':
        new_usage_count = request.form['usage_count']
        
        # Обновляем usage_count
        sql_update = f"UPDATE user_usage SET usage_count = {new_usage_count} WHERE user_id = {user_id};"
        remote_sql_executor.execute(sql_update)
        return redirect(url_for('index'))
    
    # Получаем данные пользователя
    sql_query = f"SELECT * FROM user_usage WHERE user_id = {user_id};"
    result = remote_sql_executor.execute(sql_query)
    
    if result:
        user_data = result.strip().split('|')
        user = {
            'id': user_data[0],
            'user_id': user_data[1],
            'username': user_data[2],
            'is_admin': user_data[3],
            'is_premium': user_data[4],
            'is_blocked': user_data[5],
            'usage_count': user_data[6],
            'created_at': user_data[7]
        }
        return render_template('edit_user.html', user=user)
    else:
        return "User not found", 404


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)