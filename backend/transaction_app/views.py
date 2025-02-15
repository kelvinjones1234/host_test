from django.shortcuts import render
from .serializers import TransactionSerializer
from rest_framework.views import APIView
from .models import Transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class TransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.id
        transactions = Transaction.objects.filter(wallet=user).order_by('-date_create')  # Order by descending created_at
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)