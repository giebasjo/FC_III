
// File: file_processing.cpp
// Date: Aug. 1, 2017
// Author(s): John Ostlund
//
// Extracts expiration dates and settlement values for WTI Crude Oil (CL)
// and Henry Hub Natural Gas (NG) futures and options contracts from
// the July 31, 2017 CME SPAN file
//

#include <iostream>
#include <iomanip>
#include <fstream>
#include <string>
using namespace std;

int main()
{
    string SPAN_fname("cme.20180320.c.pa2");
    ifstream fin(SPAN_fname);
    if (!fin) {
        cout << "\nERROR opening CME SPAN file " << SPAN_fname << "\n\n";
        return 1;
    }

    string out_fname("CL_and_NG_expirations_and_settlements.txt");
    ofstream fout(out_fname);
    if (!fout) {
        cout << "\nERROR creating output file " << out_fname << "\n\n";
        return 1;
    }

/* SPAN file contents
// examples of CME SPAN file record type B
B NYM CL         FUT201710                0000000000060000023750300003300000000139726000000010000 20170920 CL           00000000         0001000000000000 00 00 010000000000  00                
B NYM LO         OOF 201710     201710    0029309500060000023750300003300000000126027000000010000 20170915 CL         M 00000000N0005026+0001000000000000 00 00 010000000000  00                
B NYM NG         FUT 201710               0000000000035000015500300003300000000158904000000010000 20170927 NG           00000000         0010000000000000 00 00 010000000000  00                
B NYM ON         OOF 201710     201710    0030967900035000015500300003300000000156164000000010000 20170926 NG         M 00000000N0283400+0010000000000000 00 00 010000000000  00                
00000 0000011111 111 112222 222 222333 3333333444444444455555555556666666666777777777788888888889 99999999 9000000000 01111111111222222
01234 5678901234 567 890123 456 789012 3456789012345678901234567890123456789012345678901234567890 12345678 9012345678 90123456789012345
*/

    bool have_not_yet_displayed_type_8_header = true;

    // heading for type B records
    string line;  // next available input line
    fout << "Futures   Contract   Contract   Futures     Options   Options\n";
    fout << "Code      Month      Type       Exp Date    Code      Exp Date\n";
    fout << "-------   --------   --------   --------    -------   --------\n";

    while (getline(fin, line)) {
        string rec_type = line.substr(0, 2);
        if (rec_type == "B ") {
            string futures_code = line.substr(99, 10).substr(0, 3);		// e.g., "CL " or "NG "
            string contract_code_first_3 = line.substr(5, 3);			// e.g., "CL ", "NG ", "LO ", "ON ", ..
            if (futures_code == "CL " && (contract_code_first_3 == "CL " || contract_code_first_3 == "LO ")
                        || (futures_code == "NG " && (contract_code_first_3 == "NG " || contract_code_first_3 == "ON "))) {
                string contract_month = line.substr(18, 6);				// e.g., "201710"
                if (contract_month >= "201710" && contract_month <= "201912") {		// not earlier than 201710, or later than 201912
                    contract_month.insert(4, "-");
                    string contract_type_raw = line.substr(15, 3);			// "FUT" or "OOF"
                    string contract_type;		// initially empty			// "Fut" or "Opt"
                    string futures_exp_date;	// initially empty			// e.g., "20170927"
                    string option_code;			// initially empty			// e.g., "LO" or "ON"
                    string options_exp_date;	// initially empty			// e.g., "20170926"
                    if (contract_type_raw == "FUT") {
                        contract_type = "Fut";
                        futures_exp_date = line.substr(91, 8);
                        futures_exp_date.insert(6, "-").insert(4, "-");
                    }
                    else if (contract_type_raw == "OOF") {  // option on future
                        if (contract_code_first_3 == "LO " || contract_code_first_3 == "ON ") {
                            contract_type = "Opt";
                            options_exp_date = line.substr(91, 8);
                            options_exp_date.insert(6, "-").insert(4, "-");
                            option_code = contract_code_first_3.substr(0, 2);
                        }
                    }
                    fout << left << setw(10) << futures_code << setw(11) << contract_month << setw(11) << contract_type
                         << setw(12) << futures_exp_date << setw(10) << option_code << setw(8) << options_exp_date << '\n';
                }
            }
        }
        else if (rec_type == "81") {
           
            double CL_tick_size = 0.01;		// $0.01 per barrel
            double NG_tick_size = 0.001;	// $0.001 per MMBtu
            double NG_futures_fudge_factor = 0.01;	// undocumented extra fudge factor for NG futures ONLY
            double NG_options_fudge_factor = 0.1;   // undocumented extra fudge factor for NG options ONLY

            string futures_code = line.substr(15, 10).substr(0, 3);		// e.g., "CL " or "NG "
            string contract_code_first_3 = line.substr(5, 3);			// e.g., "CL " or "NG " or "LO " or "ON "
            if (futures_code == "CL " && (contract_code_first_3 == "CL " || contract_code_first_3 == "LO ")
                        || futures_code == "NG " && (contract_code_first_3 == "NG " || contract_code_first_3 == "ON ")) {
                if (have_not_yet_displayed_type_8_header) {
                    fout << "Futures   Contract   Contract   Strike   Settlement\n";
                    fout << "Code      Month      Type       Price    Price\n";
                    fout << "-------   --------   --------   ------   ----------\n";
                    have_not_yet_displayed_type_8_header = false;
                }
                string contract_month = line.substr(29, 6);				// e.g., "201710"
                if (contract_month >= "201710" && contract_month <= "201912") {		// not earlier than 201710, or later than 201812
                    contract_month.insert(4, "-");
                    string contract_type_raw = line.substr(25, 3);			// "FUT" or "OOF" or "OOF"
                    string C_or_P = line.substr(28, 1);
                    string contract_type;		// initially empty			// "Fut" or "Call" or "Put"
                    int strike_price_ticks = atoi(line.substr(47, 7).c_str());
                    double strike_price(-1.0);	// initially a bogus value
                    int settlement_price_ticks = atoi(line.substr(108, 14).c_str());
                    double settlement_price(-1.0);	// initially a bogus value
                    int field_width_to_align_decimal_points = 6;			// six characters wide for 2 digits after decimal point ...
                    if (contract_type_raw == "FUT") {
                        contract_type = "Fut";
                        if (futures_code == "CL ") {
                            settlement_price = settlement_price_ticks * CL_tick_size;
                            fout << fixed << setprecision(2);
                        }
                        else {	// futures_code == "NG "
                            settlement_price = settlement_price_ticks * NG_tick_size * NG_futures_fudge_factor;
                            field_width_to_align_decimal_points = 7;		// ... or seven characters for 3 digits after decimal point
                            fout << fixed << setprecision(3);
                        }
                        fout << left << setw(10) << futures_code << setw(11) << contract_month << setw(11) << contract_type
                             << setw(field_width_to_align_decimal_points) << " " << right << setw(10) << settlement_price << '\n';
                    }
                    else if (contract_type_raw == "OOF") {  // Call option
                        if (C_or_P == "C") {
                            contract_type = "Call";
                        }
                        else {  // C_or_P == "P"
                            contract_type = "Put";
                        }
                        if (futures_code == "CL ") {
                            strike_price = strike_price_ticks * CL_tick_size;
                            settlement_price = settlement_price_ticks * CL_tick_size;
                            fout << fixed << setprecision(2);
                        }
                        else {	// futures_code == "NG "
                            strike_price = strike_price_ticks * NG_tick_size;
                            settlement_price = settlement_price_ticks * NG_tick_size * NG_options_fudge_factor;
                            field_width_to_align_decimal_points = 7;		// ... or seven characters for 3 digits after decimal point
                            fout << fixed << setprecision(3);
                        }
                        fout << left << setw(10) << futures_code << setw(11) << contract_month << setw(11) << contract_type
                             << right << setw(field_width_to_align_decimal_points) << strike_price << setw(10) << settlement_price << '\n';
                    }
                    fout << setprecision(6) << resetiosflags(ios::floatfield);
                }
            }
        }
    }

    return 0;
}
