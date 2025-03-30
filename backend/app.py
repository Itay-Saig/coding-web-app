from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS

# Initialize Flask application
app = Flask(__name__)
CORS(app)

# Initialize SocketIO with CORS enabled for all origins
socketio = SocketIO(app, cors_allowed_origins="*")

# Store code blocks
code_blocks = [
    {
        "id": 1,
        "title": "Async/Await in JavaScript",
        "template": "async function fetchData() { const response = await fetch('https://api.example.com'); return response.json(); }",
        "solution": "async function fetchData() { const response = await fetch('https://api.example.com'); const data = await response.json(); return data; }"
    },
    {
        "id": 2,
        "title": "Closures and Private Variables",
        "template": "function createCounter() { let count = 0; return function() { count++; return count; }; }",
        "solution": "function createCounter() { let count = 0; return function() { count++; return count; }; }"
    },
    {
        "id": 3,
        "title": "Promises with Error Handling",
        "template": "function fetchData() { return new Promise((resolve, reject) => { if (dataExists) { resolve('Data fetched'); } else { reject('Error'); } }); }",
        "solution": "function fetchData() { return new Promise((resolve, reject) => { if (dataExists) { resolve('Data fetched'); } else { reject('Error: No data available'); } }); }"
    },
    {
        "id": 4,
        "title": "Callback Functions in JavaScript",
        "template": "function processData(data, callback) { callback(data); }",
        "solution": "function processData(data, callback) { if (data) { callback(null, data); } else { callback('Error: No data'); } }"
    },
    {
        "id": 5,
        "title": "Event Loop and Call Stack",
        "template": "console.log('Start'); setTimeout(() => { console.log('Delayed Message'); }, 1000); console.log('End');",
        "solution": "console.log('Start'); setTimeout(() => { console.log('Delayed Message'); }, 1000); console.log('End');"
    },
    {
        "id": 6,
        "title": "Array Methods - Map and Filter",
        "template": "const numbers = [1, 2, 3, 4]; const squaredNumbers = numbers.map(num => num * num);",
        "solution": "const numbers = [1, 2, 3, 4]; const squaredNumbers = numbers.map(num => num * num); const evenNumbers = numbers.filter(num => num % 2 === 0);"
    }
]

# Track users in rooms based on code block ID
users_in_room = {}
global_mentor = None  # Store the first session ID that connects as the mentor

# Route to fetch all available code blocks
@app.route("/codeblocks")
def get_codeblocks():
    """
    Return a list of all available code blocks (ID, title, template, and solution).
    """
    return jsonify(code_blocks)

def check_solution(block_id, student_code):
    """
    Compare the student's code to the correct solution for a given code block ID.
    
    Parameters:
    -----------
        block_id (int): The ID of the code block being solved.
        student_code (str): The code submitted by the student.
    
    Returns:
    --------
        bool: True if the student's code matches the solution, False otherwise.
    """
    solution = next((block['solution'] for block in code_blocks if block['id'] == block_id), None)
    if solution and student_code.strip() == solution.strip():
        return True
    return False

# Route for the home page
@app.route('/')
def home():
    """
    Home page route that simply returns a welcome message.
    """
    return "Welcome to the CodeBlock App!"

# Event handler for a user joining a code block
@socketio.on("join_codeblock")
def handle_join_codeblock(data):
    """
    Handle a user joining a specific code block.
    
    Parameters:
    -----------
        data (dict): Contains the code block ID.
    """

    global global_mentor
    block_id = data.get("id")
    username = request.sid  # Unique session ID for the user
    room = f"codeblock_{block_id}"

    # The first session connects as the mentor
    if global_mentor is None:
        global_mentor = username

    if block_id not in users_in_room:
        users_in_room[block_id] = {"mentor": None, "students": set()}

    # If this is the mentor's session, assign mentor role
    if username == global_mentor:
        users_in_room[block_id]["mentor"] = username
        join_room(room)
        print(f"👨‍🏫 Mentor joined room {room}: {username}")
        emit("role_assigned", {"role": "mentor", "message": "You are a Mentor"}, room=username)
        emit("student_count_update", {"count": 0}, room=room)  # Mentor doesn't count as a student
        return

    # Otherwise, assign student role
    if username not in users_in_room[block_id]["students"]:
        users_in_room[block_id]["students"].add(username)
        print(f"👨‍🎓 Student joined room {room}: {username}")

    join_room(room)

    student_count = len(users_in_room[block_id]["students"])
    print(f"📊 Updated student count in {room}: {student_count}")
    emit("role_assigned", {"role": "student", "message": "You are a Student"}, room=username)
    emit("student_count_update", {"count": student_count}, room=room)

# Event handler for updating code block content
@socketio.on("update_codeblock")
def handle_update_codeblock(data):
    """
    Handle updates to the code block submitted by students.
    
    Parameters:
    -----------
        data (dict): Contains the code block ID and the student's code.
    """
    block_id = data.get("id")
    student_code = data.get("template")
    username = request.sid  # Unique session ID for the student

    # Check if the student's code matches the solution
    if check_solution(block_id, student_code):
        print(f"😊 Student {username} has solved the code block {block_id}")
        emit("show_smiley", room=username)  # Notify student they solved the block
    else:
        print(f"❌ Student {username}'s code doesn't match the solution for {block_id}")

# Event handler for a user leaving a code block
@socketio.on("leave_codeblock")
def handle_leave_codeblock(data):
    """
    Handle a user leaving a code block.
    
    Parameters:
    -----------
        data (dict): Contains the code block ID.
    """
    block_id = data.get("id")
    username = request.sid
    room = f"codeblock_{block_id}"

    # Remove user from room and update student count
    if block_id in users_in_room:
        if username == users_in_room[block_id]["mentor"]:
            print(f"❌ Mentor left room {room}: {username}")
            users_in_room[block_id]["mentor"] = None
            users_in_room[block_id]["students"].clear()
            emit("redirect_to_home", broadcast=True, room=room)  # Redirect everyone to the lobby page
        else:
            users_in_room[block_id]["students"].discard(username)
            print(f"👋 Student left room {room}: {username}")

        student_count = len(users_in_room[block_id]["students"])
        emit("student_count_update", {"count": student_count}, room=room)

    leave_room(room)

# Event handler for a user disconnecting
@socketio.on("disconnect")
def handle_disconnect():
    """
    Handles the disconnection of a user from the server.
    """
    global global_mentor
    for block_id, room_data in users_in_room.items():
        if request.sid == room_data["mentor"]:
            print(f"❌ Mentor disconnected from room {block_id}")
            room_data["mentor"] = None
            room_data["students"].clear()
            emit("redirect_to_home", broadcast=True, room=f"codeblock_{block_id}")

        else:
            room_data["students"].discard(request.sid)
            print(f"👋 Student disconnected from room {block_id}")

        student_count = len(room_data["students"])
        emit("student_count_update", {"count": student_count}, room=f"codeblock_{block_id}")

    # Reset global mentor if the mentor disconnects
    if request.sid == global_mentor:
        print("🛑 Mentor session ended. Resetting global mentor.")
        global_mentor = None


# Run the app using SocketIO
if __name__ == "__main__":
    socketio.run(app, debug=True)
