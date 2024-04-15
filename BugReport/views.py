from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from openpyxl.styles import NamedStyle
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font
from .models import Bug
from .forms import ReportForm


# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/bug_list')  # Redirect to 'bug_list' URL name upon successful login
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'BugReport/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")  # Optional: Display a logout message
    return redirect('/login')  # Redirect to the login page after logout


@login_required
def report_bug(request):
    if request.method == 'POST':
        project = request.POST.get('project')
        sdm = request.POST.get('SDM')
        issue_reported = request.POST.get('issue_reported')
        resolved_by = request.POST.get('resolved_by')  # Assuming you have a form field for this

        # Assign the created_by field to the current logged-in user
        new_bug = Bug.objects.create(
            project=project,
            SDM=sdm,
            issue_reported=issue_reported,
            resolved_by=resolved_by,
            created_by=request.user  # Set the created_by field to the current user
        )

        return redirect('/bug_list')
    else:
        form = ReportForm()
    return render(request, 'BugReport/index.html', {'form': form})


@login_required
def bug_list(request):

    bugs_ordered_by_created_at = Bug.objects.order_by('-created_at')

    context = {
        'bugs': bugs_ordered_by_created_at,
    }
    return render(request, 'BugReport/bug_list.html', context=context)
    # all_bugs = Bug.objects.all()
    # return render(request, 'BugReport/bug_list.html', {'all_bugs': all_bugs})


@login_required
def download_bug_list_excel(request):
    # Retrieve Bug objects
    bugs = Bug.objects.all()

    # Create a new Excel workbook
    wb = Workbook()
    ws = wb.active

    # Set custom number format to display date only (e.g., "yyyy-mm-dd")
    date_style = NamedStyle(name='date_style', number_format='DD-MM-YYYY')  # YYYY-MM-DD

    # Add headers to the Excel file
    ws.append(['Project', 'SDM', 'Issue Reported', 'Resolved By', 'Created At'])

    # Iterate over each Bug object and add data to Excel
    for bug in bugs:
        # Convert created_at datetime to local timezone
        local_created_at = timezone.localtime(bug.created_at)
        # Add row data to Excel worksheet, formatting date using custom style
        ws.append([bug.project, bug.SDM, bug.issue_reported, bug.resolved_by, local_created_at.date()])
    
    # Apply custom number format to the "Created At" column (column E, assuming it's the 5th column)
    for cell in ws['E']:
        cell.style = date_style

    # Format the current date and time for the filename
    current_datetime = timezone.now().strftime("%Y%m%d_%H%M%S")
    # Set filename for the Excel file (including date and time)
    filename = f"BugList_{current_datetime}.xlsx"

    # Save the workbook to a response as a file attachment
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Save the workbook content to the HttpResponse
    wb.save(response)

    return response


