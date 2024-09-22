from django.shortcuts import render, redirect
from django.contrib import messages
import gspread
from google.oauth2.service_account import Credentials
from django.conf import settings
import os
from .utils import fetch_student_data
from django.http import JsonResponse

# Google Sheets setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = os.path.join(settings.STATICFILES_DIRS[0], 'credentials.json')

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

SHEET_ID = '1XDLMKIxssigi58ch7mxahauzqODo3ot4NuDXrgqCnww'  # Replace with your actual Sheet ID
WORKSHEET_NAME = 'details'

sheet = client.open_by_key(SHEET_ID).worksheet(WORKSHEET_NAME)

def get_sheet_data():
  return sheet.get_all_values()
    
def check_login(ad_no, password):
    rows = get_sheet_data()
    header = rows[0] 
    for row in rows[1:]: 
        if len(row) > 4 and row[2] == ad_no and row[4] == password:  # Ensure row has sufficient columns
            return row 
    return None

# Create your views here.
def get_user_details(ad_no):
    rows = get_sheet_data()
    for row in rows:
        if len(row) > 4 and row[2] == ad_no:
            return {
                'no': row[0],       
                'name': row[1],    
                'ad_no': row[2],   
                'balance': row[3],  
                'password': row[4] 
            }
    return {}

def index(request):
    if 'ad_no' in request.session:
        ad_no = request.session['ad_no']
        user_details = get_user_details(ad_no)
        return render(request, 'index.html', {'user_details': user_details, 'page': 'index'})
    else:
        return redirect('login')

def students(request):
    if 'ad_no' in request.session:
        students_data = fetch_student_data()
        ad_no = request.session['ad_no']
        user_details = get_user_details(ad_no)
        return render(request, 'students.html', {'user_details': user_details, 'page': 'students',  'students': students_data})
    else:
        return redirect('login')

def notifications(request):
    if 'ad_no' in request.session:
        ad_no = request.session['ad_no']
        user_details = get_user_details(ad_no)
        return render(request, 'notifications.html', {'user_details': user_details, 'page': 'notifications'})
    else:
        return redirect('login')

def services(request):
    if 'ad_no' in request.session:
        ad_no = request.session['ad_no']
        user_details = get_user_details(ad_no)
        return render(request, 'services.html', {'user_details': user_details, 'page': 'services'})
    else:
        return redirect('login')

def account(request):
    if 'ad_no' in request.session:
        ad_no = request.session['ad_no']
        user_details = get_user_details(ad_no)  # Assuming this function fetches user details
        return render(request, 'account.html', {'user_details': user_details, 'page': 'account'})
    else:
        return redirect('login')

def click_account(request):
    if 'ad_no' in request.session:
        ad_no = request.session['ad_no']
        user_details = get_user_details(ad_no)
        return render(request, 'account.html', {'user_details': user_details,})
    else:
        return redirect('login')

def login(request):
    page = "login"
    if request.method == "POST":
        ad_no = request.POST.get('adno')
        password = request.POST.get('password')

        if check_login(ad_no, password):
            request.session['ad_no'] = ad_no
            user_details = get_user_details(ad_no)
            return render(request, 'index.html', {'ad_no': ad_no, 'page': 'index', 'user_details': user_details})
        else:
            messages.error(request, 'Invalid Ad No or Password')

    return render(request, 'login.html', {'page': page})

def logout(request):
    if 'ad_no' in request.session:
        del request.session['ad_no']  # Remove user from session
        messages.info(request, 'You have been logged out successfully.')
    return redirect('login')

def find_student(request):
    ad_no = request.GET.get('adNo')
    students = fetch_student_data()

    print(students)

    student = next((s for s in students if str(s.get('Ad_No', '')).strip() == ad_no), None)

    if student:
        return JsonResponse({'name': student.get('Name', 'Unknown')})
    else:
        return JsonResponse({'error': 'Student not found'}, status=404)
    
def find_student(request):
    ad_no = request.GET.get('adNo')
    students = fetch_student_data()

    
    print("students good")

    student = next((student for student in students if str(student['Ad_No']) == ad_no), None)

    if student:
        return JsonResponse({'name': student['Name']})
    else:
        return JsonResponse({'error': 'Student not found'}, status=404)

def add_transaction(request):
    if request.method == 'POST':
        transaction_type = request.POST.get('type')
        adno = request.POST.get('adNo')
        ad_no = int(adno)
        name = request.POST.get('name')
        amount1 = request.POST.get('amount')
        amount = float(amount1)
        transactionid = request.POST.get('transactionId')
        transaction_id = int(transactionid)
        date = transaction_id/86400000+25569
        desc = request.POST.get('desc')


        # Select the appropriate Google Sheets worksheet based on transaction type
        if transaction_type == 'credit':
            sheet = client.open_by_key('1XDLMKIxssigi58ch7mxahauzqODo3ot4NuDXrgqCnww').worksheet('Credit')
        else:
            sheet = client.open_by_key('1XDLMKIxssigi58ch7mxahauzqODo3ot4NuDXrgqCnww').worksheet('Debit')

        if ad_no and name and amount:
            new_row = [transaction_id, name, ad_no, amount, desc, date]
            sheet.append_row(new_row)

            return redirect('add')
        
    return render(request, 'add_transaction.html')

def add(request):
    redirect('account')
    return JsonResponse({'status': 'success'})
