from opentargets import OpenTargetsClient
import operator
from tqdm import tqdm

ot = OpenTargetsClient()

# search for all targets associated with the given disease
eczema_targets = ot.get_associations_for_disease('EFO_0000274') # atopic eczema
print("Found " + str(len(eczema_targets)) + " possible associations")

target_by_id_dict = {}
for target in eczema_targets:
        target_by_id_dict[target["target"]["id"]] = target

# known atopic dermatitis/eczema (AD) targets provided by Leo Pharma. NOTE: replaced by random exampes, real data omitted for reasons of confidentiality
known_targets = ["ENSG00000267816", "ENSG00000010404", "ENSG00000104823"]

# find related diseases
diseaseDict = {}  # disease id - total association score
for target_id in tqdm(known_targets):
    print("Getting know diseases for target " + target_id)
    for acc_target in ot.get_associations_for_target(target_id):
        if acc_target["disease"]["id"] is not "other":
            if acc_target["disease"]["id"] not in diseaseDict:
                diseaseDict[acc_target["disease"]["id"]] = 0
            diseaseDict[acc_target["disease"]["id"]] += acc_target["association_score"]["overall"]
print("Found " + str(len(diseaseDict.keys())) + " related diseases")

# sort diseases according to relevance
disease_array = sorted(diseaseDict.items(), key=operator.itemgetter(1))
disease_array.reverse()  # sort in order of descending relevance

# find potential targets
second_target_dict = {}
diseases_process = 0;
for disease in disease_array:
    disease_id = disease[0]
    print("Getting targets for disease " + disease_id + " (" + str(disease[1]) + ")")
    diseases_process = diseases_process + 1
    if diseases_process > 50:
        break
    secondlevel_targets = ot.get_associations_for_disease(str(disease_id))
    for second_target in secondlevel_targets:
        if second_target["target"]["id"] not in second_target_dict:
            second_target_dict[second_target["target"]["id"]] = 0
        second_target_dict[second_target["target"]["id"]] = \
            second_target_dict[second_target["target"]["id"]] + second_target["association_score"]["overall"]

potential_targets = sorted(second_target_dict.items(), key=operator.itemgetter(1))
potential_targets.reverse()
potential_targets_filtered = \
    [i for i in potential_targets if (i[0] in target_by_id_dict.keys() and \
    target_by_id_dict[i[0]]["association_score"]["datatypes"]["literature"] < 0.02 \
    and target_by_id_dict[i[0]]["association_score"]["overall"] > 0.005)]

# print potential targets (minus the targets already known)
tuples_printed = 0
for target_tuple in potential_targets_filtered:
    if target_tuple[0] not in known_targets:
        tuples_printed = tuples_printed +1
        if tuples_printed > 500:
            break
        print(target_tuple[0] + "|" + str(target_tuple[1]) + "|" + \
              (target_by_id_dict[target_tuple[0]]["target"]["gene_info"]["symbol"] + \
                "|" + target_by_id_dict[target_tuple[0]]["target"]["gene_info"]["name"] + \
                "|" + str(target_by_id_dict[target_tuple[0]]["association_score"]["overall"]) + "|" + \
                str(target_by_id_dict[target_tuple[0]]["association_score"]["datatypes"]["literature"]) \
               if target_tuple[0] in target_by_id_dict else "|"))
