from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . models import TemplateModel
from rest_framework.views import APIView
from .serializers import TemplateSerializers, EmailSerializers, TemplateUpdateSerializer
from rest_framework import status
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .models import TemplateModel, EmailModel
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv

load_dotenv()

# Create your views here.
def home(request):
    return render(request ,"index.html")

def email(request):
    return render(request, "email.html")

def template(request):
    return render(request, 'template.html')

def template_update(request):
    return render(request, "template_update.html")

class Template(APIView):
    def get(self, request, *args, **kwargs):
        template_data = TemplateModel.objects.all()
        serializer = TemplateSerializers(template_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer= TemplateSerializers(data=request.data)
        print(request.data)
        if serializer.is_valid():
            data = serializer.save()
            return Response({'msg': 'Added data successfully'}, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        template_name = request.data.get('name')
        if not template_name:
            return Response({'error': 'Template name is required for update'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            template_instance = TemplateModel.objects.get(name=template_name)
            file_path = template_instance.file.path
            print(file_path)
            if os.path.isfile(file_path):  
                os.remove(file_path) 
        except TemplateModel.DoesNotExist:
            return Response({'error': 'Template not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TemplateUpdateSerializer(template_instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Updated data successfully'}, status=status.HTTP_200_OK)
        
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    

class EmailSender(APIView):
    def post(self, request):
        data=request.data
        serializer= EmailSerializers(data=request.data)
        template = data.get("template")
        receiver_email = data.get("to")
        name = data.get("name")
        template_data = TemplateModel.objects.get(name = template)
        e_name = f"Hi {name}"
        body = (template_data.body).replace("Hi,", e_name)
        subject = template_data.subject
        pdf_file = template_data.file
        print(body)
        if serializer.is_valid():
            sender_email = os.getenv('SENDER_EMAIL') 
            smtp_server = os.getenv('SMTP_SERVER')
            smtp_port = os.getenv('SMTP_PORT')
            smtp_user = os.getenv('SMTP_USER') 
            smtp_password = os.getenv('SMTP_PASSWORD')

            # Create the email
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = receiver_email
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            if pdf_file:
                with pdf_file.open('rb') as pdf:
                    attachment = MIMEApplication(pdf.read(), _subtype="pdf")
                    attachment.add_header('Content-Disposition', 'attachment', filename=pdf_file.name)
                    msg.attach(attachment)

            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                
                server.starttls()
                
                server.login(smtp_user, smtp_password)
                
                server.sendmail(sender_email, receiver_email, msg.as_string())
                print("Email sent successfully!")
                
            except Exception as e:
                print(f"Error: {e}")
            finally:
                server.quit()
            # data = serializer.save()
            return Response({'msg': 'Added data successfully'}, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)