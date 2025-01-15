# Furniture Online Store "HOME PLACE"

**Furniture Online Store "HOME PLACE"** is a comprehensive e-commerce platform that offers a wide range of furniture products, providing users with an easy and convenient shopping experience.

## Features

- **Product Catalog:** Browse a variety of furniture categories, including sofas, tables, beds, and more.
- **Search and Filter:** Quickly find items using search functionality and advanced filtering options (e.g., from expensive to cheap and vice versa, discounts).
- **User Accounts:** Register and log in to manage your orders, wishlist, and personal information.
- **Shopping Cart:** Add items to your cart and seamlessly proceed to checkout.
- **Secure Payments:** Multiple payment options, including credit cards, PayPal, and bank transfers. (not implemented yet)
- **Order Tracking:** Track your order status in real-time.
- **Customer Support:**  Support tickets for assistance. (Live chat not implemented yet) 
- **Responsive Design:** Fully optimized for desktop, tablet, and mobile devices. (not implemented yet)

## Technologies

- **Backend:** Python (Django) 
- **Database:** PostgreSQL 
- **Hosting:**  Heroku
- **Payment Integration:** Stripe / PayPal (not implemented yet)

## Installation and Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/adventurer77/my_shop_1
   cd furniture_online_store
   ```

2. **Backend Setup:**

   - Create and activate a virtual environment:

     ```bash
     python -m venv venv
     source venv/bin/activate # For Linux/MacOS
     venv\Scripts\activate  # For Windows
     ```

   - Install dependencies:

     ```bash
     pip install -r requirements.txt
     ```

   - Set up environment variables:

     Create a `.env` file in the root directory and add:

     ```
     SECRET_KEY=your_secret_key
     DATABASE_URL=your_database_url
     ```

   - Apply database migrations:

     ```bash
     python manage.py migrate
     ```

   - Run the server:

     ```bash
     python manage.py runserver
     ```

3. **Frontend Setup:**

   - Navigate to the `frontend` directory:

     ```bash
     cd frontend
     ```

   - Install dependencies:

     ```bash
     npm install
     ```

   - Start the development server:

     ```bash
     npm start
     ```


## Usage

- **Browse Products:** Explore various categories and add items to your cart.
- **Search and Filter:** Use search and filtering to find exactly what you need.
- **Place Orders:** Proceed to checkout and select your preferred payment method.
- **Track Orders:** Check the status of your orders under your account.

## Contributions

Contributions are welcome! Feel free to fork the repository, submit pull requests, or open issues for feature requests or bug fixes.


