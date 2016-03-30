- install django-guardian with "pip install django-guardian"
- create new clean database 'lucky78_master' with user 'lucky78' and password 'lucky78'
- run manage.py migrate
- import test data manage.py loaddata fundaccounts_testdata.json
- register new user and login
- open '/admin/' in anouther browser and login with admin:admin (will be created automatically on migration)

Now you can transfer from admin account to user:
- open 'Investors' Model in admin
- choose user by checking checkbox
- enter amountGBP or amountAUD or both
- choose "Transfer" action from dropdown
- press Go
- you can see transfer transactions in 'Transactions' model in admin

Making investments:
- login with user
- choose 'Funds' un menu
- enter Share for fund and press "Subscribe" button to invest
- press "Unsubscribe" button to unsubscribe