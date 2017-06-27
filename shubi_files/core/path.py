import os

current_location = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.abspath(os.path.join(current_location, '..'))

host_name = "http://localhost:5000/"


def get(path):
    """Returns path to given file in shubi project
    Example:
    get_shubi_path("shubi_files/server/database/database.db")
    returns:
    "D:/cool_programs/shubi/shubi_files/server/database/database.db"
    """
    return os.path.abspath(os.path.join(root_path, path))


root = root_path

# path for pythonw. Change this to whatever you want.
# Even to just plain:
# pythonw = "pythonw"
# to grab your own python version!
# pythonw = os.path.normpath(os.path.join(os.path.abspath(os.path.join(root_path, '..')), 'python', 'Scripts', 'pythonw.exe'))
pythonw = 'python'
if __name__ == '__main__':
    print('Pythonw:', pythonw)
    print(get('shubi_files/server/database'))
    print(get('cleint'))

    # D:\shubi\shubi_files\client\shubi_files
