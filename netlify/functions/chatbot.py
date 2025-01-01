import json
import os
from dotenv import load_dotenv
from together import Together

def handler(event, context):
    load_dotenv()
    api_key = os.getenv("TOGETHER_API_KEY")
    client = Together(api_key=api_key)

    user_query = json.loads(event['body']).get('query', "Tell me about my resume.")
    resume_context = """
    Abhay's Resume:
    Introduction: I am a full stack developer and done data structures and algorithms course.
    Full Name: Abhay Raj Gautam
    Location: Small village called Bajidpur, located in district Rampur of Uttar Pradesh

    Courses:
    - Data Structure and Algorithms
    - Information and Database Systems
    - Data Science
    - Mathematical Foundation of Computer Science
    - Computer Organization
    - Formal Language and Automata Theory
    - Statistical Foundations of Data Science

    College:
    - Indian Institute of Technology, Mandi

    School:
    - Milton Educational Academy

    Skills:
    - C++, JavaScript, React, Node.js, Python, MongoDB, BootStrap

    Projects:
    - The Blog Application:
    - A web application that allow users to manage their writing content specifically blogs digitally and efficiently.
    - Implemented password hashing, user authentication, and secure user data handling.
    - Technologies: HTML, CSS, JavaScript, EJS, NodeJS, MongoDB, Bootstrap

    - The Bookish Worm Application:
    - A react web Application for books to write the book notes or summary of the book.
    - Technologies: HTML, CSS, JavaScript, React, MongoDB

    Certifications:
    - No certifications yet
    """
    
    messages = [
        {"role": "system", "content": "You are a chatbot trained to answer questions about resumes."},
        {"role": "assistant", "content": resume_context},
        {"role": "user", "content": user_query}
    ]

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=messages,
        max_tokens=200,
        temperature=0.7,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1.0,
        stop=["<|eot_id|>", "<|eom_id|>"],
    )

    result = "".join(token['choices'][0]['delta']['content'] for token in response if 'choices' in token)
    return {
        'statusCode': 200,
        'body': json.dumps({'response': result})
    }
