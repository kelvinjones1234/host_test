# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Wallet, Notification, FundingDetails
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class WalletInline(admin.StackedInline):
    model = Wallet
    can_delete = False
    verbose_name_plural = "wallet"


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "username",
        "email",
        "phone_number",
        "is_active",
        "is_premium",
        "transaction_pin",
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "transaction_pin",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_premium",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "phone_number",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    inlines = (WalletInline,)
    search_fields = ("username", "email", "phone_number")
    ordering = ("username",)


class WalletAdmin(admin.ModelAdmin):
    model = Wallet
    list_display = ("wallet_name", "balance", "last_funded")
    readonly_fields = ("reference", "wallet_name")


class NotificationAdmin(admin.ModelAdmin):
    model = Notification
    list_display = ("user", "date_sent", "is_read")
    list_editable = ("is_read",)


class FundingDetailsAdmin(admin.ModelAdmin):
    readonly_fields = ("formatted_account_details", "user")

    def get_fields(self, request, obj=None):
        """
        Customize the fields displayed in the detail view
        """
        return [
            "user",
            "formatted_account_details",
        ]

    def formatted_account_details(self, obj):
        """
        Create a detailed, formatted view of account details
        """
        if not obj.account_details:
            return "No account details available"

        html_output = "<div style='max-width:100%; overflow-x:auto;'>"
        html_output += "<table style='width:100%; border-collapse: collapse;'>"
        html_output += """
        <thead>
            <tr style='background-color:#f2f2f2;'>
                <th style='border:1px solid #ddd; padding:12px; text-align:left;'>Bank Name</th>
                <th style='border:1px solid #ddd; padding:12px; text-align:left;'>Account Number</th>
                <th style='border:1px solid #ddd; padding:12px; text-align:left;'>Bank Code</th>
                <th style='border:1px solid #ddd; padding:12px; text-align:left;'>Account Name</th>
            </tr>
        </thead>
        <tbody>
        """

        for account in obj.account_details:
            html_output += f"""
            <tr>
                <td style='border:1px solid #ddd; padding:12px;'>{account.get('bankName', 'N/A')}</td>
                <td style='border:1px solid #ddd; padding:12px;'>{account.get('accountNumber', 'N/A')}</td>
                <td style='border:1px solid #ddd; padding:12px;'>{account.get('bankCode', 'N/A')}</td>
                <td style='border:1px solid #ddd; padding:12px;'>{account.get('accountName', 'N/A')}</td>
            </tr>
            """

        html_output += "</tbody></table></div>"
        return mark_safe(html_output)

    formatted_account_details.short_description = "Account Details"

    # Customize list display
    list_display = ("user", "brief_account_details", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("user__username", "user__email")

    def brief_account_details(self, obj):
        """
        Create a brief summary for list view
        """
        if not obj.account_details:
            return "No accounts"

        account_summary = [
            f"{account.get('bankName', 'N/A')} - {account.get('accountNumber', 'N/A')}"
            for account in obj.account_details
        ]
        return ", ".join(account_summary)

    brief_account_details.short_description = "Account Details"


admin.site.register(FundingDetails, FundingDetailsAdmin)

admin.site.register(Notification, NotificationAdmin)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Wallet, WalletAdmin)
