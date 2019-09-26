nohup python3 -u user/test/test.py params1 > nohup.out 2>&1 &
python3 manage.py makemigrations app
python3 manage.py migrate
