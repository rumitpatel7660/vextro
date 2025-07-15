from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from twilio.rest import Client
from size_charts import size_charts

# Twilio credentials (store these as environment variables ideally)
TWILIO_ACCOUNT_SID = 'ACe42e4054899219412b630d59302cdbd0'
TWILIO_AUTH_TOKEN = '1cf916651ebadaaa1c3de94f916ff744'
TWILIO_PHONE_NUMBER = '+14782416504'  # Your Twilio number
ADMIN_PHONE_NUMBER = '+919978431347'  # Admin's phone number (E.164 format)

app = Flask(__name__)
app.secret_key = 'vextro_secret_key'

# Sample product data (add more as needed)
PRODUCTS = [
    {
        'name': 'Stainless Steel Door Handle',
        'image': 'static/assets/product/aldrops/Jorjan Aldrop.jpg',
        'desc': 'Premium quality stainless steel handle for doors.',
        'category': 'Hardware'
    },
    {
        'name': 'Modern Faucet',
        'image': 'static/assets/product/hinges/Brass Railway Hinges.jpg',
        'desc': 'Elegant faucet for modern bathrooms and kitchens.',
        'category': 'Sanitary Fittings'
    },
    {
        'name': 'Brass Angle Valve',
        'image': 'static/assets/product/towerbolt/Xylo Towerbolt.jpg',
        'desc': 'Durable brass angle valve for plumbing solutions.',
        'category': 'Sanitary Fittings'
    }
]
@app.route('/')
def index():
    return render_template('index.html', products=PRODUCTS[:3])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        contact_number = request.form.get('contact_number', '')
        message = request.form.get('message', '')

        # SMS Validation
        try:
            # Compose the SMS content
            # sms_body = f"New Contact Submission:\nName: {name}\nEmail: {email}\nPhone: {contact_number}\nMessage: {message}"
            print("Initializing Twilio client...")
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            print("Creating SMS message...")
            client.messages.create(
                body="Test SMS from Flask app - contact form trigger",
                from_=TWILIO_PHONE_NUMBER,
                to=ADMIN_PHONE_NUMBER
            )
            print(f"Message sent! SID: {message.sid}")
        except Exception as e:
            print(f"Failed to send SMS to admin: {e}")
            flash('Error sending SMS notification.', 'error')

        # Basic validation
        if not name or not email or not contact_number or not message:
            flash('All fields are required.', 'error')
        else:
            print(f"Contact Form Submission: {name}, {email}, {contact_number}, {message}")
            return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/products')
@app.route('/products/<category>')
def products(category=None):
    product_path = os.path.join(app.static_folder, 'assets', 'product')
    if category:
        categories = [d for d in os.listdir(product_path) if os.path.isdir(os.path.join(product_path, d))]
        if category in categories:
            category_path = os.path.join(product_path, category)
            products_list = [{
                'name': file,
                'image': url_for('static', filename=f'assets/product/{category}/{file}'),
                'category': category.replace('_', ' ').title(),
                'size_chart_key': file  # Use filename as key
            } for file in os.listdir(category_path) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
            return render_template('products.html', products=products_list, category=category.replace('_', ' ').title(), categories=categories, size_charts=size_charts)
    
    # If no category or invalid category, show all products
    all_products = []
    categories = [d for d in os.listdir(product_path) if os.path.isdir(os.path.join(product_path, d))]
    for cat in categories:
        category_path = os.path.join(product_path, cat)
        for file in os.listdir(category_path):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                all_products.append({
                    'name': file,
                    'image': url_for('static', filename=f'assets/product/{cat}/{file}'),
                    'category': cat.replace('_', ' ').title(),
                    'size_chart_key': file  # Use filename as key
                })
    return render_template('products.html', products=all_products, categories=categories, size_charts=size_charts)

@app.route('/api/send_sms', methods=['POST'])
def send_sms():
    data = request.get_json()
    name = data.get('name', '')
    email = data.get('email', '')
    contact_number = data.get('contact_number', '')
    message = data.get('message', '')
    
    sms_body = f"New Contact Submission:\nName: {name}\nEmail: {email}\nPhone: {contact_number}\nMessage: {message}"
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        sms = client.messages.create(
            body=sms_body,
            from_=TWILIO_PHONE_NUMBER,
            to=ADMIN_PHONE_NUMBER
        )
        return jsonify({'success': True, 'sid': sms.sid}), 200
    except Exception as e:
        print(f"Failed to send SMS to admin: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/catalog_download', methods=['POST'])
def catalog_download():
    data = request.get_json()
    name = data.get('name', '')
    phone = data.get('phone', '')
    sms_body = f"Catalog Download Request:\nName: {name}\nPhone: {phone}"
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        sms = client.messages.create(
            body=sms_body,
            from_=TWILIO_PHONE_NUMBER,
            to=ADMIN_PHONE_NUMBER
        )
        return jsonify({'success': True, 'sid': sms.sid}), 200
    except Exception as e:
        print(f"Failed to send SMS for catalog download: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 