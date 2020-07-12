from flask import Blueprint, render_template, request, jsonify
import json

# Constants
STANDARD_DEDUCTION = 50000
EMPLOYEE_PF_PER = 12

MAX_PROFESSIONAL_TAX = 200
MAX_HOME_LOAN_INTEREST = 200000
MAX_80C = 150000
MAX_80D_SELF = 25000
MAX_80D_PARENTS = 50000
MAX_80D_BOTH = MAX_80D_SELF + MAX_80D_PARENTS
MAX_80TTA = 10000

TAX_ABOVE_2_5_TO_5_0_PER = 5
TAX_ABOVE_5_0_TO_7_5_PER = 10
TAX_ABOVE_7_5_TO_10_0_PER = 15
TAX_ABOVE_10_0_TO_12_5_PER = 25
TAX_ABOVE_12_5_TO_15_0_PER = 25
TAX_ABOVE_15_0_PER = 30

estimate_bp = Blueprint('estimate', __name__, url_prefix='/estimate')

@estimate_bp.route('', methods=['GET', 'POST']) # .../estimate can be called.
def estimate():
    details = getDetails(request)

    taxDetails = calculateTax(details)

    #return render_template('estimate.html', first_name = details['basic_details']['first_name'], taxPayable = taxDetails['payable'])
    return jsonify(details, taxDetails)
# end estimate

def getDetails(request):
    details = {}
    details['basic'] = getBasicDetails(request)
    details['salary'] = getSalaryDetails(request)
    details['investments'] = getInvestmentDetails(request)

    return details
# end getDetails

def getBasicDetails(request):
    basic_details = {}
    basic_details['first_name'] = request.form.get("first_name", type = str)
    basic_details['last_name'] = request.form.get("last_name", type = str)
    basic_details['email'] = request.form.get("email", type = str)
    basic_details['phone'] = request.form.get("phone", default = 0, type = int)
    basic_details['city'] = request.form.get("city", type = str)

    return basic_details
# end getBasicDetails

def getSalaryDetails(request):
    salary_details = {}
    salary_details['basic_pay'] = request.form.get("basic_pay", default = 0, type = int)
    salary_details['hra_allowance'] = request.form.get("hra_allowance", default = 0, type = int)
    salary_details['hra_city_type'] = request.form.get("hra_city_type", type = str)
    salary_details['lta_allowance'] = request.form.get("lta_allowance", default = 0, type = int)
    salary_details['meal_allowance'] = request.form.get("meal_allowance", default = 0, type = int)
    salary_details['fuel_allowance'] = request.form.get("fuel_allowance", default = 0, type = int)
    salary_details['cab_allowance'] = request.form.get("cab_allowance", default = 0, type = int)
    salary_details['internet_allowance'] = request.form.get("internet_allowance", default = 0, type = int)
    salary_details['personal_allowance'] = request.form.get("personal_allowance", default = 0, type = int)
    salary_details['other_allowance'] = request.form.get("other_allowance", default = 0, type = int)
    salary_details['taxable_allowance'] = request.form.get("taxable_allowance", default = 0, type = int)
    
    return salary_details
# end getSalaryDetails

def getInvestmentDetails(request):
    investment_details = {}
    investment_details['80c_insurance_paid'] = request.form.get("80c_insurance_paid", default = 0, type = int)
    investment_details['80d_insurance_paid'] = request.form.get("80d_insurance_paid", default = 0, type = int)
    investment_details['80d_insurance_paid_type'] = request.form.get("80d_insurance_paid", type = str)
    investment_details['ppf_paid'] = request.form.get("ppf_paid", default = 0, type = int)
    investment_details['vpf_paid'] = request.form.get("vpf_paid", default = 0, type = int)
    investment_details['home_loan_principal'] = request.form.get("home_loan_principal", default = 0, type = int)
    investment_details['home_loan_interest'] = request.form.get("home_loan_interest", default = 0, type = int)
    investment_details['rent_paid'] = request.form.get("rent_paid", default = 0, type = int)
    investment_details['rent_received'] = request.form.get("rent_received", default = 0, type = int)
    investment_details['education_loan_interest'] = request.form.get("education_loan_interest", default = 0, type = int)
    investment_details['house_tax'] = request.form.get("house_tax", default = 0, type = int)
    investment_details['employee_nps_paid'] = request.form.get("employee_nps_paid", default = 0, type = int)
    investment_details['employer_nps_paid'] = request.form.get("employer_nps_paid", default = 0, type = int)
    investment_details['elss_paid'] = request.form.get("elss_paid", default = 0, type = int)
    investment_details['govt_schemes'] = request.form.get("govt_schemes", default = 0, type = int)
    investment_details['savings_interest'] = request.form.get("savings_interest", default = 0, type = int)

    return investment_details
# end getInvestmentDetails

def calculateTax(details):
    tax_details = {}

    sum_80c = 0
    sum_80d = 0

    sum_Income_Salary = getIncomeFromSalary(details['salary'])
    sum_80c = get80cDetails(details['investments'], details['salary']['basic_pay'])
    sum_80d = get80dDetails(details['investments'])
    sum_10 = get10Details(details) # Rental
    sum_24 = get24Details(details['investments']) # Income From Other Sources
    sum_80tta = get80ttaDetails(details['investments'])
    sum_80ccd = get80ccdDetails(details['investments'])
    sum_80e = get80eDetails(details['investments'])
    sum_Prof_Tax = MAX_PROFESSIONAL_TAX * 12

    tax_details['incomeFromSalary'] = sum_Income_Salary
    tax_details['total_10'] = sum_10 * 12
    tax_details['total_24'] = sum_24
    tax_details['total_80c'] = sum_80c
    tax_details['total_80d'] = sum_80d
    tax_details['total_80ccd'] = sum_80ccd
    tax_details['total_80e'] = sum_80e
    tax_details['total_80tta'] = sum_80tta
    tax_details['total_profTaxReimbursed'] = sum_Prof_Tax
    tax_details['grossSalary'] = (tax_details['incomeFromSalary'] * 12) + tax_details['total_profTaxReimbursed']
    tax_details['totalDeductions'] = (tax_details['total_10'] + tax_details['total_24'] + tax_details['total_80c'] + tax_details['total_80d'] + tax_details['total_80tta'] + tax_details['total_80ccd'] + tax_details['total_80e'])

    tax_details['taxPayable'] = tax_details['grossSalary'] - tax_details['totalDeductions']

    return tax_details
# end taxDetails

def getIncomeFromSalary(salaryDetails):    
    sum_Income = salaryDetails['basic_pay'] + salaryDetails['taxable_allowance'] + salaryDetails['hra_allowance']

    return sum_Income
# end getIncomeFromSalary

def get80ccdDetails(investmentDetails):
    return investmentDetails['employee_nps_paid'] + investmentDetails['employer_nps_paid']
# end get80ccdDetails

def get80eDetails(investmentDetails):
    return investmentDetails['education_loan_interest']
# end get80eeDetails

def get24Details(investmentDetails):
    house_Repairs = (investmentDetails['rent_received'] * 0.3 // 100)
    sum_24 = investmentDetails['home_loan_interest'] + investmentDetails['house_tax'] - investmentDetails['rent_received'] - house_Repairs

    return sum_24
# end get24Details

def get10Details(details):
    hra_Calc = 0
    hra_Per = 40
    if details['salary']['hra_city_type'] == "METRO":
        hra_Per = 50
    
    hra_Allowable = (details['salary']['basic_pay'] * hra_Per // 100)
    if details['salary']['hra_allowance'] > hra_Allowable:
        hra_Allowable = details['salary']['hra_allowance']
    
    hra_Calc += min(hra_Allowable, details['investments']['rent_paid'], (details['investments']['rent_paid'] - 0.1 * details['salary']['basic_pay']))
    return hra_Calc
# end getHRA

def capTo80cLimit(sum_80c):
    if (sum_80c > MAX_80C):
        return MAX_80C
    
    return sum_80c
# end capTo80cLimit

def get80cDetails(investmentDetails, basic_pay):
    sum_80c = 0 
    sum_80c += investmentDetails['80c_insurance_paid'] 
    sum_80c += investmentDetails['ppf_paid']
    sum_80c += investmentDetails['vpf_paid']
    sum_80c += investmentDetails['home_loan_principal']
    sum_80c += investmentDetails['elss_paid']
    

    sum_80c += (basic_pay * EMPLOYEE_PF_PER // 100)
    val_80c = capTo80cLimit(sum_80c)

    return val_80c
# get 80cDetails

def capTo80dLimit(sum_80d, type_80d):
    if (type_80d == "SELF") & (sum_80d > MAX_80D_SELF):
        return MAX_80D_SELF
    elif (type_80d == "PARENTS") & (sum_80d > MAX_80D_PARENTS):
        return MAX_80D_PARENTS
    elif (type_80d == "BOTH") & (sum_80d > MAX_80D_BOTH):
        return MAX_80D_SELF + MAX_80D_PARENTS

    return sum_80d
# end capTo80dLimit

def get80dDetails(investmentDetails):
    sum_80d = investmentDetails['80d_insurance_paid']

    val_80d = capTo80dLimit(sum_80d, investmentDetails['80d_insurance_paid_type'])

    return val_80d
# get 80dDetails

def get80ttaDetails(investmentDetails):
    return investmentDetails['savings_interest']
# end get80ttaDetails
