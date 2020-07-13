from flask import Blueprint, render_template, request, jsonify
import json

# Constants
STANDARD_DEDUCTION = 50000
EMPLOYEE_PF_PER = 12
EDUCATION_CESS_PER = 4

MAX_PROFESSIONAL_TAX = 200 * 12
MAX_24 = 200000 # Home Loan
MAX_80C = 150000 # Insurances like Life/Term, PF, VPF, PPF, 5yr FD, Tuition fees, etc
MAX_80CCD1 = 50000 # NPS Employee
MAX_80CCD2 = 50000 # NPS Employer
MAX_80E = 150000 # Education Loan
MAX_80D_SELF = 25000 # Medical Insurance Self
MAX_80D_PARENTS = 50000 # Medical Insurance Parents
MAX_80D_BOTH = MAX_80D_SELF + MAX_80D_PARENTS
MAX_80TTA = 10000 # Interest on Savings

TAX_SLAB_25 = 250000
TAX_SLAB_50 = 500000
TAX_SLAB_75 = 750000
TAX_SLAB_100 = 1000000
TAX_SLAB_125 = 1250000
TAX_SLAB_150 = 1500000

TAX_ABOVE_2_5_TO_5_0_OLD_PER = 5
TAX_ABOVE_5_0_TO_7_5_OLD_PER = 20
TAX_ABOVE_7_5_TO_10_0_OLD_PER = 20
TAX_ABOVE_10_0_TO_12_5_OLD_PER = 30
TAX_ABOVE_12_5_TO_15_0_OLD_PER = 30
TAX_ABOVE_15_0_OLD_PER = 30

TAX_ABOVE_2_5_TO_5_0_NEW_PER = 5
TAX_ABOVE_5_0_TO_7_5_NEW_PER = 10
TAX_ABOVE_7_5_TO_10_0_NEW_PER = 15
TAX_ABOVE_10_0_TO_12_5_NEW_PER = 25
TAX_ABOVE_12_5_TO_15_0_NEW_PER = 25
TAX_ABOVE_15_0_NEW_PER = 30

HOUSE_REPAIRS_PER = 30

estimate_bp = Blueprint('estimate', __name__, url_prefix='/estimate')

@estimate_bp.route('', methods=['GET', 'POST']) # .../estimate can be called.
def estimate():
    details = getDetails(request)

    taxDetails = calculateTax(details)
    #return jsonify(details, taxDetails)

    return render_template('estimate.html', firstName = details['basic']['first_name'], lastName = details['basic']['last_name'], 
                        grossIncome = taxDetails['grossIncome'], netIncome = taxDetails['netIncome'],
                        grossIncomePerMonth = taxDetails['grossIncome'] // 12, netIncomePerMonth = taxDetails['netIncome'] // 12,
                        taxPayableNew = taxDetails['taxPayableNew'], taxPayableOld = taxDetails['taxPayableOld'],
                        taxPayablePerMonthNew = taxDetails['taxPayableNew'] // 12, taxPayablePerMonthOld = taxDetails['taxPayableOld'] // 12,
                        totalSavings = 0, totalIncomeAfterDeductions = taxDetails['totalIncomeAfterDeductions'], taxExempted = taxDetails['taxExempted'],
                        total_80c = taxDetails['total_80c'], total_80d = taxDetails['total_80d'], total_80ccd1 = taxDetails['total_80ccd1'], total_80ccd2 = taxDetails['total_80ccd2'], total_80e = taxDetails['total_80e'], total_10 = taxDetails['total_10'], total_24 = taxDetails['total_24'], total_80tta = taxDetails['total_80tta'],
                        rate80c = round(taxDetails['total_80c'] / MAX_80C * 100, 2), rate80d = round(taxDetails['total_80d'] / MAX_80D_BOTH * 100, 2), rate80e = round(taxDetails['total_80e'] / MAX_80E * 100, 2), rate80ccd1 = round(taxDetails['total_80ccd1'] / MAX_80CCD1 * 100, 2), rate80ccd2 = round(taxDetails['total_80ccd2'] / MAX_80CCD2 * 100, 2), rate24 = round(taxDetails['total_24'] / MAX_24 * 100, 2), 
                        )

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
    salary_details['basic_pay'] = request.form.get("basic_pay", default = 0, type = int) * 12
    salary_details['hra_allowance'] = request.form.get("hra_allowance", default = 0, type = int) * 12
    salary_details['hra_city_type'] = request.form.get("hra_city_type", type = str)
    salary_details['lta_allowance'] = request.form.get("lta_allowance", default = 0, type = int) * 12
    salary_details['meal_allowance'] = request.form.get("meal_allowance", default = 0, type = int) * 12
    salary_details['fuel_allowance'] = request.form.get("fuel_allowance", default = 0, type = int) * 12
    salary_details['cab_allowance'] = request.form.get("cab_allowance", default = 0, type = int) * 12
    salary_details['internet_allowance'] = request.form.get("internet_allowance", default = 0, type = int) * 12
    salary_details['special_allowance'] = request.form.get("special_allowance", default = 0, type = int) * 12
    salary_details['other_allowance'] = request.form.get("other_allowance", default = 0, type = int) * 12
    salary_details['taxable_allowance'] = request.form.get("taxable_allowance", default = 0, type = int) * 12
    
    return salary_details
# end getSalaryDetails

def getInvestmentDetails(request):
    investment_details = {}
    investment_details['80c_insurance_paid'] = request.form.get("80c_insurance_paid", default = 0, type = int)
    investment_details['80d_insurance_paid'] = request.form.get("80d_insurance_paid", default = 0, type = int)
    investment_details['80d_insurance_paid_type'] = request.form.get("80d_insurance_paid", type = str)
    investment_details['ppf_paid'] = request.form.get("ppf_paid", default = 0, type = int) * 12
    investment_details['vpf_paid'] = request.form.get("vpf_paid", default = 0, type = int) * 12
    investment_details['rent_paid'] = request.form.get("rent_paid", default = 0, type = int) * 12
    investment_details['rent_received'] = request.form.get("rent_received", default = 0, type = int) * 12
    investment_details['home_loan_principal'] = request.form.get("home_loan_principal", default = 0, type = int)
    investment_details['home_loan_interest'] = request.form.get("home_loan_interest", default = 0, type = int)
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
    taxDetails = {}

    sum_80c = 0
    sum_80d = 0

    sum_Income_Salary = getIncomeFromSalary(details['salary'])

    sum_80c = get80cDetails(details['investments'], details['salary']['basic_pay'])
    sum_80d = get80dDetails(details['investments'])
    sum_10 = get10Details(details) # Rental
    sum_24 = get24Details(details['investments']) # Income From Other Sources
    sum_80tta = get80ttaDetails(details['investments'])
    sum_80ccd1 = get80ccd1Details(details['investments'])
    sum_80ccd2 = get80ccd2Details(details['investments'])
    sum_80e = get80eDetails(details['investments'])
    sum_Prof_Tax = MAX_PROFESSIONAL_TAX

    taxDetails['incomeFromSalary'] = sum_Income_Salary
    taxDetails['total_10'] = sum_10
    taxDetails['total_24'] = sum_24
    taxDetails['total_80c'] = sum_80c
    taxDetails['total_80d'] = sum_80d
    taxDetails['total_80ccd1'] = sum_80ccd1
    taxDetails['total_80ccd2'] = sum_80ccd2
    taxDetails['total_80e'] = sum_80e
    taxDetails['total_80tta'] = sum_80tta
    taxDetails['total_profTaxReimbursed'] = sum_Prof_Tax
    taxDetails['grossIncome'] = taxDetails['incomeFromSalary']
    taxDetails['totalDeductions'] = STANDARD_DEDUCTION + taxDetails['total_10'] + taxDetails['total_profTaxReimbursed'] + taxDetails['total_24'] + taxDetails['total_80c'] + taxDetails['total_80d'] + taxDetails['total_80tta'] + taxDetails['total_80ccd1'] + taxDetails['total_80ccd2'] + taxDetails['total_80e']

    taxDetails['totalIncomeAfterDeductions'] = taxDetails['grossIncome'] - taxDetails['totalDeductions']
    
    taxOld = computeTaxPayableOldRegime(taxDetails['grossIncome'] - taxDetails['totalDeductions'])
    taxDetails['taxPayableOld'] = taxOld + (taxOld * EDUCATION_CESS_PER // 100)
    
    taxNew = computeTaxPayableNewRegime(taxDetails['grossIncome'])
    taxDetails['taxPayableNew'] = taxNew + (taxNew * EDUCATION_CESS_PER // 100)

    taxDetails['taxPayablePerMonth'] = taxDetails['taxPayableOld'] // 12
    taxDetails['netIncome'] = taxDetails['grossIncome'] - taxDetails['taxPayableOld']
    taxDetails['taxExempted'] = getTaxExemptedIncome(details['salary'])

    return taxDetails
# end taxDetails

def getIncomeFromSalary(salaryDetails):    
    sum_Income = salaryDetails['basic_pay'] + salaryDetails['taxable_allowance'] + salaryDetails['hra_allowance']

    return sum_Income
# end getIncomeFromSalary

def getTaxExemptedIncome(salaryDetails):
    return salaryDetails['cab_allowance'] + salaryDetails['fuel_allowance'] + salaryDetails['internet_allowance'] + salaryDetails['meal_allowance'] + salaryDetails['special_allowance'] + salaryDetails['other_allowance']
# end getTaxExemptedIncome

def computeTaxPayableOldRegime(taxPayableAmount):
    tax = 0
    taxAmount = taxPayableAmount

    if (taxAmount > (TAX_SLAB_50 - TAX_SLAB_25)):
        taxAmount -= (TAX_SLAB_50 - TAX_SLAB_25)
        tax += TAX_SLAB_25 * TAX_ABOVE_2_5_TO_5_0_OLD_PER // 100
    
    if (taxAmount > (TAX_SLAB_75 - TAX_SLAB_50)):
        taxAmount -= (TAX_SLAB_75 - TAX_SLAB_50)
        tax += TAX_SLAB_25 * TAX_ABOVE_5_0_TO_7_5_OLD_PER // 100

    if (taxAmount > (TAX_SLAB_100 - TAX_SLAB_75)):
        taxAmount -= (TAX_SLAB_100 - TAX_SLAB_75)
        tax += TAX_SLAB_25 * TAX_ABOVE_7_5_TO_10_0_OLD_PER // 100

    if (taxAmount > (TAX_SLAB_125 - TAX_SLAB_100)):
        taxAmount -= (TAX_SLAB_125 - TAX_SLAB_100)
        tax += TAX_SLAB_25 * TAX_ABOVE_10_0_TO_12_5_OLD_PER // 100

    if (taxAmount > (TAX_SLAB_150 - TAX_SLAB_125)):
        taxAmount -= (TAX_SLAB_150 - TAX_SLAB_125)
        tax += TAX_SLAB_25 * TAX_ABOVE_12_5_TO_15_0_OLD_PER // 100
    
    if (taxAmount > TAX_SLAB_150):
        tax += taxAmount * TAX_ABOVE_15_0_OLD_PER // 100

    return tax
# end computeTaxPayableOldRegime

def computeTaxPayableNewRegime(taxPayableAmount):
    tax = 0
    taxAmount = taxPayableAmount

    if (taxAmount > (TAX_SLAB_50 - TAX_SLAB_25)):
        taxAmount -= (TAX_SLAB_50 - TAX_SLAB_25)
        tax += TAX_SLAB_25 * TAX_ABOVE_2_5_TO_5_0_NEW_PER // 100
    
    if (taxAmount > (TAX_SLAB_75 - TAX_SLAB_50)):
        taxAmount -= (TAX_SLAB_75 - TAX_SLAB_50)
        tax += TAX_SLAB_25 * TAX_ABOVE_5_0_TO_7_5_NEW_PER // 100

    if (taxAmount > (TAX_SLAB_100 - TAX_SLAB_75)):
        taxAmount -= (TAX_SLAB_100 - TAX_SLAB_75)
        tax += TAX_SLAB_25 * TAX_ABOVE_7_5_TO_10_0_NEW_PER // 100

    if (taxAmount > (TAX_SLAB_125 - TAX_SLAB_100)):
        taxAmount -= (TAX_SLAB_125 - TAX_SLAB_100)
        tax += TAX_SLAB_25 * TAX_ABOVE_10_0_TO_12_5_NEW_PER // 100

    if (taxAmount > (TAX_SLAB_150 - TAX_SLAB_125)):
        taxAmount -= (TAX_SLAB_150 - TAX_SLAB_125)
        tax += TAX_SLAB_25 * TAX_ABOVE_12_5_TO_15_0_NEW_PER // 100
    
    if (taxAmount > TAX_SLAB_150):
        tax += taxAmount * TAX_ABOVE_15_0_NEW_PER // 100

    return tax
# end computeTaxPayableNewRegime


def get80ccd1Details(investmentDetails):
    return investmentDetails['employee_nps_paid']
# end get80ccd1Details

def get80ccd2Details(investmentDetails):
    return investmentDetails['employer_nps_paid']
# end get80ccd2Details

def get80eDetails(investmentDetails):
    return investmentDetails['education_loan_interest']
# end get80eeDetails

def get24Details(investmentDetails):
    house_Repairs = (investmentDetails['rent_received'] * HOUSE_REPAIRS_PER) // 100
    sum_24 = investmentDetails['home_loan_interest'] + investmentDetails['house_tax'] + house_Repairs - investmentDetails['rent_received'] 

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
    
    hra_Calc += min(hra_Allowable, details['investments']['rent_paid'], (details['investments']['rent_paid'] - (10 * details['salary']['basic_pay'] // 100)))
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
