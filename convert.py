from xml.etree import ElementTree as ET
import json
import sys

orig_stdout = sys.stdout
f = open('output.txt', 'w')
sys.stdout = f

with open("batch_response_data.json") as json_file:
    json_data = json.load(json_file)


ns = {'ns': 'http://www.transunion.com/namespace/pfs/v4'}
for data in json_data:
    root = ET.fromstring(data)
        
    print "TRANSUNION CREDIT REPORT\n"
    print "<FOR>           <SUB NAME>          <MKT SUB>  <INFILE>    <DATE>     <TIME>"
    print "(I) " + ("X" * len(root.find(".//ns:industryCode", ns).text)).ljust(12) + "XXXXX XXXXX".ljust(20) + "00 XX".ljust(11) + "0/00".ljust(12) + "00/00/00".ljust(11) + "10:00CT\n"
    print "<SUBJECT>                                            <SSN>       <BIRTH DATE>"
    print ("X" * len(root.find('.//ns:last', ns).text) + ", " + "X" * len(root.find('.//ns:first', ns).text)).ljust(53) + "XXX".ljust(12) + "00/00/00".ljust(12)
    print "<CURRENT ADDRESS>                                                 <DATE RPTD> "
    indicative = root.findall('.//ns:indicative', ns)[1]
    print ("X" * len(str(indicative[1][0][0].text)) + ", " + "X" * len(str(indicative[1][1][0].text)) + " " + "X" * len(str(indicative[1][1][1].text)) + ". " + "0" * len(str(indicative[1][1][2].text))).ljust(66) 
    print "<FORMER ADDRESS>"
    former_address = indicative[2]
    if former_address.find('.//ns:address', ns) is None:
        print ""
    else:
        print ("X" * len(str(indicative[2][0][1][0].text)) + ", " + "X" * len(str(indicative[2][0][2][0].text)) + " " + "X" * len(str(indicative[2][0][2][1].text)) + ". " + "0" * len(str(indicative[2][0][2][2].text))).ljust(66)
    print "                                        <POSITION>"
    print "<CURRENT EMPLOYER AND ADDRESS                           <RPTD><HIRE>"
    print "XXXX".ljust(40) + "XX".ljust(16) + "0/00".ljust(4) + "0/00".ljust(4)
    print "<FORMER EMPLOYER AND ADDRESS>"
    print "XXXX".ljust(40) + "XX".ljust(16) + "0/00".ljust(4) + "0/00".ljust(4)
    print ""
    print "                  ***WARNING INTERNAL USE ONLY - NOT FOR RESALE***"
    print "--------------------------------------------------------------------------------------"
    print "S P E C I A L M E S S A G E S"
    print "****HIGH RISK FRAUD ALERT:INPUT SSN NOT ISSUED BY SOCIAL SECURITY"
    print "                          ADMINISTRATION***"
    print "--------------------------------------------------------------------------------------"
    print "M O D E L  P R O F I L E          * * * A L E R T * * *"
    print "***RECOVERY MODEL 1.0 SCORE +675 : ***"
    print "***NEW ACCT MODEL 2.0 ALERT: SCORE +731 : 010, 017, 031, 058 *** IN"
    print "***ADDITION TO THE FACTORS LISTED ABOVE, THE NUMBER OF INQUIRIES ON THE"
    print "***CONSUMER'S CREDIT FILE HAS ADVERSELY AFFECTED THE CREDIT SCORE."
    print "--------------------------------------------------------------------------------------"
    print "T R A D E S"
    print "SUBNAME       SUBCODE    OPENED      HIGHCRED   TERMS         MAXDELQ PAYPAT  1-12 MOP"
    print "ACCOUNT#                 VERFIED     CREDLIM    PASTDUE       AMT-MOP PAYPAT 13-24"
    print "ECOA COLLATRL/LOANTYPE   CLSD/PD     BALANCE    REMARKS                   MO 30/60/90"
    tradeAccounts = root.find('.//ns:tradeAccounts', ns)
    for account in tradeAccounts:
        subname = str(account[2][2][1].text)
        subcode = str(account[2][0].text) + " " + str(account[2][1].text)
        opened = str(account[6].text)
        highcred = str(account[12].text)
        if highcred == 'None':
            highcred = "???"
        terms = "???"
        if len(account[15]):
            terms = str(account[15][0].text) + str(account[15][1].text)
        accountnumber = str(account[4].text)
        verified = str(account[7].text)
        credlim = str(account[13].text)
        if credlim == 'None':
            credlim = "???"
        pastdue = str(account[17].text)
        if pastdue == 'None':
            pastdue = "???"
        ecoa = str(account[5].text)
        loantype = str(account[3].text)
        closed = str(account[8].text)
        if closed == 'None':
            closed = "???"
        balance = str(account[11].text)
        if balance == 'None':
            balance = "???"
        remarks = str(account[1].text)
        if remarks == 'None':
            remarks = "???"
        startdate = "     ???"
        paypattext = "     ???"
        paypathistory = "  ???"
        if len(account[18].find('ns:paymentPattern', ns)):
            paypat = account[18].find('ns:paymentPattern', ns)
            startdate = str(paypat[0].text)
            paypattext = str(paypat[1].text)
        if len(account[18].find('ns:historicalCounters', ns)):
            history = account[18].find('ns:historicalCounters', ns)
            paypathistory = str(history[0].text) + " " + str(history[1].text) + "/" + str(history[2].text) + "/" + str(history[3].text)
        print subname.ljust(14) + subcode.ljust(11) + opened.ljust(12) + highcred.ljust(11) + terms.ljust(14) + " ".ljust(8) + startdate
        print accountnumber.ljust(25) + verified.ljust(12) + credlim.ljust(11) + pastdue.ljust(14) + " ".ljust(8) + paypattext
        print ecoa[0].ljust(5) + loantype.ljust(20) + closed.ljust(12) + balance.ljust(11) + remarks.ljust(25) + paypathistory
        print ""
    print "--------------------------------------------------------------------------------------"
    print "I N Q U I R I E S"
    print "DATE    SUBCODE     SUBNAME     TYPE     AMOUNT"
    print ""
    print "--------------------------------------------------------------------------------------"
    print "C R E D I T  R E P O R T  S E R V I C E D  B Y :"
    print ""
    print "                            END OF TRANSUNION REPORT"
    print "\n"

sys.stdout = orig_stdout
f.close()