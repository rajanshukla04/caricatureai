from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import UserProfile
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import UserProfile
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

def home(request):
    """Renders the home page with check-in options"""
    return render(request, 'user_management/home.html')



def qr_checkin(request):
    error = None    
    if request.method == 'POST':
        qrcode = request.POST.get('qrcode', '').strip()
        
        try:
            user_profile = UserProfile.objects.get(qrcode=qrcode)
            # Redirect to success page with user ID
            return redirect('success_page', user_id=user_profile.id)
        except UserProfile.DoesNotExist:
            error = "Data not found - Please check the QR code and try again"
    return render(request, 'user_management/withqrcode.html', {'error': error})


from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import UserProfile

def success_page(request, user_id):
    # Get the user profile regardless of request method
    user_profile = get_object_or_404(UserProfile, id=user_id)
    
    if request.method == 'POST':
        # Handle the print time update
        user_profile.print_time = timezone.now()
        user_profile.save()
        #return redirect('camera_view/')  # Redirect back to scanner
        return redirect(reverse('camera_view'))
    # GET request - show user details
    return render(request, 'user_management/success.html', {'profile': user_profile})


from django.db.models import Q





from django.shortcuts import render
from django.db.models import Q
from .models import UserProfile

def manual_checkin(request):
    results = None
    error = None
    
    if request.method == 'POST':
        search_term = request.POST.get('search_term', '').strip()
        
        if search_term:
            # Search across multiple fields using OR conditions
            query = Q(name__icontains=search_term) | \
                    Q(email__icontains=search_term) | \
                    Q(mobile__icontains=search_term) | \
                    Q(regno__icontains=search_term)
            
            results = UserProfile.objects.filter(query)
            
            if not results.exists():
                error = "No matching records found for your search"
        else:
            error = "Please enter a search term"

    return render(request, 'user_management/withoutqrcode.html', {
        'results': results,
        'error': error
    })