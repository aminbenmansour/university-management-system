print('Start #################################################################');
db = db.getSiblingDB('students-grades-management')

db.createCollection('admin');
db.createCollection('student');
db.createCollection('data');
db.createCollection('grades');
 
db.admin.insert ({
    username: "admin",
    password: "admin"
});

print('End   #################################################################');
