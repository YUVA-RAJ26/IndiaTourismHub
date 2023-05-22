# IndiaTourismHub

IndiaTourismHub is a comprehensive tourism application built with Django, offering a seamless platform to explore and experience the enchanting destinations of India. From iconic landmarks to hidden gems, this application provides a curated collection of tourist places, tour packages, and hotels across the country.

## Features

- **Tourist Places**: Discover a rich selection of tourist places with detailed descriptions, captivating images, and essential information such as location, address, and pincode. Autocomplete features simplify the selection of state, district, and pincode.

- **Tour Packages**: Browse through an array of thoughtfully curated tour packages, encompassing multiple destinations, duration of stay, hotel accommodations, payment options, discount codes, and other necessary details.

- **User and Admin Modules**: Seamlessly navigate between user and admin modules. Users can register, login via OTP, explore tourist places, and book packages. Admins have exclusive access to manage places, packages, bookings, and hotel information.

- **Booking Management**: Users can book tour packages by filling out a comprehensive form with details such as the preferred booking date, contact number, and more. Invoice generation and email delivery streamline the booking process, while payment screenshots can be uploaded for admin approval.

- **Graphical Representations**: Admins can visualize and analyze booking data using pie and bar charts, based on state, year, or tourist package. The graphs can be downloaded as PDF files for further analysis.

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-username/IndiaTourismHub.git
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Configure the database settings in `settings.py`, ensuring the connection details for PostgreSQL are correctly set.

4. Run database migrations:

   ```
   python manage.py migrate
   ```

5. Start the development server:

   ```
   python manage.py runserver
   ```

6. Access the application by navigating to `http://localhost:8000` in your web browser.


