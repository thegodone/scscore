# scscore (Standalone version only)

### Description
Forked version of the SCScore repository (check below for original work and reference). This is a pip installable standalone version. The model is automatically loaded in silent mode when imported for easier use.

SCScore model assigns a synthetic complexity score between 1 and 5 to a molecule. The score is based on the premise that published reactions, overall, should exhibit an increase in synthetic complexity. The model has been trained on 12M reactions from Reaxys.

### Usage
``` console
pip install -e .
```

``` python
from scscore import SCScorer
scs_scorer = SCScorer()
scs_scorer.get_score_from_smi('CCCC(=O)CCCCO')
```

### Dependencies if you want to use the final model
- RDKit (most versions should be fine)
- numpy

### Dpendencies if you want to retrain on your own data
- RDKit (most versions should be fine)
- tensorflow (r0.12.0)
- h5py
- numpy



## Original work

Publication: [SCScore: Synthetic Complexity Learned from a Reaction Corpus](https://pubs.acs.org/doi/10.1021/acs.jcim.7b00622)

GitHub repository: [SCScore](https://github.com/connorcoley/scscore)

``` bash
@article{coley_scscore_2018,
	title = {{SCScore}: {Synthetic} {Complexity} {Learned} from a {Reaction} {Corpus}},
	author = {Coley, Connor W. and Rogers, Luke and Green, William H. and Jensen, Klavs F.},
	volume = {58},
	issn = {1549-9596},
	shorttitle = {{SCScore}},
	url = {https://doi.org/10.1021/acs.jcim.7b00622},
	doi = {10.1021/acs.jcim.7b00622},
	number = {2},
	urldate = {2022-09-02},
	journal = {Journal of Chemical Information and Modeling},
	month = feb,
	year = {2018},
	note = {Publisher: American Chemical Society},
	pages = {252--261},
}
```