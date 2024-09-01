from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('signup.html')
    # Retrieve form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Here you can add form validation and processing logic
    if not email or not password:
        # Handle missing form fields
        return render_template('signup.html', error='Please fill out all fields.')

    # For demonstration purposes, we'll just print the form data and redirect
    print(f'Email: {email}, Password: {password}')

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
