# # seed_db.py: Populate the database with 6 default code blocks
# from app import app, db, CodeBlock

# # Initialize Database inside app context
# with app.app_context():  
#     db.create_all()

#     # Insert Code Blocks
#     code_blocks = [
#         {
#             "id": 1,
#             "title": "Async/Await in JavaScript",
#             "template": "async function fetchData() { const response = await fetch('https://api.example.com'); return response.json(); }",
#             "solution": "async function fetchData() { const response = await fetch('https://api.example.com'); const data = await response.json(); return data; }"
#         },
#         {
#             "id": 2,
#             "title": "Closures and Private Variables",
#             "template": "function createCounter() { let count = 0; return function() { count++; return count; }; }",
#             "solution": "function createCounter() { let count = 0; return function() { count++; return count; }; }"
#         },
#         {
#             "id": 3,
#             "title": "Promises with Error Handling",
#             "template": "function fetchData() { return new Promise((resolve, reject) => { if (dataExists) { resolve('Data fetched'); } else { reject('Error'); } }); }",
#             "solution": "function fetchData() { return new Promise((resolve, reject) => { if (dataExists) { resolve('Data fetched'); } else { reject('Error: No data available'); } }); }"
#         },
#         {
#             "id": 4,
#             "title": "Callback Functions in JavaScript",
#             "template": "function processData(data, callback) { callback(data); }",
#             "solution": "function processData(data, callback) { if (data) { callback(null, data); } else { callback('Error: No data'); } }"
#         },
#         {
#             "id": 5,
#             "title": "Event Loop and Call Stack",
#             "template": "console.log('Start'); setTimeout(() => { console.log('Delayed Message'); }, 1000); console.log('End');",
#             "solution": "console.log('Start'); setTimeout(() => { console.log('Delayed Message'); }, 1000); console.log('End');"
#         },
#         {
#             "id": 6,
#             "title": "Array Methods - Map and Filter",
#             "template": "const numbers = [1, 2, 3, 4]; const squaredNumbers = numbers.map(num => num * num);",
#             "solution": "const numbers = [1, 2, 3, 4]; const squaredNumbers = numbers.map(num => num * num); const evenNumbers = numbers.filter(num => num % 2 === 0);"
#         }
#     ]

#     db.session.bulk_save_objects(code_blocks)
#     db.session.commit()

#     print("Database seeded successfully!")
