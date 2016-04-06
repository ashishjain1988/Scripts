from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import scipy.io
import csv
count = 0;
set=""
Bowtie1Path="/home/jain/Placenta_Geo_Dataset/E9.5_Mouse_Studies/Bowtie1_Output_mm9/HtSeq_Counts_3_31_2016/DESeq_Analysis_4_01_2016/GREAT_output_4_6_2016"
Bowtie2Path="/home/jain/Placenta_Geo_Dataset/E9.5_Mouse_Studies/Bowtie2_Output_mm9/HtSeq_Counts_3_31_2016/DESeq_Analysis_4_1_2016/GREAT_output_4_6_2016"
file1="deseq_E95_TGC_In-Vitro_TGC/file_Placenta_High_In_E95_TGC.genes.bed_GREAT"
file2="deseq_E95_TGC_In-Vitro_TGC/file_Placenta_High_In_In-Vitro_TGC.bed_GREAT"
fileName="GOBiologicalProcess.tsv"
with open(Bowtie1Path+'/'+file1+'/'+fileName,'r') as f:
    for i in range(8):
        next(f)
    reader=csv.reader(f,delimiter='\t')
    for row in reader:
        #print row[17]
        if(float(row[17]) >=2.0):
            set= set + " "+ row[1]
set2=""
with open(Bowtie1Path+'/'+file2+'/'+fileName,'r') as f:
    for i in range(8):
        next(f)
    reader=csv.reader(f,delimiter='\t')
    for row in reader:
        #print row[17]
        if(float(row[17]) >=2.0):
            set2= set2 + " "+ row[1]
train_set=(set,set2)
stopList=("of","and","to","in","or","at","an","from")
print type(stopList)
count_vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = stopList,   \
                             max_features = 5000)
count_vectorizer.fit_transform(train_set)
freq_term_matrix = count_vectorizer.transform(train_set) #tf-idf
vocab = count_vectorizer.get_feature_names()
#print vocab #Kaggle Tutorial
#print freq_term_matrix.todense()
frequency = freq_term_matrix.todense().tolist() #tf-idf
result=(vocab,frequency[0],frequency[1])
final_result=zip(*result)
#print final_result
with open('results.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter='\t',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["Word","Bowtie1","Bowtie2"])
    for element in final_result:
        spamwriter.writerow(element);
#tfidf_vectorizer = TfidfVectorizer() #Cosine Similarity
#tfidf_matrix = tfidf_vectorizer.fit_transform(train_set) #Cosine Similarity
#print tfidf_matrix
#scipy.io.mmwrite("tf_idf", tfidf_matrix) 
#cosine_similarity(tfidf_matrix[0:1], tfidf_matrix) #Cosine Similarity