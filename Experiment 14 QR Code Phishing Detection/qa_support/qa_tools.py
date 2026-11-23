"""Prepare and verify immutable research checkpoints. No training or calibration."""
import ast
import copy
from datetime import datetime, timezone
import hashlib
import importlib
import importlib.metadata as metadata
import inspect
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import venv
import joblib
import numpy as np
import pandas as pd

SUPPORT = Path(__file__).resolve().parent
PINNED_EXP08 = 'exp08_repeated_training_20261121T170229937001Z'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def unique_directory(override, candidates, root, label):
    if override is not None:
        selected = Path(override)
        selected = selected if selected.is_absolute() else root / selected
        if not selected.is_dir():
            raise FileNotFoundError(selected)
        return selected.resolve()
    choices = sorted({Path(p).resolve() for p in candidates})
    if len(choices) != 1:
        raise RuntimeError(f'Set {label} explicitly. Candidates: {[str(p) for p in choices]}')
    return choices[0]

def discover(root, exp08=None, search=None, corrected=None, decoder=None):
    root = Path(root).resolve()
    exp08 = unique_directory(exp08, (root/'outputs/quishing02').rglob(PINNED_EXP08), root, 'EXP08_OVERRIDE')
    normalized = exp08.parent
    search = unique_directory(search, [p for p in normalized.glob('exp13_path_encoding_*/schemeless_search')
        if (p/'stored_qr_verification/details.csv').is_file()], root, 'PATH_SEARCH_OVERRIDE')
    corrected = unique_directory(corrected, [p for p in search.glob('corrected_search_*')
        if (p/'clean_qr_verification/results.csv').is_file()], root, 'CORRECTED_OVERRIDE')
    decoder = unique_directory(decoder, [p for p in normalized.glob('qr_package_*')
        if (p/'qr_decoder.py').is_file() and (p/'sha256.json').is_file()], root, 'DECODER_PACKAGE_OVERRIDE')
    return {'root':root, 'exp08':exp08, 'search':search, 'corrected':corrected, 'decoder':decoder}

def verify_sources(paths):
    manifest = read_json(paths['exp08']/'evidence_manifest.json')
    audit = []
    for item in manifest['evidence'] + manifest['models']:
        path = paths['exp08']/item['file']
        if not path.is_file() or sha(path) != item['sha256']:
            raise ValueError(f'Research artifact integrity mismatch: {path}')
        audit.append({'file':str(path.relative_to(paths['root'])), 'sha256':item['sha256'], 'checked':True})
    decoder_hashes = read_json(paths['decoder']/'sha256.json')
    if sha(paths['decoder']/'qr_decoder.py') != decoder_hashes['qr_decoder.py']:
        raise ValueError('Previously captured decoder source has changed.')
    audit.append({'file':str((paths['decoder']/'qr_decoder.py').relative_to(paths['root'])),
                  'sha256':decoder_hashes['qr_decoder.py'], 'checked':True})
    return pd.DataFrame(audit)

def _bools(frame, name):
    values = frame[name].astype(str).str.strip().str.lower()
    if not values.isin(['true','false','1','0']).all():
        raise ValueError(f'Invalid boolean values: {name}')
    return values.isin(['true','1'])

def _resolve_source_png(saved, root):
    path = Path(str(saved))
    if path.is_file():
        return path
    if 'outputs' in path.parts:
        path = root.joinpath(*path.parts[path.parts.index('outputs'):])
    if not path.is_file():
        raise FileNotFoundError(path)
    return path

def _learned_state(model):
    states = {}
    for name, estimator in model.get_params(deep=True).items():
        if hasattr(estimator, '__dict__'):
            attributes = {k:v for k,v in vars(estimator).items()
                          if k.endswith('_') and not k.startswith('__')}
            # Transformer lists contain function references, not learned values.
            attributes.pop('transformer_list', None)
            if attributes:
                states[name] = attributes
    return joblib.hash(states)

def _load_and_bind(path, features):
    # Compatibility bridge for our own trusted __main__ checkpoints only.
    main = sys.modules['__main__']
    names = [name for name in vars(features) if name.startswith('n02_') and callable(getattr(features,name))]
    sentinel = object()
    previous = {name:getattr(main,name,sentinel) for name in names}
    try:
        for name in names:
            setattr(main,name,getattr(features,name))
        record = joblib.load(path)
    finally:
        for name,value in previous.items():
            if value is sentinel:
                delattr(main,name)
            else:
                setattr(main,name,value)
    model = record['model']
    before = _learned_state(model)
    replacements = {}
    for name,value in model.get_params(deep=True).items():
        if name.endswith('__func') and callable(value):
            if value.__name__ not in names:
                raise ValueError(f'Unreviewed feature callable: {value}')
            replacements[name] = getattr(features,value.__name__)
    model.set_params(**replacements)
    if _learned_state(model) != before:
        raise AssertionError('Learned state changed while binding importable functions.')
    return record, model, before, sorted(replacements)

def _requirements():
    # Keep the source interpreter's exact versions; a missing published wheel is a QA failure.
    package_map = metadata.packages_distributions()
    distributions = {'numpy','scipy','scikit-learn','joblib','threadpoolctl'}
    for module in ['cv2','zxingcpp']:
        candidates = package_map.get(module,[])
        if len(candidates) != 1:
            raise RuntimeError(f'Expected one installed distribution for {module}; found {candidates}')
        distributions.add(candidates[0])
    return {name:metadata.version(name) for name in sorted(distributions)}

def create_package(paths, destination=None):
    verify_sources(paths)
    destination = Path(destination) if destination else paths['root']/(
        'outputs/quishing04/qa_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    destination.mkdir(parents=True, exist_ok=False)
    package = destination/'package'
    package.mkdir()
    for name in ['quishing_features.py','quishing_pipeline.py','verify_package.py','run_verification.py','source_lineage.json']:
        shutil.copy2(SUPPORT/name,package/name)
    shutil.copy2(paths['decoder']/'qr_decoder.py',package/'qr_decoder.py')
    # Use a versioned source module path, never a function pulled from the current kernel.
    sys.path.insert(0,str(package))
    try:
        if 'quishing_features' in sys.modules:
            loaded = Path(sys.modules['quishing_features'].__file__).resolve()
            if loaded != (package/'quishing_features.py').resolve():
                raise RuntimeError('Restart this QA kernel before exporting another package.')
        features = importlib.import_module('quishing_features')
        source_manifest = read_json(paths['exp08']/'evidence_manifest.json')
        lineage=[];thresholds={}
        for item in source_manifest['models']:
            source = paths['exp08']/item['file']
            record,model,learned_hash,bound = _load_and_bind(source,features)
            seed = int(record['seed'])
            if seed not in [42,142,242] or seed in thresholds:
                raise ValueError('Unexpected or duplicated training seed.')
            if float(record['threshold']) != float(item['threshold']):
                raise AssertionError('Threshold differs from saved manifest.')
            thresholds[str(seed)] = float(record['threshold'])
            target = package/f'model_seed_{seed}.joblib'
            joblib.dump(model,target)
            lineage.append({'seed':seed,'source_checkpoint':str(source.relative_to(paths['root'])),
                'source_sha256':item['sha256'],'export_sha256':sha(target),
                'threshold':float(record['threshold']),'learned_state_fingerprint':learned_hash,
                'rebound_function_parameters':bound})
    finally:
        sys.path.remove(str(package))
    if set(thresholds) != {'42','142','242'}:
        raise AssertionError('All three seed checkpoints are required.')
    distributions = _requirements()
    config = {'revision':'R2 hostname-and-unreserved-path normalized',
        'seeds':[42,142,242],'default_seed':42,'default_seed_policy':'fixed presentation convention; no winner selected',
        'thresholds':thresholds,'calibration_target':0.02,'image_shape':[69,69],
        'source_python':sys.version,'distributions':distributions,'retrained':False,'recalibrated':False}
    (package/'config.json').write_text(json.dumps(config,indent=2))
    (package/'requirements.txt').write_text(''.join(f'{k}=={v}\n' for k,v in distributions.items()))
    (package/'artifact_lineage.json').write_text(json.dumps({'models':lineage,
        'research_manifest_sha256':sha(paths['exp08']/'evidence_manifest.json'),
        'decoder_source_sha256':sha(paths['decoder']/'qr_decoder.py')},indent=2))
    (package/'README.md').write_text('''# Frozen R2 QR phishing research package

Use Python with the same major and minor version as the recorded source interpreter.
Install requirements.txt in a new virtual environment. No model fitting is required.

```python
from quishing_pipeline import analyse_png
result = analyse_png("example.png", seed=42)
print(result)
```

Only the evaluated 69 x 69 grayscale display convention is supported.
Prediction -1 means abstention, 0 legitimate, 1 phishing. Abstention must not authorize a destination.
Only accepted decoded text reaches the classifier. No destination is contacted.
Scores are not calibrated probabilities. Validation was repeatedly inspected in development.
Three seeds use one fixed split; no general robustness or production-readiness claim is made.

The separate verification directory includes historical QR payloads, including phishing addresses.
Review dataset permissions and publication inputs before sharing those fixtures.
Only load model files from a trusted origin. Hashes detect changes, not malicious provenance.
This package verifies frozen-model inference; full research training is not rerun here.
''',encoding='utf-8')
    (destination/'qa_state.json').write_text(json.dumps({'status':'export_prepared_verification_pending'},indent=2))
    return {'paths':paths,'run_dir':destination,'package':package,'lineage':pd.DataFrame(lineage)}

def prepare_inputs(context):
    paths=context['paths'];package=context['package']
    exp=paths['exp08'];search=paths['search'];clean_dir=paths['corrected']/'clean_qr_verification'
    clean=pd.read_csv(clean_dir/'results.csv')
    pred=pd.read_csv(exp/'predictions.csv')
    pred=pred.loc[pred['subset'].eq('Original validation')]
    membership=pd.read_csv(exp/'subset_membership.csv')
    membership=membership.loc[membership['subset'].eq('validation')]
    attacks=pd.read_csv(search/'stored_qr_verification/details.csv')
    attacks=attacks.loc[_bools(attacks,'verified_conditional_evasion')]
    pairs=pd.read_csv(search/'source_results.csv')
    expected_counts={'clean':1956,'attacks':69,'pairs':755}
    if (len(clean),len(attacks),len(pairs)) != tuple(expected_counts.values()):
        raise AssertionError('Unexpected research cohort sizes; review the selected run.')
    if clean['image_index'].duplicated().any() or membership['image_index'].duplicated().any():
        raise ValueError('Duplicate clean or membership IDs.')
    ids=set(clean['image_index'])
    if ids != set(membership['image_index']):
        raise AssertionError('Validation memberships differ.')
    by_seed={}
    for seed in [42,142,242]:
        frame=pred.loc[pred['seed'].eq(seed)]
        if frame['image_index'].duplicated().any() or set(frame['image_index']) != ids:
            raise AssertionError('Missing/duplicate seed prediction membership.')
        by_seed[seed]=frame.set_index('image_index')
    hashes=membership.set_index('image_index')['payload_sha256']
    verification=package/'verification';verification.mkdir()
    plan={'clean':[],'attacks':[]}
    for row in clean.sort_values('image_index').itertuples(index=False):
        image_id=int(row.image_index)
        rel=Path('verification/images/clean')/f'{image_id}.png'
        (package/rel).parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(clean_dir/f'{image_id}.png',package/rel)
        expected={}
        for seed in [42,142,242]:
            saved=by_seed[seed].loc[image_id]
            if int(saved['label']) != int(row.label):raise AssertionError('Clean label mismatch.')
            expected[str(seed)]={'score':float(saved['score']),'prediction':int(saved['prediction'])}
        plan['clean'].append({'image_index':image_id,'label':int(row.label),
            'file':str(rel),'payload_sha256':str(hashes.loc[image_id]),'expected':expected})
    for row in attacks.sort_values('image_index').itertuples(index=False):
        image_id=int(row.image_index)
        rel=Path('verification/images/stored_path_attack')/f'{image_id}.png'
        (package/rel).parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(_resolve_source_png(row.stored_png,paths['root']),package/rel)
        plan['attacks'].append({'image_index':image_id,'file':str(rel),
            'payload_sha256':hashlib.sha256(row.candidate_payload.encode('utf-8')).hexdigest(),
            'original_scores':{str(s):float(by_seed[s].loc[image_id,'score']) for s in [42,142,242]}})
    pair_data=[{'image_index':int(r.image_index),'original_payload':r.original_payload,
                'candidate_payload':r.candidate_payload} for r in pairs.itertuples(index=False)]
    (verification/'plan.json').write_text(json.dumps(plan,indent=2))
    (verification/'path_pairs.json').write_text(json.dumps(pair_data,indent=2))
    for name in ['protocol.json','training_summary.csv','evidence_manifest.json',
                 'subset_membership.csv','path_attack_checks.csv']:
        target=verification/'research'/name;target.parent.mkdir(exist_ok=True);shutil.copy2(exp/name,target)
    inventory=[]
    for path in sorted(package.rglob('*')):
        if path.is_file() and '__pycache__' not in path.parts and path.name!='sha256.json':
            inventory.append({'file':str(path.relative_to(package)),'bytes':path.stat().st_size,
                              'sha256':sha(path),'historical_dataset_fixture':path.is_relative_to(verification)})
    (package/'sha256.json').write_text(json.dumps({r['file']:r['sha256'] for r in inventory},indent=2))
    context['inventory']=pd.DataFrame(inventory)
    context['inventory'].to_csv(context['run_dir']/'publication_input_inventory.csv',index=False)
    return pd.DataFrame([{'group':'clean QR','sources':len(plan['clean'])},
        {'group':'stored known path attacks','sources':len(plan['attacks'])},
        {'group':'retained URL pairs','sources':len(pair_data)},
        {'group':'transformations on final seed 42','sources':'8 x 1956 in baseline; 8 x 16 in fresh parity'}])

def _run_logged(command, log, cwd, timeout=3600):
    log=Path(log)
    env=os.environ.copy();env['PYTHONNOUSERSITE']='1';env.pop('PYTHONPATH',None)
    started=time.monotonic();offset=0
    with log.open('w') as stream:
        process=subprocess.Popen([str(x) for x in command],cwd=str(cwd),stdout=stream,
                                 stderr=subprocess.STDOUT,env=env,text=True)
        try:
            while process.poll() is None:
                if time.monotonic()-started>timeout:
                    process.kill();process.wait();raise TimeoutError(f'Check timed out; see {log.name}')
                time.sleep(1)
                with log.open() as reader:
                    reader.seek(offset);new=reader.read();offset=reader.tell()
                    if new:print(new,end='',flush=True)
            with log.open() as reader:
                reader.seek(offset);new=reader.read()
                if new:print(new,end='',flush=True)
            if process.returncode:
                raise RuntimeError(f'Command failed ({process.returncode}); see {log}')
        except BaseException:
            if process.poll() is None:process.kill();process.wait()
            raise
    return {'returncode':process.returncode,'log':str(log)}

def verify_same_environment(context):
    output=context['run_dir']/'same_environment_results.json'
    _run_logged([sys.executable,'-I',context['package']/'run_verification.py',
                 '--output',output],context['run_dir']/'same_environment.log',context['package'])
    context['same_result']=read_json(output)
    return summarize(context['same_result'])

def install_fresh_environment(context):
    environment=context['run_dir']/'fresh_environment'
    if environment.exists():
        raise RuntimeError('This fresh environment already exists. Reuse its interpreter for verification or start a new QA run.')
    venv.EnvBuilder(with_pip=True,system_site_packages=False).create(environment)
    python=environment/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
    context['fresh_python']=python
    _run_logged([python,'-m','pip','install','--disable-pip-version-check','-r',
        context['package']/'requirements.txt'],context['run_dir']/'fresh_environment_install.log',
        context['package'],timeout=1800)
    return pd.DataFrame([{'environment':str(environment),'inherits_system_packages':False,
                          'requirements':'exact recorded source versions','install':'passed'}])

def verify_fresh_environment(context):
    python=context.get('fresh_python')
    if not python or not Path(python).is_file():raise RuntimeError('Create the fresh environment first.')
    output=context['run_dir']/'fresh_environment_results.json'
    _run_logged([python,'-I',context['package']/'run_verification.py','--output',output,
        '--transform-limit','16','--require-venv'],context['run_dir']/'fresh_environment_verification.log',context['package'])
    context['fresh_result']=read_json(output)
    return summarize(context['fresh_result'])

def summarize(result):
    frame=pd.DataFrame(result['records']);rows=[]
    for (group,seed),part in frame.groupby(['group','seed'],sort=False):
        phishing=part['label'].eq(1);legitimate=part['label'].eq(0)
        tp=int((phishing & part['prediction'].eq(1)).sum());fp=int((legitimate & part['prediction'].eq(1)).sum())
        rows.append({'group':group,'seed':seed,'QR_images':len(part),
            'accepted':int(part['accepted'].sum()),'phishing_detected':tp,'false_alarms':fp,
            'recall_all':tp/int(phishing.sum()) if phishing.any() else None,
            'FPR_all':fp/int(legitimate.sum()) if legitimate.any() else None,
            'abstentions':int(part['prediction'].eq(-1).sum())})
    return pd.DataFrame(rows)

def finalize(context):
    baseline=context.get('same_result');fresh=context.get('fresh_result')
    if not baseline or not fresh or baseline['status']!='passed' or fresh['status']!='passed':
        raise RuntimeError('Both verification runs must pass before QA can be concluded.')
    base={(r['group'],r['image_index'],r['seed']):r for r in baseline['records']}
    for row in fresh['records']:
        prior=base[(row['group'],row['image_index'],row['seed'])]
        for key in ['accepted','payload_sha256','prediction']:
            if row[key]!=prior[key]:raise AssertionError(f'Fresh-environment parity mismatch: {key}')
        if row['score'] is None:
            if prior['score'] is not None:raise AssertionError('Abstention score mismatch.')
        elif not np.isclose(row['score'],prior['score'],rtol=1e-10,atol=1e-12):
            raise AssertionError('Fresh-environment score mismatch.')
    if not fresh['isolated_venv_checked']:raise AssertionError('Isolated environment not verified.')
    if baseline['versions'] != fresh['versions']:raise AssertionError('Installed dependency versions differ.')
    summary=summarize(baseline);summary.to_csv(context['run_dir']/'final_R2_QR_results.csv',index=False)
    expected=pd.read_csv(context['paths']['exp08']/'training_summary.csv')
    expected=expected.loc[expected['subset'].eq('Original validation')].set_index('seed')
    for row in summary.loc[summary['group'].eq('clean')].itertuples(index=False):
        if row.phishing_detected!=int(expected.loc[row.seed,'phishing_detected']) or row.false_alarms!=int(expected.loc[row.seed,'false_alarms']):
            raise AssertionError('Validation totals differ from research.')
    report={'technical_status':'passed','scope':'Frozen R2 inference and artifact lineage, not full-training rerun',
        'source_research_notebook_sha256':read_json(SUPPORT/'source_lineage.json')['research_notebook_sha256'],
        'same_environment_result_sha256':sha(context['run_dir']/'same_environment_results.json'),
        'fresh_environment_result_sha256':sha(context['run_dir']/'fresh_environment_results.json'),
        'fresh_parity_records':len(fresh['records']),'seeds':[42,142,242],
        'clean_QRs_per_seed':1956,'known_path_attack_QRs_per_seed':69,
        'retained_path_pairs_per_seed':755,'R2_full_transformations_seed_42':8,
        'fresh_transformations_samples_per_condition':16,'model_retrained':False,'threshold_recalibrated':False,
        'publication_status':'pending review of dataset fixtures and report/README integration',
        'limitations':['Previously inspected development validation.',
                       'Fixed fitting/calibration membership across seeds.',
                       'Known-attack replay, not a fresh adaptive search.',
                       '69 x 69 evaluated image convention only.',
                       'No live destination contacted; path equivalence remains conditional.']}
    (context['run_dir']/'qa_report.json').write_text(json.dumps(report,indent=2))
    (context['run_dir']/'qa_state.json').write_text(json.dumps(report,indent=2))
    return pd.DataFrame([{'check':'same-environment inference and saved-score parity','status':'passed'},
        {'check':'fresh isolated-environment inference and parity','status':'passed'},
        {'check':'model and threshold preservation','status':'passed'},
        {'check':'publication of dataset fixtures and final documentation','status':'review pending'}])
