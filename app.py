from flask import Flask
from flask import request
from flask import Response
from flask import send_file, send_from_directory, safe_join, abort,make_response
from flask_cors import CORS,cross_origin
from fpdf import FPDF,HTMLMixin

app = Flask(__name__)
cors=CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
import datetime
import json
import codecs


now = datetime.datetime.now()

@app.route("/submitletter",methods=['POST'])
@cross_origin()
def post_data():
    if request.method == 'POST':
        data = request.get_data()
        new_data = json.loads(data)
        doctor_name = new_data['details']['doctorName']
        doctor_name = doctor_name.split(' ')
        doctor_first_name = doctor_name[0]
        doctor_last_name = doctor_name[1]
        clinic_name = new_data['details']['clinicName']
        clinic_address = new_data['details']['clinicAddress']
        client_name = new_data['details']['clientName']
        client_gender = new_data['details']['clientGender']
        client_dob = new_data['details']['clientDOB']
        client_address = new_data['details']['clientAddress']
        clinician_name = new_data['details']['clinicianName']
        clinician_medicare = new_data['details']['clinicianMedicare']
        clinician_position = new_data['details']['clinicianPosition']

        summary = new_data['details']['summary']
        #clinic_name = data.details.clinicName
        generate_letter(doctor_first_name,doctor_last_name,clinic_name,clinic_address,client_name,client_address,client_gender,client_dob,clinician_name,clinician_medicare,clinician_position,summary)
        print(doctor_first_name,doctor_last_name,clinic_name,clinic_address,client_name,clinician_medicare,clinician_position,summary)
        return "Posted"

    else:
        return "not posted"



@app.route("/",methods=['GET'])
@cross_origin()
def get_data():
    filename = "simple_demo.pdf"
    headers = {"Content-Disposition":"attachment; filename=%s" % filename}
    with open(filename,'r') as f:
        body = f.read()
    return make_response((body,headers))
class MyFPDF(FPDF, HTMLMixin):
    pass
def generate_letter(doctor_first_name,doctor_last_name,clinic_name,clinic_address,client_name,client_address,client_gender,client_dob,clinician_name,clinician_medicare,clinician_position,summary):
    date = str(now)
    date_only = now.strftime("%Y/%m/%d")

    year = str(now.year)
    doctor_first_name = doctor_first_name
    doctor_last_name = doctor_last_name + " "
    gender = client_gender
    if(gender == "Male"):
        gender_pronoun = "him"

    else:
        gender_pronoun = "her"

    # create gender function if m  -> male f-> female
    clinic_name = clinic_name
    clinic_address = clinic_address
    clinician_name = clinician_name
    clinician_medicare = clinician_medicare
    clinician_position = clinician_position
    clinic_address_split = clinic_address.split(" ")
    street_number = clinic_address[0]
    street_name = clinic_address[1] + " Road "
    client_name = client_name.split(" ")
    patient_first_name = client_name[0]
    patient_last_name = client_name[1]
    patient_address = client_address
    patient_dob = client_dob
    header = "Dr. " + doctor_first_name + " " + doctor_last_name
    first_paragraph = "Dear Dr." + doctor_last_name
    second_paragraph = "Re: " + patient_first_name + " " +  patient_last_name+ " of " + patient_address
    third_paragraph = "Thank you for the Medicare referral for " + patient_first_name
    fourth_paragraph = "Please find enclosed the first report for the " + year + " calendar year under the Allied Health"
    fourth_paragraph_cont = "Care Referral Program "+ date_only + " . "
    fifth_paragraph = "Should you have any queries regarding " + patient_first_name + " therapy, please do not"
    fifth_paragraph_cont = "hesitate to contact me, as I would welcome the opportunity to discuss "+gender_pronoun+" progress."
    sixth_paragraph = "Yours sincerely,"
    generate_pdf(patient_dob,clinic_name,clinic_address,date_only,header,first_paragraph,second_paragraph,third_paragraph,fourth_paragraph,fourth_paragraph_cont,fifth_paragraph,fifth_paragraph_cont,sixth_paragraph,clinician_name,clinician_medicare,clinician_position);
    print(header)
    return (first_paragraph
     + "<br>" + second_paragraph + "<br>" + third_paragraph
         +"<br>" + fourth_paragraph + "<br>" + fifth_paragraph)
def generate_pdf(patient_dob,clinic_name,clinic_address,date_only,header,first,second,third,fourth,fourth_cont,fifth,fifth_cont,sixth,clinician_name,clinician_medicare,clinician_position):
    pdf = MyFPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    image_path = "header.png"
    image_path_footer = "footer.png"
    pdf.image(image_path, x=10, y=8, w=200)
    pdf.set_margins(27,0,0)
    pdf.ln(65)  # move 85 down


    # header
    pdf.cell(57, 10, txt=date_only,ln=1 )
    pdf.cell(77, 5, txt=header, ln=1 )
    pdf.cell(69, 5, txt=clinic_name, ln=1 )
    pdf.set_margins(27,0,0)

    pdf.cell(70, 5, txt=clinic_address, ln=1 )

    #body

    pdf.cell(80,15,txt=first,ln=1)
    pdf.set_font('Arial', style = 'B', size = 0)

    pdf.cell(120,10,txt=second + "               DOB:" + patient_dob,ln=1, )

    pdf.set_font('Arial', style = '', size = 0)

    pdf.cell(140,15,txt=third,ln=1, )
    pdf.cell(150,2.5,txt=fourth,ln=1, )
    pdf.cell(150,10,txt=fourth_cont,ln=1,  )

    pdf.cell(10,10,txt=fifth,ln=1 )
    pdf.cell(150,2.5,txt=fifth_cont,ln=1 )

    pdf.cell(70,40,txt=sixth,ln=1 )

    pdf.cell(70,5,txt=clinician_name,ln=1 )
    pdf.cell(70,5,txt=clinician_medicare,ln=1 )
    pdf.cell(70,5,txt=clinician_position,ln=1 )

    pdf.image(image_path_footer, x=20, y=250, w=200)



    pdf.output("simple_demo.pdf")
