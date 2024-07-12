from django.shortcuts import render, redirect
from .models import*
from django.forms import inlineformset_factory
from .forms import *
from .filters import*
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *

# Create your views here.

@unauthenticated_user
def registerPage(request):
    #if request.user.is_authenticated:
     #   return redirect('home')
    #else:
        
        #form = UserCreationForm()
    form = CreateUserForm()
        
    if request.method == 'POST':
        #form = UserCreationForm()
        form = CreateUserForm(request.POST)
        if form.is_valid():
            #user = form.save()
            form.save()
            username = form.cleaned_data.get('username')
            
            # group = Group.objects.get(name='customer')
            #user.groups.add(group)
            
            #Customer.objects.create(
             #   user=user  #user1 for model user2 for formm.save
            #)
            
            messages.success(request, 'Account was created for ' + username)
                
            return redirect('login')
    context = {'form':form}
    return render(request, 'register.html', context)        
    

@unauthenticated_user
def loginPage(request):
    #if request.user.is_authenticated:
        #return redirect('home')
    #else:
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
            
        user = authenticate(request, username=username, password=password)
            
        if user is not None:
            login(request, user)
            return redirect('home')
            
        else:
            messages.info(request, 'Username OR Password is incorrect')    
            
    
    context = {}
    return render(request, 'login.html', context)        


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'account_settings.html', context)

@login_required(login_url='login')
def update_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form':form,
        'customer':customer,
            }
    return render(request, 'update_customer.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    
    total_customers = customers.count()
    
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {
        'orders':orders, 'customers':customers,
        'total_orders':total_orders, 'delivered':delivered,
        'pending':pending
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
@admin_only
def create_customer(request):
    form = CreateUserForm()
        
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            
            form.save()
            username = form.cleaned_data.get('username')
            
            messages.success(request, 'Account was created for ' + username)
                
            return redirect('/')
    context = {'form':form}
    return render(request, 'create_customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    context = {'orders':orders,
            'total_orders':total_orders,
            'delivered':delivered,
            'pending':pending}
    return render(request, 'user.html', context)


@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()
    
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    
    context = {
        'customer':customer, 'orders':orders,
        'order_count':order_count,
        'myFilter':myFilter,
    }
    return render(request, 'customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    #form = OrderForm(initial={'customer':customer})
    #form = OrderForm()
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
        
    
    context = {'formset':formset}
    return render(request, 'order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form':form}
    return render(request, 'order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    
    context = {'item':order}
    return render(request, 'delete.html', context)





