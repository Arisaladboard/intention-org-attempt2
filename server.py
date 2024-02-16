from flask import Flask, request, jsonify
from flask_cors import CORS
from process_contacts import ProcessContacts
from transcriber import transcribe
from process_notes import ProcessNotes
from process_buckets import ProcessBuckets
import os

app = Flask(__name__)
CORS(app)

class Contact: 
    def __init__(self, firstName, lastName = '', phone = 0000000000):
        self.firstName = firstName
        self.lastName = lastName
        self.phone = phone

cont1 = Contact("John", 4252738555)
cont2 = Contact("Jane", 1234567890)

contactList = [cont1, cont2]

# Contacts processor
contacts_processor = ProcessContacts()
notes_processor = ProcessNotes()
bucket_processor = ProcessBuckets()
      

@app.route("/")
def home():
    return "Hello World"

# Retrieves a list of contacts from the frontend
@app.route("/api/contacts", methods=["POST"])
def receive_data():
    try: 
        data = request.get_json()
        contacts_processor.read_contacts(data)
        # currently using hardcoded user_id 4
        contacts_processor.sync_contacts(4)
        return jsonify({'message': 'Contacts received.'}), 200
    
    except Exception as err:
        return jsonify({'message': str(err)})
    
@app.route("/api/contacts", methods=['GET'])
def send_data():
    # currently using hardcoded user_id 4
    contacts_processor.retrieve_db_contacts(4)
    return jsonify(contacts_processor.contacts), 200

# Retrieves notes to transcribe from frontend
@app.route("/api/transcribe", methods=["POST"])
def receive_note_transcribe():
    try:
        # Get audio file from request
        audio_blob = request.data 

        # check if audio file exists
        if not audio_blob:
            return jsonify({'error': 'No audio data received'}), 400

        # Save the audio blob to a file with .m4a extension
        save_folder = 'temp_audio/'
        os.makedirs(save_folder, exist_ok=True)
        file_path = os.path.join(save_folder, 'recording.m4a')
        with open(file_path, 'wb') as file:
            file.write(audio_blob)

        transcribed_audio = transcribe()

        return jsonify({'message': 'File saved successfully', 'data': transcribed_audio}), 200

    except Exception as err:
        return jsonify({'error': str(err)}), 500


# Retrieves notes to save from frontend
@app.route("/api/note", methods=["POST"])
def receive_note():
    try:
        data = request.get_json()
        notes_processor.read_note(data)
        notes_processor.save_note()

        return jsonify({'message': 'Note received.'}), 200
    except Exception as err:
        return jsonify({'error': str(err)}), 500

if __name__ == "__main__":
    # added host to test, it seems to make it work on android
    app.run(debug=True,  port=5100)

@app.route("/api/Bucket", methods=["POST"])
def recieve_Buckets():
    try:
        data = request.get_json()
        bucket_processor.read_buckets(data)
        bucket_processor.sync_buckets()
        return jsonify({'message': 'Buckets received.'}), 200
    except Exception as err:
        return jsonify({'message': str(err)})

@app.route("/api/Bucket", methods=['GET'])
def send_data():
    # currently using hardcoded user_id 4
    bucket_processor.retrieve_db_buckets(4)
    return jsonify(bucket_processor.buckets), 200