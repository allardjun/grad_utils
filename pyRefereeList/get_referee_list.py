# get list of all reference letter writers

import PyPDF2
import glob
import pandas as pd

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

data_dir = '/Users/jun/Dropbox/science/service/MCSB/Admissions/presence/'

df_referee_list = pd.DataFrame(columns=['Referee email', 'Referee name', 'studentFirstName', 'studentLastName', 'PI_phrase'])

dir_list = glob.glob(data_dir + 'all_downloads/down*')

df_student_PI_pairs = pd.read_excel(data_dir + 'Student_PI_pairs.xlsx')


for single_filename in dir_list:

    print(single_filename)

    filename = single_filename

    pdf = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdf)

    ## ---- get student name from first page
    page_one = pdfReader.getPage(0)
    #print(page_one.extractText())
    page_one_text = page_one.extractText().split("\n")
    name_line = page_one_text[-3]
    name_line = name_line[2:].split(";")[0]
    student_first_name = name_line.split(',')[1].lstrip()
    student_last_name  = name_line.split(',')[0]

    print(student_first_name + ' ' + student_last_name)

    ## ---- find PI name ---

    matched_student_name = process.extractOne(student_last_name + ", " + student_first_name, df_student_PI_pairs["Student name"], scorer=fuzz.WRatio)[0]
    #print(matched_student_name)

    student_row = df_student_PI_pairs.loc[df_student_PI_pairs["Student name"] == matched_student_name]
    PI_phrase = df_student_PI_pairs.loc[df_student_PI_pairs["Student name"] == matched_student_name]["PI phrase"].values[0]
    #print(PI_phrase)
    if PI_phrase == "TBD":
        PI_full_phrase = ""
    else:
        PI_full_phrase = "To give you a small update: " + student_first_name + " matched with Professor " + PI_phrase

    print(PI_full_phrase)        

    ## ---- get referee name and e-mail

    ### -- find pages with referee info. Search "Recommender"
    numOfPages = pdfReader.getNumPages()

    for i in range(1, numOfPages):
        #print("- - - - - - - - - - - - - - - - - - - -")
        pageObj = pdfReader.getPage(i)
        if pageObj.extractText().find('Certification Signature') > 0:
            #print("Page Number: " + str(i))
            #print(pageObj.extractText())

            try:
                recommender_cover = pageObj.extractText().split("\n")
                recommender_name_line_number = recommender_cover.index("Signature")+1
                recommender_line = recommender_cover[recommender_name_line_number]
                if student_last_name in recommender_line:
                    recommender_name = recommender_line[:recommender_line.index(student_last_name)]
                else:
                    recommender_name = recommender_line

                recommender_email_line_number = recommender_cover.index("Email")+1
                recommender_email = recommender_cover[recommender_email_line_number]

                print(recommender_name + ', e-mail:' + recommender_email) 

                            # Extract and format information from the article
                this_referee = {'Referee email':recommender_email, 
                'Referee name': recommender_name, 
                'studentFirstName': student_first_name, 
                'studentLastName': student_last_name,
                'PI_phrase': PI_full_phrase}

                df_referee_list = df_referee_list.append(this_referee, ignore_index=True) 
            except:
                print('Couldnt parse pdf for ' + student_last_name)


    # close the PDF file object
    pdf.close()

writer = pd.ExcelWriter(data_dir + 'results/writers.xlsx', engine='xlsxwriter')
df_referee_list.to_excel(writer)
writer.save()