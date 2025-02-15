from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Notification, Wallet
from .models import FundingDetails


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["username"] = user.username
        token["first_name"] = user.first_name
        token["phone_number"] = user.phone_number
        token["transaction_pin"] = user.transaction_pin
        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "username",
            "password",
            "confirm_password",
            "phone_number",
            "transaction_pin",
        ]

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        if not data["transaction_pin"].isdigit() or len(data["transaction_pin"]) != 4:
            raise serializers.ValidationError(
                "Transaction PIN must be a 4-digit number"
            )
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        validated_data["password"] = make_password(validated_data["password"])
        user = User.objects.create(**validated_data)
        return user


class TransferSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    amount = serializers.IntegerField()
    transaction_pin = serializers.CharField(max_length=4)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "user", "message", "is_read", "date_sent"]


class WalletSerializer(serializers.ModelSerializer):
    wallet_name = RegisterSerializer()

    class Meta:
        model = Wallet
        fields = ["id", "wallet_name", "balance", "last_funded"]


class FundWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ["balance"]

    def update(self, instance, validated_data):
        amount_to_add = validated_data.get("balance", 0)
        instance.balance += amount_to_add
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ["date_joined"]


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Passwords do not match")
        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.CharField()


class ReservedAccountSerializer(serializers.Serializer):
    bvn = serializers.CharField(max_length=11, required=True)


class FundingDetailsSerializer(serializers.ModelSerializer):
    bank_names = serializers.SerializerMethodField()
    account_numbers = serializers.SerializerMethodField()

    class Meta:
        model = FundingDetails
        fields = [
            "id",
            "user",
            "account_details",
            "created_at",
            "updated_at",
            "bank_names",
            "account_numbers",
        ]
        read_only_fields = ["created_at", "updated_at", "bank_names", "account_numbers"]

    def get_bank_names(self, obj):
        return obj.get_bank_names()

    def get_account_numbers(self, obj):
        return obj.get_account_numbers()
