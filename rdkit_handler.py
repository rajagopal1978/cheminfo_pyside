"""
RDKit Handler - Local RDKit Processing
Replaces Django API calls with direct RDKit computations
"""

from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem, Draw, Lipinski
from rdkit.Chem import rdMolDescriptors, DataStructs
from rdkit.Chem.Draw import rdMolDraw2D
import base64
from io import BytesIO


class RDKitHandler:
    """Handle all RDKit operations locally without API calls"""

    @staticmethod
    def parse_molecule(smiles):
        """
        Parse SMILES and return molecular properties

        Args:
            smiles (str): SMILES notation

        Returns:
            dict: Molecular properties
        """
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                raise ValueError("Invalid SMILES string")

            # Calculate properties
            return {
                'valid': True,
                'smiles': smiles,
                'canonical_smiles': Chem.MolToSmiles(mol),
                'formula': rdMolDescriptors.CalcMolFormula(mol),
                'molecular_weight': Descriptors.MolWt(mol),
                'atom_count': mol.GetNumAtoms(),
                'bond_count': mol.GetNumBonds(),
                'ring_count': Descriptors.RingCount(mol),
                'aromatic_rings': Descriptors.NumAromaticRings(mol),
                'rotatable_bonds': Descriptors.NumRotatableBonds(mol),
                'h_bond_donors': Descriptors.NumHDonors(mol),
                'h_bond_acceptors': Descriptors.NumHAcceptors(mol),
                'logp': Descriptors.MolLogP(mol),
                'tpsa': Descriptors.TPSA(mol),
            }
        except Exception as e:
            return {'valid': False, 'error': str(e)}

    @staticmethod
    def generate_2d_image(smiles, width=600, height=400):
        """
        Generate 2D molecular structure image

        Args:
            smiles (str): SMILES notation
            width (int): Image width
            height (int): Image height

        Returns:
            str: Base64 encoded PNG image
        """
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                raise ValueError("Invalid SMILES string")

            # Generate 2D coordinates
            AllChem.Compute2DCoords(mol)

            # Draw molecule
            drawer = rdMolDraw2D.MolDraw2DCairo(width, height)
            drawer.DrawMolecule(mol)
            drawer.FinishDrawing()

            # Convert to base64
            img_data = drawer.GetDrawingText()
            base64_img = base64.b64encode(img_data).decode()

            return f"data:image/png;base64,{base64_img}"

        except Exception as e:
            raise ValueError(f"Failed to generate image: {str(e)}")

    @staticmethod
    def generate_fingerprint(smiles, fp_type='morgan'):
        """
        Generate molecular fingerprint

        Args:
            smiles (str): SMILES notation
            fp_type (str): Fingerprint type (morgan, rdkit, atompair, torsion, maccs)

        Returns:
            dict: Fingerprint data
        """
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                raise ValueError("Invalid SMILES string")

            # Generate fingerprint based on type
            if fp_type == 'morgan':
                fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)
            elif fp_type == 'rdkit':
                fp = Chem.RDKFingerprint(mol)
            elif fp_type == 'atompair':
                fp = rdMolDescriptors.GetHashedAtomPairFingerprintAsBitVect(mol, nBits=2048)
            elif fp_type == 'torsion':
                fp = rdMolDescriptors.GetHashedTopologicalTorsionFingerprintAsBitVect(mol, nBits=2048)
            elif fp_type == 'maccs':
                fp = AllChem.GetMACCSKeysFingerprint(mol)
            else:
                raise ValueError(f"Unknown fingerprint type: {fp_type}")

            # Convert to bit string
            fp_string = fp.ToBitString()

            return {
                'fingerprint': fp_string,
                'type': fp_type,
                'length': len(fp_string),
                'set_bits': fp_string.count('1')
            }

        except Exception as e:
            raise ValueError(f"Failed to generate fingerprint: {str(e)}")

    @staticmethod
    def generate_conformers(smiles, num_conformers=10, max_iters=200):
        """
        Generate 3D conformers for a molecule and return their energies.

        Args:
            smiles (str): SMILES notation
            num_conformers (int): Number of conformers to generate
            max_iters (int): Maximum optimization iterations per conformer

        Returns:
            dict: {'num_conformers': int, 'energies': list[float], 'status': str}
        """
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                raise ValueError("Invalid SMILES string")

            # Add hydrogens and embed 3D coordinates
            mol_h = Chem.AddHs(mol)
            params = None
            if hasattr(AllChem, 'ETKDGv3'):
                params = AllChem.ETKDGv3()
            elif hasattr(AllChem, 'ETKDG'):
                params = AllChem.ETKDG()
            if params is not None:
                try:
                    params.randomSeed = 0xF00D
                except Exception:
                    pass

            conf_ids = AllChem.EmbedMultipleConfs(mol_h, numConfs=num_conformers, params=params)
            if not conf_ids:
                return {'num_conformers': 0, 'energies': [], 'status': 'Embedding failed'}

            energies = []
            # Try MMFF optimization first, fallback to UFF
            try:
                mmff_results = AllChem.MMFFOptimizeMoleculeConfs(mol_h, maxIters=max_iters)
                energies = [float(res[1]) for res in mmff_results]
            except Exception:
                uff_results = AllChem.UFFOptimizeMoleculeConfs(mol_h, maxIters=max_iters)
                energies = [float(res[1]) for res in uff_results]

            return {'num_conformers': len(energies), 'energies': energies, 'status': 'Success'}

        except Exception as e:
            return {'num_conformers': 0, 'energies': [], 'status': f'Error: {str(e)}'}

    @staticmethod
    def calculate_similarity(query_smiles, target_smiles_list, threshold=0.7, fp_type='morgan'):
        """
        Calculate Tanimoto similarity between query and target molecules

        Args:
            query_smiles (str): Query SMILES
            target_smiles_list (list): List of target SMILES
            threshold (float): Similarity threshold
            fp_type (str): Fingerprint type

        Returns:
            list: Similarity results
        """
        try:
            query_mol = Chem.MolFromSmiles(query_smiles)
            if query_mol is None:
                raise ValueError("Invalid query SMILES")

            # Generate query fingerprint
            if fp_type == 'morgan':
                query_fp = AllChem.GetMorganFingerprintAsBitVect(query_mol, 2, nBits=2048)
            else:
                query_fp = Chem.RDKFingerprint(query_mol)

            results = []
            for target_smiles in target_smiles_list:
                target_mol = Chem.MolFromSmiles(target_smiles)
                if target_mol is None:
                    continue

                # Generate target fingerprint
                if fp_type == 'morgan':
                    target_fp = AllChem.GetMorganFingerprintAsBitVect(target_mol, 2, nBits=2048)
                else:
                    target_fp = Chem.RDKFingerprint(target_mol)

                # Calculate Tanimoto similarity
                similarity = DataStructs.TanimotoSimilarity(query_fp, target_fp)

                if similarity >= threshold:
                    results.append({
                        'smiles': target_smiles,
                        'similarity': similarity
                    })

            return results

        except Exception as e:
            raise ValueError(f"Failed to calculate similarity: {str(e)}")

    @staticmethod
    def find_mcs(smiles_list, timeout=10):
        """
        Find maximum common substructure (MCS) for a list of SMILES strings.

        Args:
            smiles_list (list): list of SMILES strings
            timeout (int): maximum time in seconds for the search

        Returns:
            dict: { 'smarts': str, 'smarts_smiles': str, 'num_atoms': int, 'num_bonds': int, 'num_molecules': int, 'status': str }
        """
        try:
            mols = []
            for s in smiles_list:
                if not s:
                    continue
                m = Chem.MolFromSmiles(s)
                if m is not None:
                    mols.append(m)

            if len(mols) < 2:
                return {'smarts': '', 'smarts_smiles': '', 'num_atoms': 0, 'num_bonds': 0, 'num_molecules': len(mols), 'status': 'Need at least two valid molecules'}

            from rdkit.Chem import rdFMCS
            res = rdFMCS.FindMCS(mols, timeout=timeout)
            smarts = res.smartsString or ''
            num_atoms = int(res.numAtoms)
            num_bonds = int(res.numBonds)
            mcs_mol = Chem.MolFromSmarts(smarts) if smarts else None
            smarts_smiles = Chem.MolToSmiles(mcs_mol) if mcs_mol is not None else ''

            return {
                'smarts': smarts,
                'smarts_smiles': smarts_smiles,
                'num_atoms': num_atoms,
                'num_bonds': num_bonds,
                'num_molecules': len(mols),
                'status': 'Success'
            }
        except Exception as e:
            return {'smarts': '', 'smarts_smiles': '', 'num_atoms': 0, 'num_bonds': 0, 'num_molecules': 0, 'status': f'Error: {str(e)}'}

    @staticmethod
    def match_smarts(smarts, smiles_list):
        """
        Match a SMARTS pattern against a list of SMILES strings.

        Args:
            smarts (str): SMARTS pattern
            smiles_list (list): list of SMILES strings

        Returns:
            dict: {'pattern': smarts, 'matches': list of match dicts, 'num_matched': int, 'status': str}
        """
        try:
            patt = Chem.MolFromSmarts(smarts)
            if patt is None:
                return {'pattern': smarts, 'matches': [], 'num_matched': 0, 'status': 'Invalid SMARTS'}

            matches = []
            num_matched = 0
            for s in smiles_list:
                m = Chem.MolFromSmiles(s)
                if m is None:
                    matches.append({'smiles': s, 'matched': False, 'match_count': 0, 'matches': []})
                    continue
                submatches = m.GetSubstructMatches(patt)
                matched = len(submatches) > 0
                if matched:
                    num_matched += 1
                matches.append({'smiles': s, 'matched': matched, 'match_count': len(submatches), 'matches': [tuple(map(int, msi)) for msi in submatches]})

            return {'pattern': smarts, 'matches': matches, 'num_matched': num_matched, 'status': 'Success'}
        except Exception as e:
            return {'pattern': smarts, 'matches': [], 'num_matched': 0, 'status': f'Error: {str(e)}'}

    @staticmethod
    def process_reaction(reaction_smarts, reactant_sets, timeout=10):
        """
        Process a reaction SMARTS on provided reactant sets.

        Args:
            reaction_smarts (str): reaction SMARTS (e.g., '[O:1]>>[OH:1]')
            reactant_sets (list): list of reactant tuples (each tuple/list of SMILES strings)

        Returns:
            dict: {'reaction': str, 'results': list of {'reactants': tuple, 'products': list}, 'status': str}
        """
        try:
            from rdkit.Chem import rdChemReactions
            rxn = rdChemReactions.ReactionFromSmarts(reaction_smarts)
            if rxn is None:
                return {'reaction': reaction_smarts, 'results': [], 'status': 'Invalid reaction SMARTS'}

            results = []
            for reactant_tuple in reactant_sets:
                try:
                    mols = [Chem.MolFromSmiles(s) for s in reactant_tuple]
                    if any(m is None for m in mols):
                        results.append({'reactants': tuple(reactant_tuple), 'products': [], 'status': 'Invalid reactant SMILES'})
                        continue
                    prods = rxn.RunReactants(tuple(mols))
                    # Flatten product sets into canonical SMILES
                    prod_sets = []
                    for prod in prods:
                        ps = [Chem.MolToSmiles(p, isomericSmiles=True) for p in prod]
                        prod_sets.append('.'.join(sorted(ps)))
                    results.append({'reactants': tuple(reactant_tuple), 'products': prod_sets, 'status': 'Success' if prod_sets else 'No products'})
                except Exception as e:
                    results.append({'reactants': tuple(reactant_tuple), 'products': [], 'status': f'Error: {str(e)}'})

            return {'reaction': reaction_smarts, 'results': results, 'status': 'Success'}
        except Exception as e:
            return {'reaction': reaction_smarts, 'results': [], 'status': f'Error: {str(e)}'}

    @staticmethod
    def plan_retrosynthesis(smiles, max_suggestions=10):
        """
        Provide naive retrosynthetic disconnections by single-bond cuts.

        Args:
            smiles (str): target molecule SMILES
            max_suggestions (int): maximum number of disconnections to return

        Returns:
            dict: {'target': str, 'suggestions': list of {'bond_idx': int, 'fragments': [smiles, smiles]}, 'status': str}
        """
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                return {'target': smiles, 'suggestions': [], 'status': 'Invalid SMILES'}

            bonds = [b for b in mol.GetBonds() if b.GetBondType().name == 'SINGLE']
            suggestions = []
            for b in bonds[:max_suggestions]:
                idx = b.GetIdx()
                frag_mol = Chem.FragmentOnBonds(mol, [idx], addDummies=True)
                frags = Chem.GetMolFrags(frag_mol, asMols=True, sanitizeFrags=True)
                frag_smiles = [Chem.MolToSmiles(f, isomericSmiles=True) for f in frags]
                suggestions.append({'bond_idx': idx, 'fragments': frag_smiles})

            return {'target': smiles, 'suggestions': suggestions, 'status': 'Success'}
        except Exception as e:
            return {'target': smiles, 'suggestions': [], 'status': f'Error: {str(e)}'}

    @staticmethod
    def check_lipinski(smiles):
        """
        Check Lipinski's Rule of Five

        Args:
            smiles (str): SMILES notation

        Returns:
            dict: Lipinski rule check results
        """
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                raise ValueError("Invalid SMILES string")

            mw = Descriptors.MolWt(mol)
            logp = Descriptors.MolLogP(mol)
            hbd = Descriptors.NumHDonors(mol)
            hba = Descriptors.NumHAcceptors(mol)

            return {
                'molecular_weight': mw,
                'logp': logp,
                'h_bond_donors': hbd,
                'h_bond_acceptors': hba,
                'mw_pass': mw <= 500,
                'logp_pass': logp <= 5,
                'hbd_pass': hbd <= 5,
                'hba_pass': hba <= 10,
                'violations': sum([
                    mw > 500,
                    logp > 5,
                    hbd > 5,
                    hba > 10
                ])
            }

        except Exception as e:
            raise ValueError(f"Failed to check Lipinski rules: {str(e)}")

    @staticmethod
    @staticmethod
    def analyze_stereochemistry(smiles):
        """
        Analyze stereochemical properties of a molecule

        Args:
            smiles (str): SMILES notation

        Returns:
            dict: {'chiral_centers': int, 'possible_stereoisomers': int, 'has_stereo': 'Yes'|'No'}
        """
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                raise ValueError("Invalid SMILES string")

            # Assign stereochemistry information
            Chem.AssignStereochemistry(mol, cleanIt=True, force=True, flagPossibleStereoCenters=True)

            # Find chiral centers (include unassigned so we know potential centers)
            chiral_centers = Chem.FindMolChiralCenters(mol, includeUnassigned=True)
            num_chiral_centers = len(chiral_centers)

            # Determine if any stereochemistry is explicitly defined (R/S or bond stereo)
            chiral_defined = any([c[1] in ('R', 'S') for c in chiral_centers])
            bond_stereo_defined = any([b.GetStereo() != Chem.BondStereo.STEREONONE for b in mol.GetBonds()])
            has_stereo = chiral_defined or bond_stereo_defined

            # Try to enumerate stereoisomers to get an accurate count when possible
            possible = None
            try:
                from rdkit.Chem.EnumerateStereoisomers import EnumerateStereoisomers, StereoEnumerationOptions
                opts = StereoEnumerationOptions(unique=True)
                isos = list(EnumerateStereoisomers(mol, options=opts))
                possible = len(isos)
            except Exception:
                # Fallback estimate: 2 ** (number of potential centers)
                possible = 2 ** num_chiral_centers if num_chiral_centers > 0 else 1

            return {
                'chiral_centers': num_chiral_centers,
                'possible_stereoisomers': possible,
                'has_stereo': 'Yes' if has_stereo else 'No'
            }

        except Exception as e:
            return {'chiral_centers': 0, 'possible_stereoisomers': 0, 'has_stereo': f'Error: {str(e)}'}

    def validate_smiles(smiles):
        """
        Validate SMILES string

        Args:
            smiles (str): SMILES notation

        Returns:
            dict: Validation result
        """
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                return {'valid': False, 'message': 'Invalid SMILES string'}

            return {
                'valid': True,
                'message': 'Valid SMILES',
                'canonical_smiles': Chem.MolToSmiles(mol)
            }
        except Exception as e:
            return {'valid': False, 'message': str(e)}
