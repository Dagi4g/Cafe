# Campus Cafe

A Django web application for QR code-based ordering in a campus cafe.

---

## Project Progress

### ✅ Completed
- **Django project setup:** The project uses Django and is organized as a standard Django app (`cafe/` and `order/` directories).
- **Basic order management:** Initial code for handling core order functions is present (in the `order/` directory).
- **Menu viewing:** Students can view the menu after scanning a table QR code.
- **Order placement:** Students can order food via the web interface.
- **Payment system:** Both digital and cash payment options laid out, with payment functionality being worked on in code.
- **Real-time availability:** Menu updates are suggested; relevant code can be enhanced for real-world use.
- **Getting Started instructions** provided in the README.

### 🚧 In Progress / Partially Done
- **Order delivery to table:** Basic logic exists; can be enhanced for seat-specific delivery tracking.
- **Payment integration:** Cash and digital payment “modes” exist; integration with real payment providers can be expanded.
- **Project structure:** Contains `requirements.txt`, `manage.py`, and Django directory layout.


---

## Getting Started
### 1, fork the repository 

```bash
# Clone the repository
git clone https://github.com/<your username>/Cafe.git
cd Cafe

# Install dependencies
pip install -r requirements.txt

# Run migrations and start the server
python manage.py migrate
python manage.py runserver


```

### How to use it?
1. got to the home page.
2. Scan your table’s QR code with the builtin scanner.
3. Browse menu, order.
4. Pay with a pay button in the receipt page.
5. The Waiter delivers food to your table.
6. The Waiter scans his qrcode badge with the users phone for confirmation .


---

## TODO

- [ ] QR code generation and mapping for each table
- [ ] Authentication for staff and students
- [ ] Order status page and notifications for students
- [ ] Enhanced payment integration (e.g.,telebirr)
- [ ] Order history and receipts for users
- [ ] Mobile design improvements
- [ ] Tests (unit/integration)
- [ ] Production-ready deployment instructions


---

