from datetime import timezone
from django.http import HttpResponse
from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib.auth.hashers import  check_password
from base.models.customer import Customer
from django.views import View
from base.models.useractivity import UserActivity


class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get ('return_url')
        return render (request, 'login2.html')

    def post(self, request):
        email = request.POST.get ('email')
        password = request.POST.get ('password')
    
        customer = Customer.get_customer_by_email (email)
        error_message = None
        if customer:
            flag = check_password (password, customer.password)
            if flag:
                #log the user in
                request.session['customer'] = customer.id
                request.session['customer_email'] = customer.email

                logged_in_customer = Customer.objects.get(id=customer.id)
                
                if Login.return_url:
                    return HttpResponseRedirect (Login.return_url)
                else:
                    Login.return_url = None
                    return redirect ('base:home')
            else:
                error_message = 'Invalid !!'
        else:
            error_message = 'Invalid !!'

        print (email, password)
        return render (request, 'login2.html', {'error': error_message})

def logout(request):
    if 'customer_id' in request.session:
        del request.session['customer_id']
    if 'customer_email' in request.session:
        del request.session['customer_email']

    return redirect('base:login2')