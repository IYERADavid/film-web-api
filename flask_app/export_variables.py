import os

basedir = os.path.abspath(os.path.dirname(__file__))
def export_envs():
    '''it export environment variable'''
    file = open(basedir + '/env.txt')
    for line in file:
        line_data = line.rstrip('\n')
        data_pieces = line_data.split('=')
        env_name = data_pieces[0]
        env_value = data_pieces[1]
        os.environ[env_name] = env_value
