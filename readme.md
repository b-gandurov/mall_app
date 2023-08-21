# 🛍 Mall App

The **Mall App** is a Django-based application designed to provide functionalities related to a shopping mall. It has features like Cinema, Parking, Stores, User profile

## 🌟 Features

- 🎬 **Cinema**: The cinema module enables users to browse and view the latest movies being shown in the mall. It provides intercative scheduling information and also allows for ticket bookings and keep updated with the latest showtimes. Only signed up users have the option to book seats to their profile.

  ![My Image](demo_cinema.gif)

- 🚗 **Parking**: Manage your vehicle with the parking module. It allows users to check parking availability, signed up users have the option to regster cars so that each time when they open the app they can see how long a given car has been parked and what is the total parking cost for each car.
- 🏬 **Stores**: Explore various stores available in the mall. Stores can be searched based on category, name or both. The stores module provides detailed information on all the stores, along with working hours,location in the mall, website,phone and others. All of these details can be customized from the backend. The store owners have the option to veature items on their store page that are avaiable for reservation for specific ammout of time. Only registered users will have the option to reserve items.
- 🔐 **User Authentication System**: Provides registration, login, and password reset functionalities. Authenticated users have additonal functionalities enabled to them for each part of the app.
- 🧑 **User Profiles**: Store and manage personal information including first name, last name, date of birth, and phone number. Additionaly users can manage their Cinema tickets bookings, store items reservations or add/remove cars to their parking profile along with checking addtional parking fees and parked time in more details.

## 🛠 Prerequisites

- **Python**: 3.8+
- **Django**: 4.2+
- **PostgreSQL**: (If you opt for this database)
- **Other dependencies**: As mentioned in your `requirements.txt` (assuming you have one)

## 🚀 Installation

1. **Clone the Repository**

   ```bash
   git clone git@github.com:b-gandurov/mall_app.git
      cd mall_app/
   ```

2. **Set up a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

   For IOS use:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Environment Variables Setup**
   Create a `.env` file in the root directory and add the following:

   ```bash
   SECRET_KEY=your-secret-key
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=your-db-name
   DB_USER=your-db-user
   DB_PASSWORD=your-db-password
   DB_HOST=your-db-host
   DB_PORT=your-db-port
   EMAIL_HOST_USER=your-email
   EMAIL_HOST_PASSWORD=your-email-password
   ```

6. **Run Migrations**

   ```bash
   python manage.py migrate
   ```

7. **Start the Development Server**

   ```bash
   python manage.py runserver
   ```

## ⚙ Configuration

- The project defaults to Django's SQLite database during development. However, it can easily transition to PostgreSQL or other supported databases.
- For email functions, the system is integrated with Gmail's SMTP server. You will need to Follow [this guide](https://support.google.com/accounts/answer/185833?hl=en) on how to to generate App Passwords if you are goin to use this setup.

## 📜 License

[MIT](https://choosealicense.com/licenses/mit/)
