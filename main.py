from app import app, db
from app.models import User, Post, Inventory, LastUpdate, DataHistory

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Inventory': Inventory, 'LastUpdate': LastUpdate, 'DataHistory': DataHistory}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)