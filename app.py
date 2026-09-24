from flask import Flask, jsonify, request, render_template, redirect, url_for
from intake_logic import validate_intake
from database import initialize_database, save_intake, get_all_intakes, get_intake_by_id
from ai_summary import generate_ai_summary

app = Flask(__name__)

initialize_database()


@app.route("/", methods=["GET"])
def home():
    return render_template("intake.html")


@app.route("/intake", methods=["POST"])
def create_intake():
    intake_data = request.form.to_dict()

    if not intake_data:
        return jsonify({
            "error": "No intake information was provided."
        }), 400

    intake_analysis = validate_intake(intake_data)

    ai_summary = generate_ai_summary(
        intake_data,
        intake_analysis
    )

    intake_id = save_intake(
        intake_data,
        intake_analysis,
        ai_summary
    )

    return redirect(url_for("intake_review", intake_id=intake_id))


@app.route("/dashboard", methods=["GET"])
def dashboard():
    intakes = get_all_intakes()

    return render_template(
        "dashboard.html",
        intakes=intakes
    )


@app.route("/intake/<int:intake_id>", methods=["GET"])
def intake_review(intake_id):
    intake = get_intake_by_id(intake_id)

    if intake is None:
        return "Intake not found.", 404

    return render_template(
        "intake_review.html",
        intake=intake
    )


if __name__ == "__main__":
    app.run(debug=True)