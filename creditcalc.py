import math
import argparse

menu = '''What do you want to calculate?
type "n" for number of monthly payments,
type "a" for annuity monthly payment amount,
type "p" for loan principal,
type "d" for different monthly payment amount: '''

parser = argparse.ArgumentParser(description='This program can calculate the loan payments and its term.'
                                             ' Use the "types" from the user menu.')
parser.add_argument('--type', choices=['annuity', 'diff'])
parser.add_argument('--payment')
parser.add_argument('--principal')
parser.add_argument('--periods')
parser.add_argument('--interest')

args = parser.parse_args()


def loan_principal(annuity_payment, number_periods, loan_interest):
    i = loan_interest / (12 * 100)
    p = annuity_payment / ((i * pow((1 + i), number_periods)) /
                           (pow((1 + i), number_periods) - 1))
    print(f'Your loan principal = {math.floor(p)}!')
    print(f'Overpayment = {math.ceil((annuity_payment * number_periods) - p)}')


def monthly_payments(principal, monthly_payment, loan_interest):
    i = loan_interest / (12 * 100)
    n = math.ceil(math.log((monthly_payment / (monthly_payment - i * principal)), 1 + i))
    if n // 12 == 0:
        print(f"It will take {n % 12} {'months' if n % 12 > 1 else 'month'} to repay this loan!")
    elif {n % 12} == 0:
        print(f"It will take {n // 12} {'years' if n // 12 > 1 else 'year'} to repay this loan!")
    else:
        print(f'It will take {n // 12} years and {n % 12} months to repay this loan!')
    print(f'Overpayment = {int((monthly_payment * n) - principal)}')


def _annuity_payment(principal, number_periods, loan_interest):
    i = loan_interest / (12 * 100)
    a = principal * ((i * pow((1 + i), number_periods)) / (pow((1 + i), number_periods) - 1))
    print(f'Your monthly payment = {math.ceil(a)}!')
    print(f'Overpayment = {int((math.ceil(a) * number_periods) - principal)}')


def differentiate_payments(principal, loan_interest, number_periods):
    i = loan_interest / (12 * 100)
    overall_sum = 0
    for m in range(1, number_periods + 1):
        differentiated_payment = principal / number_periods + i * (principal - (principal * (m - 1) / number_periods))
        overall_sum += math.ceil(differentiated_payment)
        print(f'Month {m}: payment is {math.ceil(differentiated_payment)}')
    print()
    print(f'Overpayment = {int(overall_sum - principal)}')


def calculator(letter):
    if letter == 'n':
        principal = float(input('Enter the loan principal: '))
        monthly_payment = float(input('Enter the monthly payment: '))
        loan_interest = float(input('Enter the loan interest: '))
        monthly_payments(principal, monthly_payment, loan_interest)
    elif letter == 'a':
        principal = float(input('Enter the loan principal: '))
        number_periods = int(input('Enter the number of periods: '))
        loan_interest = float(input('Enter the loan interest: '))
        _annuity_payment(principal, number_periods, loan_interest)
    elif letter == 'p':
        annuity_payment = float(input('Enter the annuity payment: '))
        number_periods = int(input('Enter the number of periods: '))
        loan_interest = float(input('Enter the loan interest: '))
        loan_principal(annuity_payment, number_periods, loan_interest)
    elif letter == 'd':
        principal = float(input('Enter the loan principal: '))
        loan_interest = float(input('Enter the loan interest: '))
        number_periods = int(input('Enter the number of periods: '))
        differentiate_payments(principal, loan_interest, number_periods)


while True:
    if args.type == 'diff' and args.payment is not None:
        print('Incorrect parameters')
        break
    if args.interest is None:
        print('Incorrect parameters')
        break
    args.list = [args.type, args.payment, args.principal, args.periods, args.interest]
    new_args = []
    for elem in args.list:
        if elem is not None:
            new_args.append(elem)
        continue
    if len(new_args) != 4:
        print('Incorrect parameters')
        break
    if args.list[0] == 'diff':
        differentiate_payments(float(args.principal), float(args.interest), int(args.periods))
        break
    else:
        if args.payment is None:
            _annuity_payment(float(args.principal), int(args.periods), float(args.interest))
            break
        if args.principal is None:
            loan_principal(float(args.payment), int(args.periods), float(args.interest))
            break
        monthly_payments(float(args.principal), float(args.payment), float(args.interest))
        break

calculator(input(menu))