from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import StockUser,StockPortfolio
from .serializers import StockUserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
import yfinance as yf
import json
from django.contrib.auth.decorators import login_required

#Create or update the StockUserDetails instance.
class StockUserDetails(APIView):
  
    def put(self, request, pk, format=None):
        Stock_user = StockUser.objects.get(pk=pk)
        serializer = StockUserSerializer(Stock_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request,pk,format=None):
        Stock_user = StockUser.objects.get(pk=pk)
        serializer = StockUserSerializer(Stock_user)
        return Response(serializer.data)

    #update the account balance
    def post(self, request, format=None):
        serializer = StockUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Buy stock and update StockUser StockPortfolio table
@login_required
@api_view(['GET', 'POST'])
@csrf_exempt
def buy(request):

    stock_symbol=request.POST.get('stock_symbol', '').strip()
    user_id = request.user.id  
    num_shares=request.POST.get('num_shares', '').strip()
    cost_per_share=request.POST.get('cost_per_share', '').strip()
    print(user_id)
    try:
        stock_user = StockUser.objects.get(user=user_id)
        stock_user.spent += float(cost_per_share) * int(num_shares)
        stock_user.account_balance -= float(cost_per_share) * int(num_shares)
        stock_user.save()
        result = StockPortfolio.objects.get_or_create(stock=stock_symbol, user=stock_user)[0]
        result.shares += int(num_shares)
        data=result.save()
        return Response("Transaction completed Successfully", status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error":"user wallet do not exit"}, status=status.HTTP_400_BAD_REQUEST)



#Buy stock and update StockUser StockPortfolio table.
@api_view(['GET', 'POST'])
@login_required
@csrf_exempt
def sell(request):
    stock_symbol=request.POST.get('stock_symbol', '').strip()
    user_id = request.user
    num_shares=request.POST.get('num_shares', '').strip()
    cost_per_share=request.POST.get('cost_per_share', '').strip()
    try:
        stock_user = StockUser.objects.get(user=user_id)
        result = StockPortfolio.objects.filter(stock=stock_symbol, user=stock_user)
        result.shares -= int(num_shares)
        if result.shares < 0:
          result.shares = 0  
        stock_user.earnt += float(cost_per_share) * int(num_shares)
        stock_user.account_balance += float(cost_per_share) * int(num_shares)
        stock_user.save()
        if result.shares == 0:
          result.delete()
        else:
          result.save()
        return Response("Transaction completed Successfully", status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error":"No share Availabe."}, status=status.HTTP_400_BAD_REQUEST)

#Returns the list live rate form Yahoo Finance
@csrf_exempt
@login_required
@api_view(['GET', 'POST'])
def portfolio_stocks(request):
    portfolio_info = []
    tickers=request.POST.get('tickers', '').strip()
    data=yf.download(tickers)
    return Response(data, status=status.HTTP_201_CREATED)

#Returns the user's earn,spend,stock,share and account details
@csrf_exempt
@login_required
@api_view(['GET', 'POST'])
def user_portfolio(request):
    data=StockPortfolio.objects.filter(user=request.user.id)[0]
    portfolio=[]
    print(request.user.id)
    # stoke_data=[]
    account_info={}
    # account_info=[]
    account_info={"account_info":{'user_name':data.user.user.username,'account_balance':data.user.account_balance}}
    data=StockPortfolio.objects.filter(user=request.user.id)
    for i in data:
        print(data)
        portfolio.append({'earnt':i.user.earnt,
        'spent':i.user.spent,
        'stock':i.stock,
        'shares':i.shares
        })
    portfolio.append(account_info)
    # portfolio.append({"stoke_info":stoke_data})
    return Response(portfolio, status=status.HTTP_201_CREATED)