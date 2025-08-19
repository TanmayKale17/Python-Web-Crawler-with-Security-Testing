from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def echo():
    if request.method == "POST":
        user_input = request.form.get("query", "")
    else:
        user_input = request.args.get("query", "")

    # This page reflects the input directly
    html = f"""
    <!doctype html>
    <html>
    <body>
        <h1>Echo Page</h1>
        <form method="get">
            <input name="query" type="text">
            <input type="submit" value="Submit GET">
        </form>
        <form method="post">
            <input name="query" type="text">
            <input type="submit" value="Submit POST">
        </form>
        <hr>
        <div>
            <strong>Reflection:</strong>
            <p>{user_input}</p>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
