from flask import Flask, render_template,request,jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI

app=Flask(__name__)

load_dotenv()
apikey=os.getenv("OPENAI_API")

client=OpenAI(api_key=apikey)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    question= request.form.get("question")
    response=client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": "act like a personal assistant"},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_output_tokens=512

    )
        
    answer=response.output[0].content[0].text.strip()
        
    return jsonify({"response": answer}),200
    
@app.route("/summarize", methods=["POST"])
def sumarize():
    email_text=request.form.get("email")
    prompt=f"summrize the following email in 2-3 sentences:{email_text}"
    response=client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": "act like a expert email assistant"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_output_tokens=512
    )
    summary=response.output[0].content[0].text.strip()
    return jsonify({"response": summary})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
