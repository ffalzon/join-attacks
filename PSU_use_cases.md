# Usage of PSU

## In Relation to General Data Join Mechanisms

1. **Privacy-Preserving Distributed Mining of Association Rules on Horizontally Partitioned Data** ([IEEE transactions on knowledge and data engineering, 2004](https://doi.org/10.1109/TKDE.2004.45))

   * Compute union of **encrypted** $k$-itemsets. However, knowing which encrypted itemset stems from which party is still undesirable:

     > [...] if a site knows which fully encrypted itemsets come from which sites, it can compute the size of the intersection between any set of sites. While generally innocuous, if it has this information for itself, it can guess at the itemsets supported by other sites.


   * The authors claim semi-honest security and mention that there must be $\geq 3$ parties; Our attack can therefore only recover the union of all honest parties' inputs (assuming the input-malicious parties collude).


   * Some additional leakage, which the authors deem acceptable.

2. **Secret-Shared Joins with Multiplicity from Aggregation Trees** [CCS'22](https://doi.org/10.1145/3548606.3560670)

   * Core protocol only computes inner-joins (intersections), but can be extended to full unions

   * Arbitrary SQL-like queries **over secret shared data**
   * Our PSU attack should apply at least if only the union is computed(plausible in some cases), i.e.,
     1. Secret-share data
     2. Compute union
     3. Reconstruct data

3. **Fast Database Joins and PSI for Secret Shared Data** [CCS'20](https://doi.org/10.1145/3372297.3423358)

   * More inefficient predecessor of 2. which additionally assumes that keys are unique (only one-to-one matches) 
   * They outline (and implement) two concrete applications (Both are more envision more than two parties): 
     * Detect inconsistencies in US voter registration databases (e.g. multiple registrations per person in different states)
     * Threat Log Comparison: Compute union of security events (e.g. IP addresses making suspicious requests). Extension to only reveal an event if it occurred in $k$ out of $n$ networks are possible.  


## Other Usages

1. **A Model for Secure and Mutually Beneficial Software Vulnerability Sharing** ([WISC'16](https://dl.acm.org/doi/abs/10.1145/2994539.2994547))
   * PSU-like functionality: "Mediator". Not exactly but the PSU attack may carry over (partially)

2. **Secure Multiparty Computation for Cooperative Cyber Risk Assessment** [SecDev'16](https://doi.org/10.1109/SecDev.2016.028)
   * Talk, so no concrete writeup. Recording: unknown, check again.
   * Two applications of MPC for  cooperative cyber risk assessment:
     1. Threshold-PSU for IP blacklist aggregation (more than two parties)
     2. PSI-SUM-like functionality to aggregate vulnerability data

Other applications such as **aggregating medical data** or **anomaly detection in network monitoring** are mentioned without references to further papers or concrete pointers where this is used (specific companies, agencies, products, ...) 
