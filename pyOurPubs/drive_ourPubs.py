# get recent publications from our students, taken from PubMed
# Jun allardlab.com

import pandas as pd

from grad_utils import Student
import ourPubs_single


def get_our_pubs(dfStudentList):
    # load list of students and their advisors

    #print(dfStudentList)

    # create dataframe
    df_pub_list = pd.DataFrame(columns=['studentFirstName', 'studentLastName', 'PILastName', 'Title', 'Journal', 'Date','pmid'])


    for index, df_thisStudent in dfStudentList.iterrows():

        #print(df_thisStudent)

        thisStudent = Student(df_thisStudent['Last name'],
            df_thisStudent['First name'])
        thisStudent.PILastName = df_thisStudent['PI last name']
        df_pub_list_single = ourPubs_single.get_pubs(thisStudent)

        print(df_pub_list_single)

        df_pub_list = pd.concat([df_pub_list,df_pub_list_single])

    print('And all together: \n')
    print(df_pub_list)

if __name__ == "__main__":
    if 1:
        dfStudentList = pd.read_excel('StudentList.xlsx')
    if 0:
        student_dict = {'Last name':['Park'], 
            'First name': ['Sohyeon'], 'PI last name':['Allard']}
        dfStudentList = pd.DataFrame(student_dict)
    get_our_pubs(dfStudentList)