from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

#create a helper function to find an event by ID
#we are going to use this function in the update and delete routes to find the event by its ID
def find_event(event_id):
    for event in events:
        if event.id == event_id:
            return event
    return None

#Welcome route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Event Management API!"}), 200

#get all events
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200

# TODO: Task 1 - Define the Problem
# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    if "title" not in data or not data["title"]:
        return jsonify({"error": "Title is required"}), 400

    new_id = max(event.id for event in events) + 1 if events else 1
    new_event = Event(new_id, data["title"])
    events.append(new_event)
    return jsonify(new_event.to_dict()), 201




# TODO: Task 1 - Define the Problem
# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    if "title" not in data or not data["title"]:
        return jsonify({"error": "Title is required"}), 400

    event.title = data["title"]
    return jsonify(event.to_dict()), 200

# TODO: Task 1 - Define the Problem
# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)
    return jsonify({"message": "Event deleted successfully"}), 204

if __name__ == "__main__":
    app.run(debug=True)
