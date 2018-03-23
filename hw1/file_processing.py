"""
Group:
    Harveen Oberoi
    Lucas Duarte Bahia
    Daniel Rojas Coy
    Jordan Giebas

HW1 Pr1 (a):
    Convert programming prep homework cpp
    code into python.
"""

# Define the input/output files
# Check to make sure both file objects have been created successfully
try:
    inFile  = open("cme.20180320.c.pa2", 'r')
    outFile = open("python_CL_and_NG_expirations_and_settlements.txt", 'w')
except IOError:
    print("input or output file not created successfully!")

# Proceed with the program
not_yet_displayed_header = True;

# Write to file
outFile.write("Futures   Contract   Contract   Futures     Options   Options\n")
outFile.write("Code      Month      Type       Exp Date    Code      Exp Date\n")
outFile.write("-------   --------   --------   --------    -------   --------\n")

for line in inFile:

    rec_type = line[0:2]

    if (rec_type == "B "):

        futures_code = line[99:109][0:3]
        contract_code_first_3 = line[5:8]

        if(futures_code == "CL " and (contract_code_first_3=="CL " or contract_code_first_3=="LO ") or 
           (futures_code=="NG " and (contract_code_first_3=="NG " or contract_code_first_3=="ON "))):

            contract_month = line[18:24]
            
            if(contract_month >= "201807" and contract_month <= "202012"):

                contract_month = contract_month[0:4] + "-" + contract_month[4:]
                contract_type_raw = line[15:18]
                contract_type = ""
                futures_exp_date = ""
                option_code = ""
                options_exp_date = ""
                if(contract_type_raw == "FUT"):

                    contract_type = "Fut"
                    futures_exp_date = line[91:99]
                    futures_exp_date = futures_exp_date[0:4] + "-" + futures_exp_date[4:6] + "-" + futures_exp_date[6:]

                elif(contract_type_raw == "OOF"):

                    if(contract_code_first_3=="LO " or contract_code_first_3=="ON "):

                        contract_type = "Opt"
                        options_exp_date = line[91:99]
                        options_exp_date = options_exp_date[0:4] + "-" + options_exp_date[4:6] + "-" + options_exp_date[6:]
                        option_code = contract_code_first_3[0:2]
                        outFile.write( "{:10}{:11}{:11}{:12}{:10}{:8}\n".format(futures_code,contract_month,contract_type,futures_exp_date,option_code,options_exp_date) )



    elif (rec_type == "81"):

        CL_tick_size = 0.01; NG_tick_size = 0.001; NG_futures_fudge_factor = 0.01; NG_options_fudge_factor = 0.1;
        futures_code = line[15:25][0:3]; contract_code_first_3 = line[5:8]
        if(futures_code=="CL " and (contract_code_first_3=="CL " or contract_code_first_3=="LO ") or 
           (futures_code=="NG " and (contract_code_first_3=="NG " or contract_code_first_3=="ON "))):

            if(not_yet_displayed_header):
                outFile.write("Futures   Contract   Contract   Strike   Settlement\n")
                outFile.write("Code      Month      Type       Price    Price\n")
                outFile.write("-------   --------   --------   ------   ----------\n")
                not_yet_displayed_header = False

            contract_month = line[29:35]
            if(contract_month >= "201807" and contract_month <= "202012"):

                contract_month = contract_month[0:4] + "-" + contract_month[4:]
                contract_type_raw = line[25:28]
                C_or_P = line[28:29]
                contract_type = ""
                strike_price_ticks = int(line[47:54]); strike_price = -1.0
                settlement_price_ticks = int(line[108:122]); settlement_price = -1.0
                if(contract_type_raw=="FUT"):
                    contract_type = "Fut"
                    if(futures_code=="CL "):
                        settlement_price = round(settlement_price_ticks * CL_tick_size, 2)
                        outFile.write( "{:10}{:11}{:11}{:6} {:>10.2f}\n".format(futures_code,contract_month,contract_type,"",settlement_price)  )
                    else:
                        settlement_price = round(settlement_price_ticks * NG_tick_size * NG_futures_fudge_factor, 2)
                        outFile.write( "{:10}{:11}{:11}{:7} {:>10.2f}\n".format(futures_code,contract_month,contract_type,"",settlement_price)  )
                elif(contract_type_raw=="OOF"):
                    if(C_or_P == "C"):
                        contract_type = "Call"
                    else:
                        contract_type = "Put"
                    
                    if(futures_code=="CL "):
                        strike_price = round(strike_price_ticks* CL_tick_size, 3)
                        settlement_price = round(settlement_price_ticks * CL_tick_size, 3)
                        outFile.write( "{:10}{:11}{:11}{:6.3f}{:>10.3f}\n".format(futures_code,contract_month,contract_type,strike_price,settlement_price)  )
                    else:
                        strike_price = round(strike_price_ticks* NG_tick_size, 4)
                        settlement_price = round(settlement_price_ticks * NG_tick_size * NG_options_fudge_factor, 4)
                        outFile.write( "{:10}{:11}{:11}{:7.3f}{:>10.4f}\n".format(futures_code,contract_month,contract_type,strike_price,settlement_price)  )
 


# Close the opened file objs
inFile.close()
outFile.close()
