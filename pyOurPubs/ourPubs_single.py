from pymed import PubMed
import pandas as pd
import xlsxwriter

from grad_utils import Student

def get_pubs(thisStudent):

    # Create a PubMed object that GraphQL can use to query
    # Note that the parameters are not required but kindly requested by PubMed Central
    # https://www.ncbi.nlm.nih.gov/pmc/tools/developers/
    pubmed = PubMed(tool="PhDProgramDirectoryMaker", email="jun.allard@uci.edu")

    # Create a GraphQL query in plain text

    queryTemplate = '((Irvine[Ad]) AND ("2022/01/01"[Date - Create] : "3000"[Date - Create])) AND ({thisStudentLastName} {thisStudentFirstInitial}*[Author]) AND ({thisPILastName}[Author])'
    query=queryTemplate.format(thisStudentLastName=thisStudent.lastName,
         thisStudentFirstInitial=thisStudent.firstName[0], 
         thisPILastName=thisStudent.PILastName)

    #print(query)

    # Execute the query against the API
    results = pubmed.query(query, max_results=500)

    #print(results)

    # create dataframe
    df_pub_list = pd.DataFrame(columns=['studentFirstName', 'studentLastName', 'PILastName', 'Title', 'Journal', 'Date','pmid'])

    # Loop over the retrieved articles
    try:
        #print('hello')
        for article in results:
            # print('begin article')
            # # Extract and format information from the article
            # article_id = article.pubmed_id
            # title = article.title
            # publication_date = article.publication_date
            # abstract = article.abstract
            # # Show information about the article
            # print(
            #     f'{publication_date} - {title}\n'
            # )
            # print('old article assignments')
            # ------ END TEST

            # Extract and format information from the article
            this_pub = {'studentFirstName':thisStudent.firstName, 
                'studentLastName':thisStudent.lastName, 
                'PILastName':thisStudent.PILastName, 
                'Title':article.title, 
                'Journal':article.journal, 
                'Date':str(article.publication_date),
                'pmid':article.pubmed_id.partition('\n')[0]}
            # Show information about the article
            #print('dict created')
            #print(str(this_pub['Date']) + ': ' + str(this_pub['Title']))

            #print(this_pub)
            df_pub_list = df_pub_list.append(this_pub, ignore_index=True) 
    except:
        print("Unable to find any PubMed articles for " + thisStudent.lastName + "\n")

    #print(df_pub_list) 
    return df_pub_list



if __name__ == "__main__":

    thisStudent = Student('Park', 'Sohyeon')
    thisStudent.PILastName = 'Allard'
    print(get_pubs(thisStudent))