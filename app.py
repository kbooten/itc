from flask import Flask, render_template, request, jsonify
from flask_httpauth import HTTPBasicAuth
import json
import time

import threading ## for rewriting 

from llm_interface import get_llm_response
from update_text_with_llm import maybe_update_field_yaml, maybe_update_field_prose, maybe_update_user_yaml
from google_sheets_io import append_data_to_google_sheet, write_field_to_google_sheets

from make_main_prompt import build_prompt

app = Flask(__name__)
auth = HTTPBasicAuth()


from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import datetime

# Users for basic auth
users = {
    "itc": "platsplatsplats",  # remember to remove this
} 


@auth.verify_password
def verify_password(meta_username, password):
    if meta_username in users and users[meta_username] == password:
        return meta_username
    return None


def process_history(history):
    hist_string = ""
    for h in history:
        print(h)  # Log h to inspect its structure
        if isinstance(h, dict):  # Ensure h is a dictionary
            if 'user' in h and 'text' in h:  # Ensure required keys are present
                if h['user'] == "You":
                    hist_string += "User: %s\n" % h["text"]
                else:
                    hist_string += "AI: %s\n" % h["text"]
            else:
                print("Warning: Missing 'user' or 'text' key in history item:", h)
        else:
            print("Warning: Unexpected item in history:", h)
    return hist_string


def process_input(user_text, user_id, user_email, user_yaml, history):
    """
    get main llm response
    threadedly start other changes to field, map, etc.
    return main llm response
    """
    llm_response = get_llm_response(build_prompt(user_text, user_yaml, history))
    user_yaml = maybe_update_user_yaml(user_text, llm_response, user_yaml) ## just update each time
    thread = threading.Thread(target=process_input_slow_stuff, args=(user_text, user_id, user_email, llm_response, history))
    thread.start()
    return {"response":llm_response,"user_yaml":user_yaml}


def process_input_slow_stuff(user_text, user_id, user_email, llm_response, history):
    """
    to be threaded so costly io and llm responses that won't be immediately returned 
    won't block return of response
        - update field (both prose description and yaml)
        - send response to google sheets
    """
    maybe_update_field_yaml(user_text,llm_response,history)
    maybe_update_field_prose(user_text,llm_response)
    data_to_append = [[int(time.time()), user_id, user_text, llm_response]]
    append_data_to_google_sheet(data_to_append)


@app.route('/')
@auth.login_required
def home():
    return render_template('chat.html')


@app.route("/send_message", methods=["POST"])
def send_message():
    user_input = request.form.get("message")
    user_id = request.form.get("user_id")
    user_email = request.form.get("user_email")
    user_yaml = request.form.get("user_yaml")
    history = process_history(json.loads(request.form.get("history")))
    #last_n_turns = request.form.get("last_n_turns")
    if user_input.strip():
        response = process_input(user_input, user_id, user_email, user_yaml, history)
        return jsonify({"user": "Same, KA", "text": response['response'], "user_yaml":response['user_yaml']})
    return jsonify({"error": "No message received"})


def scheduled_task():
    write_field_to_google_sheets()
    print(f"Scheduled task (writing rooms to sheets) executed at {datetime.datetime.now()}")


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=scheduled_task, trigger="interval", minutes=20)
    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    app.run(debug=True,use_reloader=False)