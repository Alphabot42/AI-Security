# V1 publication status

Q14_04_QA01 is complete for the frozen R2 reproduction scope.
Q14_04_JAL01 is complete for publication of the reviewed V1 study and its
reproducible frozen-inference artifacts.

| Deliverable | Status |
|---|---|
| English report and diagrams | Published in the reviewed versions |
| Source code and public notebook copies | Published with provenance |
| Demonstration | Executed five-case saved-evidence demonstration |
| Frozen R2 model package | Published as individual files in models/quishing_v1 |
| Verification fixtures and exact split | Included |
| Complete lab verification results | Included in evidence/quishing_v1/lab |
| Independent artifact review | Passed; 4,106 transfer files and original/exported model states checked |
| Independent complete replay | Passed; 21,723 image results matched exactly, plus 755 URL pairs per model |
| Final V1 publication milestone | Complete for the documented V1 scope |

The original verification used Python 3.11.15. The independent review used an
isolated Python 3.12.14 environment with the same pinned dependency versions.
No model was refitted, threshold recalibrated or measured result upgraded.
The stronger blur condition retains its documented decoder availability failure.

The raw source dataset remains available from its authors. Included fixtures
are attributed adaptations under the authors' CC BY 4.0 license. V2 external-data
work and application deployment are separate phases.
