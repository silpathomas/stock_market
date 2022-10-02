 stock_market_tracking_system
  # Stock market tracking system-backend setup 
  
  Stock market tracking system where user’s can trade stocks or shares.



> system should have support for users to login/logout.

> Users should be able to add balance to their wallet.

> Users should be able to buy/sell shares (transactions need not be stored)

> Users should be able to subscribe to an endpoint that should provide live rates.

> Users should have the ability to see their portfolio

git clone https://github.com/silpathomas/stock_market.git

1.Create a virtual environment using following command

    python -m venv stock-env

2.Activate  virtual environment

   source stock-env/bin/activate

3.iInstall the requirements
   Enter into stockemarket folder
   
    cd stockmarket
    
    pip install -r requirements.txt
    
4.Change the database details in settings.py file

      DATABASES = {
          'default': {
              'ENGINE': 'django.db.backends.postgresql_psycopg2',
              'NAME':stock_market, 
              'USER': 'postgres', 
              'PASSWORD': 'postgres',
              'HOST': '127.0.0.1', 
              'PORT': '5432',
          }
      }
5.Apply Migrations

    python manage.py migrate
    
    python manage.py makemigrations
    
    python manage.py migrate
    
6.Run the project using below command

	   Python manage.py runserver
