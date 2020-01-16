# Leopharma Open Innovation - Hackathon Event
## Using AI to find new drug targets for eczema

This eczema hackathon was a 2-day research sprint where teams of 3-4 persons explored academic literature and mapped out potential solutions to identify new targets and pathways for treating atopic dermatitis/eczema using Artificial Intelligence (AI).

More information at:<br>
http://openinnovation.leo-pharma.com/Take-part/Scithon-event.aspx

Our approach:<br>
Based on the known targets for Eczema provived by LeoPharma, we use the Open Targets REST API (https://www.targetvalidation.org/) to find diseases associated with these targets in the literature. Then we look at other targets available for these diseases in the literature as potential candidates for Eczema. The hypothesis is that we find targets for eczema within targets that work for related diseases. Diseases are also ranked by their association score (given by Open Targets) to find the most similar diseases and by extension the most relevant targets. The final list is compared against the scientific literature by hand to filter it further.
