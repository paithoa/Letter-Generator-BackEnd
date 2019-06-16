from flask import Flask
from fpdf import FPDF,HTMLMixin

##app = Flask(__name__)
import datetime
now = datetime.datetime.now()




##@app.route("/")
class MyFPDF(FPDF, HTMLMixin):
    pass
def generate_letter():
    date = str(now)
    date_only = now.strftime("%Y/%m/%d")

    year = str(now.year)
    doctor_first_name = "Freddy"
    doctor_last_name = "Mercury "
    gender = "Male"
    if(gender == "Male"):
        gender_pronoun = "him"
    
    else:
        gender_pronoun = "her"
    
    # create gender function if m  -> male f-> female
    clinic_name = "Quahog Hospital "
    clinic_address = "Old Trafford road "
    clinician_name = "Allied Health Name"
    clinician_medicare = "1234567"
    clinician_position = "Manager"
    street_number = 123
    street_name = "Abbey's Road"
    patient_first_name = "John"
    patient_last_name = "Doe"
    patient_address = "West Virginia"
    patient_dob = "30/12/1996"
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
    pdf.ln(65)  # move 85 down
 
    # header
    pdf.cell(57.5, 10, txt=date_only,ln=1 , align="C")
    pdf.cell(74, 5, txt=header, ln=1, align= "C" )
    pdf.cell(69, 5, txt=clinic_name, ln=1, align= "C" )
    pdf.set_margins(27,0,0)

    pdf.cell(70, 5, txt=clinic_address, ln=1, align= "C" )

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


generate_letter();