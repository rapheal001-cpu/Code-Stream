from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import (
    User,
    Notification,
    Wallet,
    PaymentHistory,
    OrderHistory,
)


# ==========================================
# INLINE MODELS
# ==========================================

class WalletInline(admin.StackedInline):
    model = Wallet
    extra = 0
    can_delete = False
    readonly_fields = (
        'balance',
        'created_at',
        'updated_at',
    )


# ==========================================
# USER ADMIN
# ==========================================

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'avatar_preview',
        'username',
        'full_name',
        'email',
        'role',
        'is_active',
        'follower_count',
        'following_count',
        'unread_notification',
        'wallet_balance_display',
        'date_joined',
    )

    list_filter = (
        'role',
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
    )

    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )

    ordering = ('-date_joined',)

    list_per_page = 20

    readonly_fields = (
        'avatar_preview_large',
        'last_login',
        'date_joined',
        'analytics',
    )

    autocomplete_fields = ()

    inlines = [WalletInline]

    fieldsets = (

        ("Profile Information", {
            'fields': (
                'avatar',
                'avatar_preview_large',
                'first_name',
                'last_name',
                'username',
                'email',
                'description',
                'role',
            )
        }),

        ("Social Statistics", {
            'fields': (
                'followers',
                'views',
                'analytics',
            )
        }),

        ("Permissions", {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),

        ("Security", {
            'fields': (
                'password',
            )
        }),

        ("Important Dates", {
            'fields': (
                'last_login',
                'date_joined',
            )
        }),
    )

    # ==========================================
    # CUSTOM METHODS
    # ==========================================

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="50" height="50" '
                'style="border-radius:50%; object-fit:cover;" />',
                obj.avatar.url
            )
        return "No Avatar"

    avatar_preview.short_description = "Avatar"

    def avatar_preview_large(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="180" '
                'style="border-radius:12px;" />',
                obj.avatar.url
            )
        return "No Avatar"

    avatar_preview_large.short_description = "Profile Preview"

    def wallet_balance_display(self, obj):
        try:
            return f"${obj.wallet.balance}"
        except:
            return "$0.00"

    wallet_balance_display.short_description = "Wallet"

    def analytics(self, obj):

        followers = obj.follower_count
        following = obj.following_count
        unread = obj.unread_notification

        try:
            balance = obj.wallet.balance
        except:
            balance = 0

        return format_html(
            """
            <div style="
                padding:20px;
                border-radius:12px;
                background:#111827;
                color:white;
            ">
                <h2>User Analytics</h2>

                <p><strong>Followers:</strong> {}</p>

                <p><strong>Following:</strong> {}</p>

                <p><strong>Unread Notifications:</strong> {}</p>

                <p><strong>Wallet Balance:</strong> ${}</p>
            </div>
            """,
            followers,
            following,
            unread,
            balance
        )

    analytics.short_description = "Statistics"


# ==========================================
# NOTIFICATION ADMIN
# ==========================================

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'sender',
        'name',
        'is_read',
        'created_at',
    )

    list_filter = (
        'is_read',
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
        'name',
        'sender',
    )

    ordering = ('-created_at',)

    list_per_page = 25

    autocomplete_fields = ('user',)

    readonly_fields = ('created_at',)

    fieldsets = (
        ("Notification Details", {
            'fields': (
                'user',
                'sender',
                'name',
                'message',
                'is_read',
            )
        }),

        ("System Fields", {
            'fields': (
                'created_at',
            )
        }),
    )


# ==========================================
# WALLET ADMIN
# ==========================================

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'user_role',
        'balance',
        'created_at',
    )

    list_filter = (
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
    )

    ordering = ('-created_at',)

    autocomplete_fields = ('user',)

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ("Wallet Information", {
            'fields': (
                'user',
                'balance',
            )
        }),

        ("Dates", {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )

    def user_role(self, obj):
        return obj.user.role

    user_role.short_description = "Role"


# ==========================================
# PAYMENT HISTORY ADMIN
# ==========================================

@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'user_role',
        'payment_type',
        'status',
        'created_at',
    )

    list_filter = (
        'payment_type',
        'status',
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
        'message',
    )

    ordering = ('-created_at',)

    autocomplete_fields = ('user',)

    readonly_fields = ('created_at',)

    fieldsets = (
        ("Payment Information", {
            'fields': (
                'user',
                'payment_type',
                'status',
                'message',
            )
        }),

        ("System Fields", {
            'fields': (
                'created_at',
            )
        }),
    )

    def user_role(self, obj):
        return obj.user.role

    user_role.short_description = "Role"


# ==========================================
# ORDER HISTORY ADMIN
# ==========================================

@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'user_role',
        'name',
        'status',
        'created_at',
    )

    list_filter = (
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
        'name',
        'message',
    )

    ordering = ('-created_at',)

    autocomplete_fields = ('user',)

    readonly_fields = ('created_at',)

    fieldsets = (
        ("Order Information", {
            'fields': (
                'user',
                'name',
                'message',
                'status',
            )
        }),

        ("System Fields", {
            'fields': (
                'created_at',
            )
        }),
    )

    def user_role(self, obj):
        return obj.user.role

    user_role.short_description = "Role"