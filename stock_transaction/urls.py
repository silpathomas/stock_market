
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from stock_transaction import views
from . import views as stock_transaction
urlpatterns = [
path('stock_user/', views.StockUserDetails.as_view()),
path('stock_user/<int:pk>/', views.StockUserDetails.as_view()),
path('buy', stock_transaction.buy, name="buy"),
path('sell', stock_transaction.sell, name="sell"),
path('portfolio_stocks', stock_transaction.portfolio_stocks, name="portfolio_stocks"),
path('user_portfolio', stock_transaction.user_portfolio, name="user_portfolio"),
]
