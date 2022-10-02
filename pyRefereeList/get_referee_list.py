import PyPDF2

data_dir = '/Users/jun/Dropbox/science/service/MCSB/Admissions/presence/'

filename = data_dir + 'download.pdf'

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

## ---- get referee name and e-mail

### -- find pages with referee info. Search "Recommender"
numOfPages = pdfReader.getNumPages()

for i in range(1, numOfPages):
    #print("- - - - - - - - - - - - - - - - - - - -")
    pageObj = pdfReader.getPage(i)
    if pageObj.extractText().find('Certification Signature') > 0:
        #print("Page Number: " + str(i))
        #print(pageObj.extractText())

        recommender_cover = pageObj.extractText().split("\n")
        recommender_name_line_number = recommender_cover.index("Signature")+1
        recommender_name = recommender_cover[recommender_name_line_number]

        recommender_email_line_number = recommender_cover.index("Email")+1
        recommender_email = recommender_cover[recommender_email_line_number]

        print(recommender_name + ', e-mail:' + recommender_email) 

    #print("- - - - - - - - - - - - - - - - - - - -")

# close the PDF file object
pdf.close()
