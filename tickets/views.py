from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .forms import SignUpForm, CustomAuthenticationForm
from io import BytesIO
from .models import * 
import stripe
import qrcode
import base64

# Create your views here.

def homepage(request):
    return render(request, 'tickets/homepage.html')


def tickets_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'tickets/tickets_list.html', {'tickets': tickets})


def add_to_cart(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    cart_id = request.session.get('cart_id')

    if cart_id:
        try:
            cart = Cart.objects.get(id=cart_id)
        except Cart.DoesNotExist:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    else:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id

    cart_item, created = CartItem.objects.get_or_create(cart=cart, ticket=ticket)
    cart_item.quantity += 1
    cart_item.save()
    request.session['cart_id'] = cart.id

    messages.success(request, f'{ticket.name} a été ajouté à votre panier!')

    return redirect('tickets_list')


def clear_cart(request):
    request.session['cart_id'] = {}
    return redirect('cart_detail')


def cart_detail(request):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    else:
        cart = get_object_or_404(Cart, id=cart_id)

    cart_items = CartItem.objects.filter(cart=cart)

    total_price = sum(item.ticket.price * item.quantity for item in cart_items)

    return render(request, 'tickets/cart_detail.html', {
        'cart_items': cart_items,
        'total_price' : total_price
    })

def success_view(request):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    else:
        cart = get_object_or_404(Cart, id=cart_id)

    cart_items = CartItem.objects.filter(cart=cart)

    for item in cart_items:
        for _ in range(item.quantity):
            Purchase.objects.create(
                user=request.user, 
                ticket=item.ticket, 
                quantity=1,
                payment_status='paid',
                unique_id=uuid.uuid4().hex[:10]
            )
    request.session['cart_id'] = {}

    return render(request, 'tickets/success.html')


def cancelled_view(request):
    return render(request, 'tickets/cancelled.html')


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
    
@csrf_exempt
def create_checkout_session(request):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id
    else:
        cart = get_object_or_404(Cart, id=cart_id)

    cart_items = CartItem.objects.filter(cart=cart)
    total_price = int(str(sum(item.ticket.price * item.quantity for item in cart_items)).replace('.', ''))

    cart_description = "Détail de votre commande : "
    for item in cart_items:
        cart_description += f"{item.ticket.name} (x{item.quantity}), "

    cart_description = cart_description.strip(", ")

    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                # A compléter pour récupérer l'ID de l'utilisateur qui a acheté le Ticket
                # client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'unit_amount': total_price,
                        'product_data': {
                            'name': 'Tickets',
                            'description': cart_description,
                            'images': ['https://img.freepik.com/photos-gratuite/vieux-talon-billet-dechire-marron-utilise-isole_1101-3193.jpg?size=626&ext=jpg&ga=GA1.1.1788614524.1719014400&semt=ais_user'],
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
            )


            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
        
@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                messages.error(request, "Invalid username or password.")

    else:
        form = CustomAuthenticationForm()
    
    return render(request, "registration/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('homepage')


@login_required
def user_dashboard(request):
    user_purchases = Purchase.objects.filter(user=request.user)
    tickets = Ticket.objects.all()
    is_superuser = request.user.is_superuser
    sales_stats = Purchase.objects.values('ticket__name').annotate(total_sold=Sum('quantity')).order_by('ticket__name')
    logs = AdminLog.objects.all().order_by('-action_date')

    context = {
        'user_purchases': user_purchases,
        'tickets': tickets,
        'is_superuser': is_superuser,
        'sales_stats': sales_stats,
        'logs': logs,
    }
    return render(request, 'registration/user_dashboard.html', context)


def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    return img


def view_qr_code(request, purchase_id):
    purchase = get_object_or_404(Purchase, id=purchase_id, user=request.user)
    data = f"{request.user.profile.unique_key}-{purchase.unique_id}"
    img = generate_qr_code(data)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    context = {
        'purchase': purchase,
        'qr_code': img_str,
    }
    return render(request, 'tickets/view_qr_code.html', context)


# Administration

@login_required
def create_ticket(request):
    if not request.user.is_superuser:
        return redirect('user_dashboard')

    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        ticket = Ticket.objects.create(name=name, description=description, price=price)

        AdminLog.objects.create(admin=request.user, action='create', ticket_name=ticket.name)

        return redirect('user_dashboard')

    return render(request, 'create_ticket.html')


@login_required
def delete_ticket(request, ticket_id):
    if not request.user.is_superuser:
        return redirect('user_dashboard')

    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.delete()

    AdminLog.objects.create(admin=request.user, action='delete', ticket_name=ticket.name)

    return redirect('user_dashboard')