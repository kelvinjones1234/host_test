from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from user_app.models import User
from user_app.models import Wallet


def reformat_phone_number(phone_number):
    # Remove the country code (+234) and return the local number
    if phone_number.startswith('+234'):
        return '0' + phone_number[4:]  # Replace +234 with 0
    return phone_number

@csrf_exempt
def ussd_callback(request):
    if request.method == 'POST':
        session_id = request.POST.get('sessionId')
        service_code = request.POST.get('serviceCode')
        phone_number = reformat_phone_number(request.POST.get('phoneNumber'))
        print(phone_number)
        text = request.POST.get('text', 'default')

        # Check if the phone number exists in the database
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return HttpResponse("END This phone number is not registered. Please sign up for an account.", content_type='text/plain')

        if text == '':
            response = "CON Welcome to MaduConnect!\n"
            response += "1. Buy Data\n"
            response += "2. Buy Airtime\n"
            response += "3. My Credit Balance\n"
            response += "4. My phone number"
        elif text == '1':
            response = "CON Choose a data plan\n"
            response += "1. 500mb for 180\n"
            response += "2. 1gb for 369"
        elif text == '2':
            response = "CON Select Network\n"
            response += "1. MTN\n"
            response += "2. Airtel\n"
            response += "3. Glo\n"
            response += "4. 9mobile"
        elif text.startswith('2*'):
            parts = text.split('*')
            if len(parts) == 2:
                network_choice = parts[1]
                networks = {
                    '1': 'MTN',
                    '2': 'Airtel',
                    '3': 'Glo',
                    '4': '9mobile'
                }
                if network_choice in networks:
                    response = f"CON Enter amount for {networks[network_choice]} airtime:"
                else:
                    response = "END Invalid network selection. Please try again."
            elif len(parts) == 3:
                network_choice = parts[1]
                amount = parts[2]
                networks = {
                    '1': 'MTN',
                    '2': 'Airtel',
                    '3': 'Glo',
                    '4': '9mobile'
                }
                if network_choice in networks and amount.isdigit():
                    response = f"END You're about to buy {networks[network_choice]} airtime worth {amount} naira. Please confirm on the next prompt."
                else:
                    response = "END Invalid input. Please try again."
        elif text == '3':
            try:
                balance = user.wallet.balance
                response = f"END Your balance is {balance}"
            except Wallet.DoesNotExist:
                response = "END Your wallet has not been set up yet."
        elif text == '4':
            response = f"END Your phone number is {phone_number}"
        else:
            response = "END Invalid input. Try again."

        return HttpResponse(response, content_type='text/plain')
    return HttpResponse("Method not allowed", status=405)



