from opentargets import OpenTargetsClient
import operator
ot = OpenTargetsClient()

# search for all targets associated with the given disease
eczema_targets = ot.get_associations_for_disease('EFO_0000274') # atopic eczema
print "Found " + str(len(eczema_targets)) + " possible associations"

target_by_id_dict = {}
for target in eczema_targets:
        target_by_id_dict[target["target"]["id"]] = target

# known AD targets provided by Leo Pharma
known_targets = ["ENSG00000178394", "ENSG00000135914", "ENSG00000043591", "ENSG00000106546", "ENSG00000088832", \
                 "ENSG00000118432", "ENSG00000163823", "ENSG00000005844", "ENSG00000092009", "ENSG00000073756", \
                 "ENSG00000007908", "ENSG00000131981", "ENSG00000107485", "ENSG00000113580", "ENSG00000196639", \
                 "ENSG00000113749", "ENSG00000134489", "ENSG00000106348", "ENSG00000027697", "ENSG00000113302", \
                 "ENSG00000169194", "ENSG00000124391", "ENSG00000112115", "ENSG00000127318", "ENSG00000164509", \
                 "ENSG00000137033", "ENSG00000077238", "ENSG00000113525", "ENSG00000162434", "ENSG00000082556", \
                 "ENSG00000025434", "ENSG00000115353", "ENSG00000197561", "ENSG00000007171", "ENSG00000116329", \
                 "ENSG00000186827", "ENSG00000065989", "ENSG00000169403", "ENSG00000168229", "ENSG00000131759", \
                 "ENSG00000145777", "ENSG00000232810", "ENSG00000137462", "ENSG00000136869", "ENSG00000239732", \
                 "ENSG00000198400", "ENSG00000196689", "ENSG00000111424", "ENSG00000169252", "ENSG00000196262", \
                 "ENSG00000188822", "ENSG00000160255", "ENSG00000095303", "ENSG00000188404", "ENSG00000178035", \
                 "ENSG00000159128", "ENSG00000105639", "ENSG00000131408", "ENSG00000082556", "ENSG00000117586", \
                 "ENSG00000184588", "ENSG00000183134", "ENSG00000077092", "ENSG00000067182", "ENSG00000188778", \
                 "ENSG00000174175", "ENSG00000105397", "ENSG00000112038", "ENSG00000105650", "ENSG00000172819", \
                 "ENSG00000028137", "ENSG00000153246", "ENSG00000069764", "ENSG00000100078", "ENSG00000123739", \
                 "ENSG00000138308", "ENSG00000188257", "ENSG00000117215", "ENSG00000158786", "ENSG00000188784", \
                 "ENSG00000167525", "ENSG00000170989", "ENSG00000267534", "ENSG00000213694", "ENSG00000180739", \
                 "ENSG00000125910", "ENSG00000198121", "ENSG00000064547", "ENSG00000171517", "ENSG00000171608"]

# find related diseases
diseaseDict = {}
for target_id in known_targets:
    print "Getting know diseases for target " + target_id
    for acc_target in ot.get_associations_for_target(target_id):
        if acc_target["disease"]["id"] is not "other":
            if acc_target["disease"]["id"] not in diseaseDict:
                diseaseDict[acc_target["disease"]["id"]] = 0
            diseaseDict[acc_target["disease"]["id"]] += acc_target["association_score"]["overall"]
print "Found " + str(len(diseaseDict.keys())) + " related diseases"

# sort diseases according to relevance
disease_array = sorted(diseaseDict.items(), key=operator.itemgetter(1))
disease_array.reverse()

# find potential targets
second_target_dict = {}
diseases_process = 0;
for disease in disease_array:
    disease_id = disease[0]
    print "Getting targets for disease " + disease_id + " (" + str(disease[1]) + ")"
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
        print target_tuple[0] + "|" + str(target_tuple[1]) + "|" + \
              (target_by_id_dict[target_tuple[0]]["target"]["gene_info"]["symbol"] + \
                "|" + target_by_id_dict[target_tuple[0]]["target"]["gene_info"]["name"] + \
                "|" + str(target_by_id_dict[target_tuple[0]]["association_score"]["overall"]) + "|" + \
                str(target_by_id_dict[target_tuple[0]]["association_score"]["datatypes"]["literature"]) \
               if target_tuple[0] in target_by_id_dict else "|")
