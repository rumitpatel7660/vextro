from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'vextro_secret_key'

# Sample product data (add more as needed)
PRODUCTS = [
    {
        'name': 'Stainless Steel Door Handle',
        'image': 'static/assets/product/IMG_1751.jpg',
        'desc': 'Premium quality stainless steel handle for doors.',
        'category': 'Hardware'
    },
    {
        'name': 'Modern Faucet',
        'image': 'static/assets/product/IMG_1857.jpg',
        'desc': 'Elegant faucet for modern bathrooms and kitchens.',
        'category': 'Sanitary Fittings'
    },
    {
        'name': 'Brass Angle Valve',
        'image': 'static/assets/product/IMG_1862.jpg',
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
        message = request.form.get('message', '')
        # Basic validation
        if not name or not email or not message:
            flash('All fields are required.', 'error')
        else:
            print(f"Contact Form Submission: {name}, {email}, {message}")
            flash('Thank you for contacting us! We will get back to you soon.', 'success')
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
                'category': category.replace('_', ' ').title()
            } for file in os.listdir(category_path) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]
            return render_template('products.html', products=products_list, category=category.replace('_', ' ').title(), categories=categories)
    
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
                    'category': cat.replace('_', ' ').title()
                })
    return render_template('products.html', products=all_products, categories=categories)

if __name__ == '__main__':
    app.run(debug=True) 