from openai import OpenAI
import json
import time
import os

os.environ['OPENAI_API_KEY'] = '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'

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


def create_run(assistant_id, thread, prompt):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
    )
    
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id 
    )
    
    return run

def get_response(thread):
    messages = client.beta.threads.messages.list(thread_id=thread.id, order="asc")
    return messages
def create_thread_and_run(prompt):
    thread = client.beta.threads.create()
    run = create_run(activity_grader_id, thread, prompt)
    # 이 부분은 바꿔가면서 이용해야함..!!
    return thread, run

def complete_run(run, thread):
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id, 
            run_id=run.id)
        time.sleep(1)
    
    return run

def pretty_print(messages):
    print(" # Messages ")
    for message in messages:
        print(f"{message.role}: {message.content}")
        
        
def pretty_print_second_content(data):
    second_content_value = data["content"][1]["text"]["value"]
    print(second_content_value)

def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding
