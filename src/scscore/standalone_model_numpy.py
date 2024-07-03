'''
This is a standalone, importable SCScorer model. It does not have tensorflow as a
dependency and is a more attractive option for deployment. The calculations are
fast enough that there is no real reason to use GPUs (via tf) instead of CPUs (via np)
'''
import math
import numpy as np
import rdkit.Chem as Chem
import rdkit.Chem.AllChem as AllChem
import json
import gzip
import os

project_root = os.path.dirname(os.path.dirname(__file__))

class SCScorer():
    def __init__(self, score_scale=5.0, FP_len=1024, FP_rad=2):
        self.score_scale = score_scale
        self.FP_len = FP_len
        self.FP_rad = FP_rad
        self.vars = []
        self._restored = False
        self.mol_to_fp = None
        self.restore()

    def restore(self, weight_path=None):
        if weight_path is None:
            weight_path = os.path.join(project_root, 'scscore', 'models', 'full_reaxys_model_1024bool', 'model.ckpt-10654.as_numpy.json.gz')
        self._load_vars(weight_path)
        self._setup_mol_to_fp_function()
        self._restored = True

    def _setup_mol_to_fp_function(self):
        if self.vars[0].dtype == np.uint8:
            self.mol_to_fp = self._mol_to_fp_counts
        else:
            self.mol_to_fp = self._mol_to_fp_bits

    def _mol_to_fp_counts(self, mol):
        if mol is None:
            return np.zeros((self.FP_len,), dtype=np.uint8)
        fp = AllChem.GetMorganFingerprint(mol, self.FP_rad, useChirality=True)
        fp_folded = np.zeros((self.FP_len,), dtype=np.uint8)
        for k, v in fp.GetNonzeroElements().items():
            fp_folded[k % self.FP_len] += v
        return fp_folded

    def _mol_to_fp_bits(self, mol):
        if mol is None:
            return np.zeros((self.FP_len,), dtype=bool)
        return np.array(AllChem.GetMorganFingerprintAsBitVect(mol, self.FP_rad, nBits=self.FP_len, useChirality=True), dtype=bool)

    def smi_to_fp(self, smi):
        mol = Chem.MolFromSmiles(smi)
        return self.mol_to_fp(mol) if mol else np.zeros((self.FP_len,), dtype=self.vars[0].dtype)

    def apply(self, x):
        if not self._restored:
            raise ValueError('Model weights not restored!')
        for i in range(0, len(self.vars), 2):
            x = np.dot(x, self.vars[i]) + self.vars[i + 1]
            if i < len(self.vars) - 2:  # ReLU for hidden layers
                x = np.maximum(0, x)
        # Ensure the final layer uses sigmoid and returns a scalar
        x = 1 + (self.score_scale - 1) * (1 / (1 + np.exp(-x)))  # Sigmoid for output layer
        return x[0]  # Ensure we return a scalar value from apply

    def get_score_from_smi(self, smi):
        if not smi:
            return ('', 0.0)
        fp = self.smi_to_fp(smi)
        score = self.apply(fp) if np.any(fp) else 0.0
        return (Chem.MolToSmiles(Chem.MolFromSmiles(smi), isomericSmiles=True) if smi else '', float(score))

    def _load_vars(self, weight_path):
        with gzip.GzipFile(weight_path, 'r') as fin:
            self.vars = [np.array(x) for x in json.loads(fin.read().decode('utf-8'))]

if __name__ == '__main__':
    scorer = SCScorer()
    smis = ['CCCOCCC', 'CCCNc1ccccc1']
    scores = [scorer.get_score_from_smi(smi) for smi in smis]
    for smi, score in scores:
        print(f'{score:.4f} <--- {smi}')

