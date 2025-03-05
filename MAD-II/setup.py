from app import db, Role, User, user_datastore
from flask_security import   hash_password

def createUsers():
    try:
        email = 'almighty@email.com'
        pswd = '123123'
        name = 'Almighty'
        user_datastore.create_user(email = email,full_name = name, password=hash_password(pswd))
        db.session.commit()
        r1 = Role(name = 'Admin', description = 'Admin Can Perform Crud Operation On Categories')
        r2 = Role(name = 'storeManager', description = 'storeManager Can Perform Crud Operation On Products')
        db.session.add(r1)
        db.session.add(r2)
        db.session.commit()
        user = User.query.filter_by(email = email).first()
        role_i = Role.query.filter_by(name = 'Admin').first()
        user.roles.append(role_i)
        db.session.commit()
    except Exception as e:
        print(e)
createUsers()