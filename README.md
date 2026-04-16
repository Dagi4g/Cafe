# Campus Cafe

A Django web application for QR code-based ordering in a campus cafe.

---
# what it does :

an online ordering system with menu to specific cafe ,table and chair.

this system replaces the hustle of waiting inline to order , asking for bank account and waiting until the card number is called by the waiters.

## Getting Started
### 1, fork the repository 
for linux and unix based systems .
```bash
# Clone the repository
git clone https://github.com/<your_username>/Cafe.git

cd Cafe

# create a vertual environment and activate it
python -m venv cafe_venv
source cafe_venv/bin/activate

# Install dependencies
pip install -r requirements.txt

```
## create an environmental variable 

```
# generate a secrete key using Django 

python -c "from django.core.management.utils import get_random_secret_key;print(get_random_secret_key())"

```
##### copy the output and save it to new file called > .env 

```
# Run migrations and start the server
python manage.py migrate
python manage.py runserver


```

### With gunicorn


```
gunicorn -bind 0.0.0.0:8000 cafe.wsgi:application

```
> Don't forget to make allowed hosts to the ip adress of the device(server) or "\*"in development.

### How it works?
1. open home page.
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

