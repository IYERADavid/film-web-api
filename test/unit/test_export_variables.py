import os
from flask_app.export_variables import basedir

def test_export_envs():
    file = open(basedir + '/env.txt')
    for line in file:
        line_data = line.rstrip('\n')
        data_pieces = line_data.split('=')
        env_name = data_pieces[0]
        env_value = data_pieces[1]
        assert os.environ.get(env_name) == env_value
