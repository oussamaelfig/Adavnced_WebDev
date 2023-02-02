from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        # getting input with name = fname in HTML form
        first_name = request.form.get("fname")
        # getting input with name = lname in HTML form
        last_name = request.form.get("lname")
        # getting radio button
        color = request.form['customRadio']
        fo = open("DataForm", "w")
        fo.write("Your name is " + first_name + " " + last_name + " \n the color you choose is " + color)
       """ return "Your name is " + first_name + " " + last_name + " \n the color you choose is " + color"""
    return render_template('homeForm.html')


if __name__ == '__main__':
    app.run()
