import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Fonts and canvas to starting writing the pdf
pdfmetrics.registerFont(TTFont('main_font', 'enticare/fonts/main_font.ttf'))
pdfmetrics.registerFont(TTFont('Caveat', 'enticare/fonts/caveat.ttf'))
pdfmetrics.registerFont(TTFont('MarckScript', 'enticare/fonts/marcks_cript.ttf'))
pdfmetrics.registerFont(TTFont('Meddon', 'enticare/fonts/meddon.ttf'))
pdfmetrics.registerFont(TTFont('Pacifico', 'enticare/fonts/pacifico.ttf'))


def generate_legal_form_pdf(data):
    """ This function is to generate pdf for legal forms """

    _canvas = canvas.Canvas('legal_form.pdf', A4)

    # Data that needs to be written dynamically
    # data = {
    #   "patient_auth": {
    #     "auth_signature": {
    #       "signature": "bishi",
    #       "font_family": "Caveat, cursive"
    #     },
    #     "auth_current_date": "2023-07-16",
    #     "auth_relation": "son",
    #     "auth_expiry": "2023-08-17",
    #     "patient_name": "bisharat",
    #     "auth_date": "2023-08-16"
    #   },
    #   "patient_financial_policy": {
    #     "patient_financial_signature": {
    #       "signature": "test",
    #       "font_family": "'Marck Script', cursive"
    #     },
    #     "patient_financial_name": "test",
    #     "patient_financial_date": "2023-08-23"
    #   },
    #   "medication_history_consent": {
    #     "patient_consent_name": "test",
    #     "medication_consent_date": "2023-08-17",
    #     "patient_financial_signature": {
    #       "signature": "test",
    #       "font_family": "Meddon, cursive"
    #     }
    #   },
    #   "communication_consent": {
    #     "communication_patient_name": "test",
    #     "communication_consent_signature": {
    #       "signature": "bishi",
    #       "font_family": "Pacifico, cursive"
    #     },
    #     "communication_consent_date": "2023-08-16"
    #   },
    #   "procedures_in_office": {
    #     "office_procedures_signature": {
    #       "signature": "test",
    #       "font_family": "Caveat, cursive"
    #     },
    #     "procedure_print_name": "test",
    #     "procedure_date": "2023-08-11",
    #     "procedure_relation": "test"
    #   }
    # }

    # Main font that will be used for every text
    _canvas.setFont('main_font', 10)
    # Draw patient authorization static pdf at full page to write dynamic data on it
    _canvas.drawImage('enticare/forms_jpg/patient_authorization.jpg', 0, 0, 600, 840)
    # Write dynamic data on the form
    _canvas.drawString(70, 670, data['patient_auth']['patient_name'])
    _canvas.drawString(450, 670, data['patient_auth']['auth_date'])
    _canvas.drawString(445, 173, data['patient_auth']['auth_current_date'])
    _canvas.drawString(185, 225, data['patient_auth']['auth_expiry'])
    _canvas.drawString(100, 116, data['patient_auth']['auth_relation'])
    # Set font for signature
    signature_font = data['patient_auth']['auth_signature']['font_family'].split(",")[0].replace(" ", "").replace("'","")
    _canvas.setFont(signature_font, 10)
    _canvas.drawString(100, 175, data['patient_auth']['auth_signature']['signature'])
    # save page
    _canvas.showPage()


    # Main font that will be used for every text
    _canvas.setFont('main_font', 10)
    # Draw financial policy static pdf at full page to write dynamic data on it
    _canvas.drawImage('enticare/forms_jpg/financial_policy.jpg', 0, 0, 600, 840)
    # Write dynamic data on the form
    _canvas.drawString(330, 107, data['patient_financial_policy']['patient_financial_name'])
    _canvas.drawString(500, 107, data['patient_financial_policy']['patient_financial_date'])
    # Set font for signature
    signature_font = data['patient_financial_policy']['patient_financial_signature']['font_family'].split(",")[0].replace(" ", "").replace("'","")
    _canvas.setFont(signature_font, 10)
    _canvas.drawString(100, 107, data['patient_financial_policy']['patient_financial_signature']['signature'])
    # save page
    _canvas.showPage()


    # Main font that will be used for every text
    _canvas.setFont('main_font', 10)
    # Draw medication history / communication consent static pdf at full page to write dynamic data on it
    _canvas.drawImage('enticare/forms_jpg/medication_history.jpg', 0, 0, 600, 840)
    # Write dynamic data on the form
    _canvas.drawString(120, 415, data['medication_history_consent']['patient_consent_name'])
    _canvas.drawString(490, 365, data['medication_history_consent']['medication_consent_date'])
    # Set font for signature
    signature_font = data['medication_history_consent']['patient_financial_signature']['font_family'].split(",")[0].replace(" ", "").replace("'","")
    _canvas.setFont(signature_font, 10)
    _canvas.drawString(120, 365, data['medication_history_consent']['patient_financial_signature']['signature'])

    _canvas.setFont('main_font', 10)
    _canvas.drawString(120, 180, data['communication_consent']['communication_patient_name'])
    _canvas.drawString(490, 128, data['communication_consent']['communication_consent_date'])
    # Set font for signature
    signature_font = data['communication_consent']['communication_consent_signature']['font_family'].split(",")[0].replace(" ", "").replace("'","")
    _canvas.setFont(signature_font, 10)
    _canvas.drawString(120, 128, data['communication_consent']['communication_consent_signature']['signature'])
    # save page
    _canvas.showPage()


    # Main font that will be used for every text
    _canvas.setFont('main_font', 10)
    # Draw Office procedure static pdf at full page to write dynamic data on it
    _canvas.drawImage('enticare/forms_jpg/procedure_in_office.jpg', 0, 0, 600, 840)
    # Write dynamic data on the form
    _canvas.drawString(140, 203, data['procedures_in_office']['procedure_print_name'])
    _canvas.drawString(455, 150, data['procedures_in_office']['procedure_date'])
    _canvas.drawString(455, 203, data['procedures_in_office']['procedure_relation'])
    # Set font for signature
    signature_font = data['procedures_in_office']['office_procedures_signature']['font_family'].split(",")[0].replace(" ", "").replace("'","")
    _canvas.setFont(signature_font, 10)
    _canvas.drawString(140, 150, data['procedures_in_office']['office_procedures_signature']['signature'])
    # save page
    _canvas.showPage()

    # Save PDF
    _canvas.save()