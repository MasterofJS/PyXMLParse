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
    print "<FOR>           <SUB NAME>          <MKT SUB>  <INFILE>    <DATE>     <TIME> "
    print "(I) " + ("X" * len(root.find(".//ns:industryCode", ns).text)).ljust(12) + "XXXXX XXXXX".ljust(20) + "00 XX".ljust(11) + "0/00".ljust(12) + "00/00/00".ljust(11) + "10:00CT\n"
    print "<SUBJECT>                                            <SSN>       <BIRTH DATE>"
    print ("X" * len(root.find('.//ns:last', ns).text) + ", " + "X" * len(root.find('.//ns:first', ns).text)).ljust(53) + "XXX".ljust(12) + "00/00/00".ljust(12)
    print "<CURRENT ADDRESS>                                                 <DATE RPTD>"
    indicative = root.findall('.//ns:indicative', ns)[1]
    print ("X" * len(str(indicative[1][0][0].text)) + ", " + "X" * len(str(indicative[1][1][0].text)) + " " + "X" * len(str(indicative[1][1][1].text)) + ". " + "0" * len(str(indicative[1][1][2].text))).ljust(66) + "".ljust(11)
    print "<FORMER ADDRESS>" + "".ljust(61)
    former_address = indicative[2]
    if former_address.find('.//ns:address', ns) is None:
        print "".ljust(77)
    else:
        print ("X" * len(str(indicative[2][0][1][0].text)) + ", " + "X" * len(str(indicative[2][0][2][0].text)) + " " + "X" * len(str(indicative[2][0][2][1].text)) + ". " + "0" * len(str(indicative[2][0][2][2].text))).ljust(66) + "".ljust(11)
    print "                                        <POSITION>" + "".ljust(27)
    print "<CURRENT EMPLOYER AND ADDRESS                           <RPTD><HIRE>" + "".ljust(9)
    print "XXXX".ljust(40) + "XX".ljust(16) + "0/00".ljust(6) + "0/00".ljust(6) + "".ljust(9)
    print "<FORMER EMPLOYER AND ADDRESS>" + "".ljust(48)
    print "XXXX".ljust(40) + "XX".ljust(16) + "0/00".ljust(6) + "0/00".ljust(6) + "".ljust(9)
    print ""
    determinationStatus = root.find('.//ns:determinationStatus', ns)
    print "                  ***WARNING INTERNAL USE ONLY - NOT FOR RESALE***" + "".ljust(11)
    print "-" * 77
    print "S P E C I A L M E S S A G E S"
    flag = False
    for alert in determinationStatus.findall('ns:redFlag', ns):
        if str(alert.text) == 'None':
            break
        if flag == False:
            print "***Alerts***"
            flag = True
        if len(str(alert.text)) > 77:
            print "***" + str(alert.text)[0:74]
            print str(alert.text)[74:] + "***"
        else:
            print "***" + str(alert.text) + "***"
    flag = False
    for warning in determinationStatus.findall('ns:warnings', ns):
        if str(warning.text) == 'None':
            break
        if flag == False:
            print "***Warnings***"
            flag = True
        if len(str(warning.text)) > 77:
            print "***" + str(warning.text)[0:74]
            print str(warning.text)[74:] + "***"
        else:
            print "***" + str(warning.text) + "***"
    # print "****HIGH RISK FRAUD ALERT:INPUT SSN NOT ISSUED BY SOCIAL SECURITY"
    # print "                          ADMINISTRATION***"
    print "-" * 77
    print "M O D E L  P R O F I L E          * * * A L E R T * * *"
    print "***RECOVERY MODEL 1.0 SCORE +675 : ***"
    print "***NEW ACCT MODEL 2.0 ALERT: SCORE +731 : 010, 017, 031, 058 *** IN"
    print "***ADDITION TO THE FACTORS LISTED ABOVE, THE NUMBER OF INQUIRIES ON THE"
    print "***CONSUMER'S CREDIT FILE HAS ADVERSELY AFFECTED THE CREDIT SCORE."
    print "-" * 77
    print "T R A D E S"
    print "SUBNAME      SUBCODE    OPENED  HIGHCRED TERMS     MAXDELQ  PAYPAT  1-12 MOP"
    print "ACCOUNT#                VERFIED CREDLIM  PASTDUE   AMT-MOP  PAYPAT 13-24"
    print "ECOA COLLATRL/LOANTYPE  CLSD/PD BALANCE  REMARKS                MO 30/60/90"
    tradeAccounts = root.find('.//ns:tradeAccounts', ns)
    for account in tradeAccounts:
        subname = str(account[2][2][1].text)
        subcode = str(account[2][0].text) + " " + str(account[2][1].text)
        opened = str(account[6].text)
        highcred = str(account[12].text)
        if highcred == 'None':
            highcred = "???"
        else:
            highcred = "$" + str(int(highcred))
        terms = "???"
        if len(account[15]):
            terms = str(account[15][1].text)
        accountnumber = str(account[4].text)
        verified = str(account[7].text)
        credlim = str(account[13].text)
        if credlim == 'None':
            credlim = "???"
        else:
            credlim = "$" + str(int(credlim))
        pastdue = str(account[17].text)
        if pastdue == 'None':
            pastdue = "???"
        ecoa = str(account[5].text)
        loantype = str(account[3].text)
        closed = str(account[8].text)
        if closed == 'None':
            closed = "???"
        else:
            closed = closed[5:7] + "/" + closed[2:4]
        balance = str(account[11].text)
        if balance == 'None':
            balance = "???"
        else:
            balance = "$" + str(int(balance))
        remarks = str(account[1].text)
        if remarks == 'None':
            remarks = "???"
        paypattext = "     ???"
        paypathistory = " ???"
        if len(account[18].find('ns:paymentPattern', ns)):
            paypat = account[18].find('ns:paymentPattern', ns)
            startdate = str(paypat[0].text)
            paypattext = str(paypat[1].text)
        if len(account[18].find('ns:historicalCounters', ns)):
            history = account[18].find('ns:historicalCounters', ns)
            paypathistory = str(history[0].text) + " " + str(history[1].text) + "/" + str(history[2].text) + "/" + str(history[3].text)
        print subname.ljust(13) + subcode.ljust(11) + (opened[5:7] + "/" + opened[2:4]).ljust(8) + highcred.ljust(9) + terms.ljust(10) + "".ljust(9) + paypattext[0:12]
        print accountnumber.ljust(24) + (verified[5:7] + "/" + verified[2:4]).ljust(8) + credlim.ljust(9) + pastdue.ljust(10) + "".ljust(9) + paypattext[12:24]
        print ecoa[0].ljust(5) + loantype.ljust(19) + closed.ljust(8) + balance.ljust(9) + remarks.ljust(23) + paypathistory
        print ""
    print "-" * 77
    print "I N Q U I R I E S" + "".ljust(60)
    print "DATE     SUBCODE         SUBNAME        TYPE    AMOUNT" + "".ljust(23)
    print "NO DATA  NO DATA         NO DATA        NO DATA NO DATA" + "".ljust(22)
    print "-" * 77
    print "C R E D I T  R E P O R T  S E R V I C E D  B Y :" + "".ljust(29)
    print ""
    print "                            END OF TRANSUNION REPORT"
    print "\n"

sys.stdout = orig_stdout
f.close()