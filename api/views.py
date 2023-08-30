from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from .models import CartItem, Cart, Order, OrderItem, Category
from .models import Product
from .serializers import ProductSerializer, UserSerializer, CartItemSerializer, CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User


@api_view(['GET'])
def get_products(request):
    category = request.GET.get('category', None)
    if category:
        products = Product.objects.filter(category__name=category)
    else:
        products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_to_cart(request):
    user = request.user
    product_id = request.data['product_id']
    quantity = request.data.get('quantity', 1)

    cart, created = Cart.objects.get_or_create(user=user, defaults={'user': user})

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product_id, defaults={
        'quantity': quantity,
        'cart': cart,
        'product_id': product_id
    })

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data)


@api_view(['DELETE'])
def remove_from_cart(request, pk):
    # Implementasi detail logika untuk menghapus item dari keranjang

    return Response("Item removed from cart")


@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
            username=data['username'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def checkout(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    order = Order.objects.create(user=user)

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )
        # Update stok produk
        product = item.product
        product.stock -= item.quantity
        product.save()

    cart.items.clear()
    return Response("Checkout successful")


@api_view(['GET'])
def list_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


from django.db.models import Q

@api_view(['GET'])
def search_products(request):
    query = request.query_params.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(category__name__icontains=query)
    )
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def register(request):
    print("Request Data:", request.data)  # Menambahkan debug print

    if 'username' not in request.data or 'password' not in request.data:
        return Response({'error': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    username = request.data['username']
    password = request.data['password']

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists. Please choose a different username.'}, status=status.HTTP_400_BAD_REQUEST)

    if len(password) < 8:
        return Response({'error': 'Password must be at least 8 characters long.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    return Response({'message': 'Login failed'}, status=401)