from xml.etree import ElementTree as ET

ns = {'ns': 'http://www.transunion.com/namespace/pfs/v4'}

def render_print_image(data):
    root = ET.fromstring(data)
        
    result = "TRANSUNION CREDIT REPORT\n\n"
    result += "<FOR>           <SUB NAME>          <MKT SUB>  <INFILE>    <DATE>     <TIME> \n"
    result += "(I) " + ("X" * len(root.find(".//ns:industryCode", ns).text)).ljust(12) + "XXXXX XXXXX".ljust(20) + "00 XX".ljust(11) + "0/00".ljust(12) + "00/00/00".ljust(11) + "10:00CT\n\n"
    result += "<SUBJECT>                                            <SSN>       <BIRTH DATE>\n"
    result += ("X" * len(root.find('.//ns:last', ns).text) + ", " + "X" * len(root.find('.//ns:first', ns).text)).ljust(53) + "XXX".ljust(12) + "00/00/00".ljust(12) + "\n"
    result += "<CURRENT ADDRESS>                                                 <DATE RPTD>\n"
    indicative = root.findall('.//ns:indicative', ns)[1]
    result += ("X" * len(str(indicative[1][0][0].text)) + ", " + "X" * len(str(indicative[1][1][0].text)) + " " + "X" * len(str(indicative[1][1][1].text)) + ". " + "0" * len(str(indicative[1][1][2].text))).ljust(66) + "".ljust(11) + "\n"
    result += "<FORMER ADDRESS>" + "".ljust(61) + "\n"
    former_address = indicative[2]
    if former_address.find('.//ns:address', ns) is None:
        result += "\n"
    else:
        result += ("X" * len(str(indicative[2][0][1][0].text)) + ", " + "X" * len(str(indicative[2][0][2][0].text)) + " " + "X" * len(str(indicative[2][0][2][1].text)) + ". " + "0" * len(str(indicative[2][0][2][2].text))).ljust(66) + "".ljust(11) + "\n"
    result += "                                        <POSITION>" + "".ljust(27) + "\n"
    result += "<CURRENT EMPLOYER AND ADDRESS                           <RPTD><HIRE>" + "".ljust(9) + "\n"
    result += "XXXX".ljust(40) + "XX".ljust(16) + "0/00".ljust(6) + "0/00".ljust(6) + "".ljust(9) + "\n"
    result += "<FORMER EMPLOYER AND ADDRESS>" + "".ljust(48) + "\n"
    result += "XXXX".ljust(40) + "XX".ljust(16) + "0/00".ljust(6) + "0/00".ljust(6) + "".ljust(9) + "\n"
    result += "\n"
    determinationStatus = root.find('.//ns:determinationStatus', ns)
    result += "                  ***WARNING INTERNAL USE ONLY - NOT FOR RESALE***" + "".ljust(11) + "\n"
    result += "-" * 77 + "\n"
    result += "S P E C I A L M E S S A G E S" + "\n"
    flag = False
    for alert in determinationStatus.findall('ns:redFlag', ns):
        if str(alert.text) == 'None':
            break
        if flag == False:
            result += "***Alerts***"  + "\n"
            flag = True
        if len(str(alert.text)) > 77:
            result += "***" + str(alert.text)[0:74]  + "\n"
            result += str(alert.text)[74:] + "***"  + "\n"
        else:
            result += "***" + str(alert.text) + "***"  + "\n"
    flag = False
    for warning in determinationStatus.findall('ns:warnings', ns):
        if str(warning.text) == 'None':
            break
        if flag == False:
            result += "***Warnings***"  + "\n"
            flag = True
        if len(str(warning.text)) > 77:
            result += "***" + str(warning.text)[0:74] + "\n"
            result += str(warning.text)[74:] + "***" + "\n"
        else:
            result += "***" + str(warning.text) + "***" + "\n"
    result += "-" * 77 + "\n"
    result += "M O D E L  P R O F I L E          * * * A L E R T * * *" + "\n"
    result += "***RECOVERY MODEL 1.0 SCORE +675 : ***" + "\n"
    result += "***NEW ACCT MODEL 2.0 ALERT: SCORE +731 : 010, 017, 031, 058 *** IN" + "\n"
    result += "***ADDITION TO THE FACTORS LISTED ABOVE, THE NUMBER OF INQUIRIES ON THE" + "\n"
    result += "***CONSUMER'S CREDIT FILE HAS ADVERSELY AFFECTED THE CREDIT SCORE." + "\n"
    result += "-" * 77 + "\n"
    result += "T R A D E S" + "\n"
    result += "SUBNAME      SUBCODE    OPENED  HIGHCRED TERMS     MAXDELQ  PAYPAT  1-12 MOP" + "\n"
    result += "ACCOUNT#                VERFIED CREDLIM  PASTDUE   AMT-MOP  PAYPAT 13-24" + "\n"
    result += "ECOA COLLATRL/LOANTYPE  CLSD/PD BALANCE  REMARKS                MO 30/60/90" + "\n"
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
        result += subname.ljust(13) + subcode.ljust(11) + (opened[5:7] + "/" + opened[2:4]).ljust(8) + highcred.ljust(9) + terms.ljust(10) + "".ljust(9) + paypattext[0:12] + "\n"
        result += accountnumber.ljust(24) + (verified[5:7] + "/" + verified[2:4]).ljust(8) + credlim.ljust(9) + pastdue.ljust(10) + "".ljust(9) + paypattext[12:24] + "\n"
        result += ecoa[0].ljust(5) + loantype.ljust(19) + closed.ljust(8) + balance.ljust(9) + remarks.ljust(23) + paypathistory + "\n"
        result += "\n"
    result += "-" * 77 + "\n"
    result += "I N Q U I R I E S" + "".ljust(60) + "\n"
    result += "DATE     SUBCODE         SUBNAME        TYPE    AMOUNT" + "".ljust(23) + "\n"
    result += "NO DATA  NO DATA         NO DATA        NO DATA NO DATA" + "".ljust(22) + "\n"
    result += "-" * 77 + "\n"
    result += "C R E D I T  R E P O R T  S E R V I C E D  B Y :" + "".ljust(29) + "\n"
    result += "\n"
    result += "                            END OF TRANSUNION REPORT" + "\n"
    result += "\n"
    return result