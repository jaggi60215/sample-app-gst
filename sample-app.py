import streamlit as st
import pandas as pd
from fpdf import FPDF
import time
import datetime
  
ct = datetime.datetime.now()

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size = 15)

df = pd.DataFrame(columns = ["Items", "Price", "GST","Discount"])

org_name = 'ABC Enterprise'

global n, ts

ts = time.time()

n=1

Items=[None] * 30
Price=[None] * 30
GST=[None] * 30

def add_items(n):
    return st.text_input("Item{n}".format(n=n+1))

def add_price(n):
    return st.text_input("Item{n} price".format(n=n+1))
    
def add_gst(n):
    return st.text_input("Item{n} GST".format(n=n+1))

def main():
    st.title(org_name)
    menu = ["Home","About"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.subheader("Invoice Form")
        with st.form(key='form1'):

            Name=st.text_input("Buyer's Name")
            Seller=st.text_input("Sales Man Name")
            InvoiceDate=st.date_input("Invoice Date")
            GSTN=st.text_input("GST Number")
            NItems=st.number_input("Number of Items",min_value=1,max_value=20,format='%d')
            cnf_button=st.form_submit_button(label="Confirm",type="primary")
            col1,col2,col3=st.columns([2,1,1])
            if NItems>0:
                # with st.form(key='Item Details'):
                for i in range(NItems):
                    with col1:
                        Items[i]=add_items(i)
                    with col2:
                        Price[i]=add_price(i)
                    with col3:
                        GST[i]=add_gst(i)
            submit_button=st.form_submit_button(label="Done")
            if submit_button:
                st.success("Hello {sm}!! Your invoice has been generated.".format(sm=Seller))
                # st.write("Hello {sm}!! Your invoice has been generated.".format(sm=Seller))
                df['Items']=Items
                df['Price']=Price
                df['GST']=GST
                df['Discount']=None
                data=df.loc[~df['Items'].isna()]
                st.table(data)
                pdf.cell(200, 10, txt = org_name,ln = 1, align = 'C')
                pdf.cell(200, 10, txt = "GST Invoice Bill",ln = 2, align = 'C')                
                pdf.cell(200, 10, txt = "Invoice Date Time",ln = 2, align = 'C')                
                pdf.cell(200, 10, txt = str(ct),ln = 2, align = 'C')                
                pdf.cell(200, 10, txt = "",ln = 2, align = 'C')                
                pdf.cell(200, 10, txt = "",ln = 2, align = 'C')                
                columnNameList=data.columns
                for header in columnNameList[:-1]:
                    pdf.cell(35,10,header,1,0,'C')
                pdf.cell(35,10,columnNameList[-1],1,2,'C')
                pdf.cell(-105)
                for row in range(0,len(data)):
                    for col_num, col_name in enumerate(columnNameList):
                        if col_num != len(columnNameList)-1:
                            pdf.cell(35,10,str(data[col_name].iloc[row]),1,0,'C')
                        else:
                            pdf.cell(35,10,str(data[col_name].iloc[row]),1,2,'C')
                            pdf.cell(-105)
                pdf.output("Bill_{ts}.pdf".format(ts=ts),'F') 

        try:
            with open("Bill_{ts}.pdf".format(ts=ts), "rb") as pdf_file:
                PDFbyte = pdf_file.read()
                st.download_button(label="Download PDF",data=PDFbyte,file_name="Bill_{ts}.pdf".format(ts=ts),mime='application/octet-stream')
        except:
            pass

    else:
        st.subheader("About")


if __name__=="__main__":
    main()