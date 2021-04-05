from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import Bookserializer,LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth import login as book_login,logout as book_logout
# api/books
        #get=>list of all books(book_name:book1,price:150,pages:150,author:author))
        #post=>
    #{"book_name":book1,price:150,pages:150,author:author}=>model save
class BookList(APIView):
    def get(self,request,format=None):
        books=Book.objects.all()
        serializer=Bookserializer(books,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request,format=None):
        serializer=Bookserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#   api/books.id
#method get
# return that perticular book object
    #{book:"bookname",
    #price:150'
    #pages:150'
    #author:test}

class BookDetail(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get_object(self,pk):
        return Book.objects.get(id=pk)

    def get(self,request,pk, format=None):
        book=self.get_object(pk)
        serializer=Bookserializer(book)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,pk,format=None):
        book=self.get_object(pk)
        serializer=Bookserializer(book,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request,pk,format=None):
        book=self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data["user"]
        book_login(request,user)
        token,created=Token.objects.get_or_create(user=user)
        return Response({"token":token.key},status=200)

class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    def post(self,request):
        book_logout(request)
        return Response(status=status.HTTP_200_OK)