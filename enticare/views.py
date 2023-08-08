from django.shortcuts import render
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os import environ
import os


# Create your views here.
class GeneratePDF(APIView):
    def post(self, request):
        """Generate PDF based on payload data"""
        try:
            payload = request.data  # Assuming the payload data is available in the request
            if payload:
            # Access the required data from the payload
                start = payload.get('start', {})
                patient_info = payload.get('patient_info', {})
                other_address = payload.get('other_address', {})
                home_phone = payload.get('home_phone', '')
                cell_phone = payload.get('cell_phone', '')
                work_phone = payload.get('work_phone', '')
                preferred_method = payload.get('preferred_method', '')
                email = payload.get('email', '')
                pharmacy_name_city = payload.get('pharmacy_name_city', '')
                cross_street = payload.get('cross_street', '')
                phone = payload.get('phone', '')
                referral_info = payload.get('referral_info', {})
                federal_privacy_standards = payload.get('federal_privacy_standards', {})
                hippa_approved_contacts = payload.get('hippa_approved_contacts', {})
                emergency_contact = payload.get('emergency_contact', {})
                height = payload.get('height', '')
                weight = payload.get('weight', '')
                medical_history=payload.get('medical_history', {})
                medications = payload.get('medications', {})
                allergies = payload.get('allergies')
                surgery_history = payload.get('surgery_history', {})
                family_history = payload.get('family_history', {})
                social_history = payload.get('social_history', {})
                recreational_drug_use = payload.get('recreational_drug_use', {})
                review_of_symptoms1=payload.get('review_of_symptoms1',{})
                review_of_symptoms2=payload.get('review_of_symptoms2',{})
                eustachian_tube_dysfunction=payload.get('eustachian_tube_dysfunction',{})
                the_epworth_sleepiness_scale=payload.get('the_epworth_sleepiness_scale',{})
                hearing_history_questionnaire=payload.get('hearing_history_questionnaire',{})
                allergy_history_questionnaire=payload.get('allergy_history_questionnaire',{})
                

                # Write the payload data to the template file
                temp_name = "general/templates/"
                cv_template = "output.html"  # Assuming the template file name is "cv.html"
                open(temp_name + cv_template, "w").write(render_to_string('f.html', {
                    'start': start,
                    'patient_info': patient_info,
                    'other_address': other_address,
                    'home_phone': home_phone,
                    'cell_phone': cell_phone,
                    'work_phone': work_phone,
                    'preferred_method': preferred_method,
                    'email': email,
                    'pharmacy_name_city': pharmacy_name_city,
                    'cross_street': cross_street,
                    'phone': phone,
                    'referral_info': referral_info,
                    'federal_privacy_standards':federal_privacy_standards,
                    'hippa_approved_contacts':hippa_approved_contacts,
                    'emergency_contact':emergency_contact,
                    'height':height,
                    'weight':weight,
                    'medications':medications,
                    'allergies':allergies,
                    'surgery_history':surgery_history,
                    'family_history':family_history,
                    'social_history':social_history,
                    'recreational_drug_use':recreational_drug_use,
                    'medical_history':medical_history,
                    'review_of_symptoms1':review_of_symptoms1,
                    'review_of_symptoms2':review_of_symptoms2,
                    'eustachian_tube_dysfunction':eustachian_tube_dysfunction,
                    'the_epworth_sleepiness_scale':the_epworth_sleepiness_scale,
                    'hearing_history_questionnaire':hearing_history_questionnaire,
                    'allergy_history_questionnaire':allergy_history_questionnaire,
                }))
                HTML(temp_name + cv_template).write_pdf("output.pdf",fit_to_page=True)

                # Serve the generated PDF as a response
                with open("output.pdf", 'rb') as f:
                    file_data = f.read()
                response = HttpResponse(file_data, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="output.pdf"'
                sender_email = os.environ['sender_email']
                recipient_email = os.environ['recipient_email']
                subject = "Generated FORM PDF"
                body = "Please find the generated Form PDF attached."

                msg = MIMEMultipart()
                msg['Subject'] = subject
                msg['From'] = sender_email
                msg['To'] = recipient_email

                text = MIMEText(body)
                msg.attach(text)

                # Attach the generated PDF to the email
                pdf_filename = "output.pdf"
                with open(pdf_filename, 'rb') as f:
                    attach_pdf = MIMEApplication(f.read(), Name=pdf_filename)
                attach_pdf['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
                msg.attach(attach_pdf)

                # Send the email using AWS SES
                aws_access_key_id = os.environ['CAREER_GUIDANCE_AWS_ACCESS_KEY_ID']
                aws_secret_access_key = os.environ['CAREER_GUIDANCE_AWS_SECRET_KEY_ID']
                aws_region = "us-east-1"


                client = boto3.client('ses', region_name=aws_region,
                                    aws_access_key_id=aws_access_key_id,
                                    aws_secret_access_key=aws_secret_access_key)

                response = client.send_raw_email(
                    Source=sender_email,
                    Destinations=[recipient_email],
                    RawMessage={
                        'Data': msg.as_string()
                    }
                )

                # Return a success response indicating that the email has been sent
                return Response({'message': 'CV PDF sent via email successfully.'}, status=status.HTTP_200_OK)

            else:
                return Response({'message': "Form can not be empty"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
