flask db init
flask db migrate -m "Fix relationship backref name to avoid conflicts"
flask db upgrade

python create_test_users.py

flask --app app run --debug --host=0.0.0.0