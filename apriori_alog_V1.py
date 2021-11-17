##########################################################################
## Author Name   ::
## Description  ::
## Created on   ::
## Modules to be installed
## Installing any Python modules: pip install <modulename>
## Script Usage ::  python scriptname
## Modules need to be installed : Flask
## If you want to install the packages please uncomment below three lines and install the packages
# pip install Flask
# pip install matplotlib
# pip install numpy
##########################################################################

## Importing the Modules
import itertools
from flask import Flask, flash, redirect, render_template, request, url_for

def generationoffirstCandiadateSet(input_dataset):
    product_values_dict = {}
    result_set = []
    for data in input_dataset:
        for product in data:
            if product not in product_values_dict:
               product_values_dict[product] = 1
            else:
                 product_values_dict[product] = product_values_dict[product] + 1
    for eachkey in product_values_dict:
        temp = []
        temp.append(eachkey)
        result_set.append(temp)
        result_set.append(product_values_dict[eachkey])
        temp = []
    return result_set


def generationOfFrequentItems(candidatelist, no_of_trans, min_supp, input_dataset, father_frequent_list_values):
    frequentitems_values = []
    for i in range(len(candidatelist)):
        if i%2 != 0:
            print(no_of_trans)
            support = (candidatelist[i] * 1.0 / no_of_trans) * 100.0
            if support >= min_supp:
                frequentitems_values.append(candidatelist[i-1])
                frequentitems_values.append(candidatelist[i])
            else:
                eliminated_items_list.append(candidatelist[i-1])

    for k in frequentitems_values:
        father_frequent_list_values.append(k)

    if len(frequentitems_values) == 2 or len(frequentitems_values) == 0:
        return_list = father_frequent_list_values
        return return_list
    else:
        generationCandidateValues(input_dataset, eliminated_items_list, frequentitems_values, no_of_trans, min_supp)

def generationCandidateValues(input_dataset, eliminated_items_list, frequentitems_values, no_of_transactions, min_support):
    unique_elements = []
    list_values_after_combinations = []
    candidate_list_values = []
    for i in range(len(frequentitems_values)):
        if i%2 == 0:
            unique_elements.append(frequentitems_values[i])
    for eachitem in unique_elements:
        temp_combination_values = []
        k = unique_elements.index(eachitem)
        for i in range(k + 1, len(unique_elements)):
            for j in eachitem:
                if j not in temp_combination_values:
                    temp_combination_values.append(j)
            for m in unique_elements[i]:
                if m not in temp_combination_values:
                    temp_combination_values.append(m)
            list_values_after_combinations.append(temp_combination_values)
            temp_combination_values = []
    sorted_combination_values = []
    unique_combination_list = []
    for i in list_values_after_combinations:
        sorted_combination_values.append(sorted(i))
    for i in sorted_combination_values:
        if i not in unique_combination_list:
            unique_combination_list.append(i)
    list_values_after_combinations = unique_combination_list
    for eachitem in list_values_after_combinations:
        count = 0
        for eachtransaction in input_dataset:
            if set(eachitem).issubset(set(eachtransaction)):
                count = count + 1
        if count != 0:
            candidate_list_values.append(eachitem)
            candidate_list_values.append(count)
    generationOfFrequentItems(candidate_list_values, no_of_transactions, min_support, input_dataset, father_frequent_list_values)

def generationAssociationRule(frequentSet):
    associationrule_list = []
    for eachitem in frequentSet:
        if isinstance(eachitem, list):
            if len(eachitem) != 0:
                length = len(eachitem) - 1
                while length > 0:
                    combinations_list = list(itertools.combinations(eachitem, length))
                    tempvalue = []
                    LHS = []
                    for RHS in combinations_list:
                        LHS = set(eachitem) - set(RHS)
                        tempvalue.append(list(LHS))
                        tempvalue.append(list(RHS))
                        associationrule_list.append(tempvalue)
                        tempvalue = []
                    length = length - 1
    return associationrule_list

def AprioriOutput(rules, input_dataset, min_support, min_con,no_of_transactions):
    apriori_output = []
    for eachrule in rules:
        supportOfX = 0
        supportOfXinPercentage = 0
        supportOfXandY = 0
        supportOfXandYinPercentage = 0
        for eachtransaction in input_dataset:
            if set(eachrule[0]).issubset(set(eachtransaction)):
                supportOfX = supportOfX + 1
            if set(eachrule[0] + eachrule[1]).issubset(set(eachtransaction)):
                supportOfXandY = supportOfXandY + 1
        try:
            supportOfXinPercentage = (supportOfX * 1/ no_of_transactions) * 100
        except ZeroDivisionError:
            supportOfXinPercentage = 0
        try:
            supportOfXandYinPercentage = (supportOfXandY * 1 / no_of_transactions) * 100
        except ZeroDivisionError:
            supportOfXandYinPercentage = 0
        try:
            confidence = (supportOfXandYinPercentage / supportOfXinPercentage) * 100
        except ZeroDivisionError:
            confidence = 0
        if confidence >= min_con:
            supportOfXAppendString = "Support Of X: " + str(round(supportOfXinPercentage, 2))
            supportOfXandYAppendString = "Support of X & Y: " + str(round(supportOfXandYinPercentage))
            confidenceAppendString = "Confidence: " + str(round(confidence))
            apriori_output.append(supportOfXAppendString)
            apriori_output.append(supportOfXandYAppendString)
            apriori_output.append(confidenceAppendString)
            apriori_output.append(eachrule)
    return apriori_output


def main():
    ### Flask Programming ####
    app = Flask(__name__)
    @app.route('/')
    def index():
        return render_template('index.html',inputdata=[{'name': '1000-out1.csv'}, {'name': '5000-out1.csv'}, {'name': '20000-out1.csv'}, {'name': '75000-out1.csv'}])

    @app.route("/result", methods=['GET', 'POST'])
    def output():
        file_name = request.form.get('comp_select')
        min_sup = request.form.get('minimum_value')
        min_conf = request.form.get('minimum_conf')

        filename = 'data/'+file_name
        with open(filename, 'r') as fp:
            lines = fp.readlines()

        for line in lines:
            line = line.rstrip()
            input_dataset.append(line.split(","))

        no_of_trans = len(input_dataset)
        first_candidate_set = generationoffirstCandiadateSet(input_dataset)
        frequent_item_set = generationOfFrequentItems(first_candidate_set, no_of_trans, int(min_sup), input_dataset,
                                                      father_frequent_list_values)
        association_rules = generationAssociationRule(father_frequent_list_values)
        apriori_result = AprioriOutput(association_rules, input_dataset, int(min_sup), int(min_conf), no_of_trans)
        result_data = []
        c = 1
        if len(apriori_result) == 0:
            print("There are no association rules for this support and confidence.")
        else:
            for i in apriori_result:
                if c == 4:
                    ddd = str(i[0]) + "------>" + str(i[1])
                    result_data.append(ddd)
                    result_data.append("---------------------------")
                    print("")
                    c = 0
                else:
                    result_data.append(str(i))
                c = c + 1
        return render_template('result.html', output=result_data)
    app.run(host='localhost', port=8082, debug=False)

if __name__ == '__main__':
    input_dataset = []
    eliminated_items_list = []
    no_of_trans = 0
    father_frequent_list_values = []
    main()