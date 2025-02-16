from rest_framework.exceptions import PermissionDenied
from django.core.mail import send_mail
import random
import string
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import hashlib
from .serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    NotificationSerializer,
    WalletSerializer,
    TransferSerializer,
    UserSerializer,
    FundWalletSerializer,
    PasswordResetSerializer,
    PasswordResetRequestSerializer,
    ReservedAccountSerializer,
)


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from django.db.models import F
from django.db import transaction

from rest_framework import status, generics
from rest_framework.response import Response
from .models import Notification, Wallet, User, FundingDetails
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .utils import MonnifyAPIClient
from .models import FundingDetails
from .serializers import FundingDetailsSerializer

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator


from dotenv import load_dotenv
import os

# Load environme
load_dotenv()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            sender = request.user

            if not sender.is_authenticated:
                raise PermissionDenied("User is not authenticated")

            recipient_username = serializer.validated_data["username"]
            amount = serializer.validated_data["amount"]
            transaction_pin = serializer.validated_data["transaction_pin"]

            if not transaction_pin == sender.transaction_pin:
                return Response(
                    {"error": "Invalid transaction pin"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                recipient = User.objects.get(username=recipient_username)
            except User.DoesNotExist:
                return Response(
                    {"error": "Recipient does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if sender.wallet.balance < amount:
                return Response(
                    {"error": "Insufficient balance"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            sender.wallet.balance -= amount
            recipient.wallet.balance += amount
            sender.wallet.save()
            recipient.wallet.save()

            Notification.objects.create(
                user=recipient,
                message=f"You have received {amount} credits from {sender.username}",
            )
            Notification.objects.create(
                user=sender,
                message=f"You have sent {amount} credits to {recipient.username}",
            )

            return Response(
                {
                    "success": "Transfer completed",
                    "balance": sender.wallet.balance,  # Include the updated balance
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by(
            "-date_sent"
        )


class NotificationDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class WalletDetailView(generics.RetrieveUpdateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "wallet_name__username"

    # class FundWalletView(generics.RetrieveUpdateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = FundWalletSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        username = self.kwargs.get("wallet_name__username")
        return get_object_or_404(Wallet, wallet_name__username=username)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class PasswordResetRequestView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = (
                    f"https://atom-blush.vercel.app/user/reset-password/{uid}/{token}/"
                )

                # Send the reset link via email
                subject = "Password Reset Request"
                message = f"Click the link below to reset your password:\n{reset_link}"
                from_email = "praisejournal2@gmail.com"
                recipient_list = [email]

                send_mail(subject, message, from_email, recipient_list)

                return Response(
                    {"message": "Password reset link has been sent to your email"},
                    status=status.HTTP_200_OK,
                )
            except User.DoesNotExist:
                return Response(
                    {"error": "User with this email does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    def post(self, request, uidb64, token, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            uid = force_str(urlsafe_base64_decode(uidb64))
            try:
                user = User.objects.get(pk=uid)
                if default_token_generator.check_token(user, token):
                    user.set_password(serializer.validated_data["password"])
                    user.save()
                    return Response(
                        {"message": "Password has been reset successfully"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
                    )
            except User.DoesNotExist:
                return Response(
                    {"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MonnifyReservedAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def generate_account_reference(self, username):
        """
        Generate an 8-digit unique reference number based on the username.

        Args:
            username (str): The username of the logged-in user

        Returns:
            str: An 8-digit random reference number
        """
        # Use the first 4 characters of a hash of the username to ensure some uniqueness
        username_hash = hashlib.md5(username.encode()).hexdigest()[:4]

        # Generate 4 random digits
        random_digits = "".join(random.choices(string.digits, k=4))

        return username_hash + random_digits

    def post(self, request):
        try:
            # Get the current logged-in user's data
            user_data = request.user

            # Prepare serializer data
            serializer_data = {
                "bvn": request.data.get("bvn")  # Assuming BVN is passed in request data
            }

            # Create serializer with request data
            serializer = ReservedAccountSerializer(data=serializer_data)

            if serializer.is_valid():
                # Extract only the BVN from the serializer
                bvn = int(serializer.validated_data["bvn"])

                # Generate unique account reference
                account_reference = (
                    f"maduconnect_{self.generate_account_reference(user_data.username)}"
                )
                # print(user_data.username)

                # Prepare account details using user's information
                account_details = {
                    "accountName": user_data.username,
                    "accountReference": account_reference,
                    "currencyCode": "NGN",
                    "contractCode": "6525688895",
                    "customerEmail": user_data.email,
                    "customerName": f"{user_data.first_name} {user_data.last_name}",
                    "bvn": bvn,
                    "getAllAvailableBanks": True,
                }
                wallet = Wallet.objects.get(wallet_name__username=user_data.username)
                wallet.reference = account_reference
                wallet.save()
                # Initialize Monnify client
                monnify_client = MonnifyAPIClient()

                # Create reserved account
                response_data = monnify_client.create_reserved_account(account_details)

                # Save funding details if account creation is successful
                if response_data.get("requestSuccessful", False):
                    accounts = response_data.get("responseBody", {}).get("accounts", [])

                    # Create or update FundingDetails with all accounts
                    FundingDetails.objects.update_or_create(
                        user=user_data, defaults={"account_details": accounts}
                    )

                return Response(response_data)

            # If serializer is not valid, return validation errors
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class FundingDetailsAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, username):
        """Retrieve funding details for the specified user"""
        user = get_object_or_404(
            User, username=username
        )  # Fetch the user by username or return 404
        funding_details = FundingDetails.objects.filter(
            user=user
        )  # Filter by user instance
        serializer = FundingDetailsSerializer(funding_details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Replace this with your actual Monnify client secret key
MONNIFY_CLIENT_SECRET = os.getenv("MONIFY_SECRETE_KEY")


@method_decorator(csrf_exempt, name="dispatch")
class MonnifyWebhookView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract the payload and the Monnify signature from the headers
        payload = request.body.decode("utf-8")
        monnify_signature = request.headers.get("monnify-signature")

        # Verify the hash to ensure the payload is from Monnify
        if not self.verify_signature(payload, monnify_signature):
            return Response(
                {"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Parse the payload
        try:
            payload_data = json.loads(payload)
        except json.JSONDecodeError:
            return Response(
                {"error": "Invalid JSON payload"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Extract transaction details
        event_type = payload_data.get("eventType")
        event_data = payload_data.get("eventData")

        if event_type == "SUCCESSFUL_TRANSACTION":
            account_reference = event_data.get("accountReference")
            amount_paid = event_data.get("amountPaid")

            # Update the user's wallet
            try:
                wallet = Wallet.objects.get(account_reference=account_reference)
                wallet.balance(amount_paid)
                return Response(status=status.HTTP_200_OK)
            except Wallet.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def verify_signature(self, payload, monnify_signature):
        """
        Verify the Monnify signature by computing the SHA-512 hash of the payload
        using the client secret key and comparing it with the provided signature.
        """
        # Compute the hash
        computed_hash = hashlib.sha512(
            (MONNIFY_CLIENT_SECRET + payload).encode("utf-8")
        ).hexdigest()

        # Compare the computed hash with the provided signature
        return computed_hash == monnify_signature
