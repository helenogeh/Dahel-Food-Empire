from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/order", methods=["GET", "POST"])
def order():

    if request.method == "POST":

        product = request.form["product"]
        quantity = request.form["quantity"]
        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]

        print("New Order")
        print("Product:", product)
        print("Quantity:", quantity)
        print("Name:", name)
        print("Phone:", phone)
        print("Address:", address)

        return render_template("success.html")

    return render_template("order.html")


@app.route("/training", methods=["GET", "POST"])
def training():

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        training = request.form["training"]
        training_type = request.form["training_type"]
        experience = request.form["experience"]
        location = request.form["location"]
        start_date = request.form["start_date"]
        goal = request.form["goal"]

        print("New Training Registration")
        print("Name:", name)
        print("Phone:", phone)
        print("Email:", email)
        print("Training:", training)
        print("Training Type:", training_type)
        print("Experience:", experience)
        print("Location:", location)
        print("Start Date:", start_date)
        print("Goal:", goal)

        return render_template("training_success.html")

    return render_template("training.html")


if __name__ == "__main__":
    app.run(debug=True)
    