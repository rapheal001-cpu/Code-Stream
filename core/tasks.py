from celery import shared_task
from accounts.models import User, Wallet

# Create Instructor Wallet
@shared_task
def create_instructor_wallet(user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return 'This user does not exist'

    Wallet.objects.create(user=user)
    return 'Instructor Wallet created successfully'
