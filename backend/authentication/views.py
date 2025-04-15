from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username_or_email = attrs.get('username')
        password = attrs.get('password')

        if not username_or_email:
            raise serializers.ValidationError({
                'username': ['This field is required.']
            })

        if not password:
            raise serializers.ValidationError({
                'password': ['This field is required.']
            })

        # Try to authenticate with username first
        user = authenticate(username=username_or_email, password=password)
        
        # If authentication fails, try with email
        if not user:
            try:
                user = User.objects.get(email=username_or_email)
                user = authenticate(username=user.username, password=password)
            except User.DoesNotExist:
                raise serializers.ValidationError({
                    'username': ['Invalid username/email or password']
                })

        if not user:
            raise serializers.ValidationError({
                'username': ['Invalid username/email or password']
            })

        data = super().validate(attrs)
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Please provide username and password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create(
            username=username,
            email=email if email else '',  # Make email optional
            password=make_password(password)
        )

        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_user_profile(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    try:
        print("Received login request data:", request.data)
        
        username_or_email = request.data.get('username')
        password = request.data.get('password')

        if not username_or_email:
            return Response(
                {'error': 'Username/email is required', 'field': 'username'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not password:
            return Response(
                {'error': 'Password is required', 'field': 'password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Try to authenticate with username first
        user = authenticate(username=username_or_email, password=password)
        
        # If authentication fails, try with email
        if not user:
            try:
                user = User.objects.get(email=username_or_email)
                user = authenticate(username=user.username, password=password)
            except User.DoesNotExist:
                print(f"User not found with username/email: {username_or_email}")
                return Response(
                    {'error': 'Invalid username/email or password', 'field': 'username'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        if not user:
            return Response(
                {'error': 'Invalid username/email or password', 'field': 'username'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })

    except Exception as e:
        print(f"Login error: {str(e)}")
        return Response(
            {'error': 'An error occurred during login'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 