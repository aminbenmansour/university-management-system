from notety import create_app, admin_collection

app = create_app()

app.jinja_env.filters['zip'] = zip

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
    admin = admin_collection.find_one()

    if admin is None:
        admin = {
            "username": 'admin',
            "password": 'admin'
        }
        admin_collection.insert_one(admin)

    del admin