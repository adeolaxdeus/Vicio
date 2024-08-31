from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/sign-up', methods='GET')
def sign_in():
    # Retrieve form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Here you can add form validation and processing logic
    if not email or not password:
        # Handle missing form fields
        return render_template('index.html', error='Please fill out all fields.')
    # Process the data (e.g., save to database, authenticate user, etc.)
    # ...

    # Redirect to a success page or another route
    return redirect(url_for('success'))

@app.route('/success')
def success():
    print("Form submitted successfully!")
    # Render the form template if the request method is GET
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
