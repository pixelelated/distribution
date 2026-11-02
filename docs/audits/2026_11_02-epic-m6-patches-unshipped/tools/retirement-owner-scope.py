#!/usr/bin/env python3
"""Explicit own-lane process evidence; never an all-UID/global-clean census."""
import os,pathlib
LIMIT='Original all-same-UID attempt could not read /proc/2389/cwd. Its owner/references remain unknown; this module does not inspect it or claim it unrelated. No all-same-UID/global no-reference assertion is available.'
def identity(pid):
 p=pathlib.Path('/proc')/str(pid);raw=(p/'stat').read_text();start=raw.rsplit(')',1)[1].split()[19]
 uid=int(next(x for x in (p/'status').read_text().splitlines() if x.startswith('Uid:')).split()[1])
 return {'pid':pid,'uid':uid,'start_ticks':start}
def references(pid):
 p=pathlib.Path('/proc')/str(pid);out=[]
 for link in [p/'cwd']+list((p/'fd').iterdir()):
  try:out.append(os.readlink(link))
  except FileNotFoundError:continue
 return out
def observer():return {**identity(os.getpid()),'role':'current metadata/deletion observer','state':'active-observer'}
def assess(root,completion,known_jobs,reference_reader=references,identity_reader=identity):
 assert completion.get('finished') and isinstance(completion.get('exit'),int) and completion.get('termination')=='returned','missing or ambiguous own completion'
 assert completion.get('child_accounting')=='synchronous source/control implementation; no persistent child or handoff','unaccounted own descendant or handoff'
 checked=[]
 for job in known_jobs:
  assert all(k in job for k in ('pid','uid','start_ticks')),'ambiguous known owner identity'
  try:
   actual=identity_reader(job['pid'])
   assert actual=={k:job[k] for k in ('pid','uid','start_ticks')},'ambiguous known owner identity'
   refs=reference_reader(job['pid'])
  except (PermissionError,FileNotFoundError,ProcessLookupError) as e:raise AssertionError('inaccessible or ambiguous known owner: '+type(e).__name__)
  hit=[p for p in refs if p==root or p.startswith(root+'/')]
  assert not hit,'known own cwd/fd reference'
  assert job.get('role')=='current metadata/deletion observer' and job.get('state')=='active-observer','known relevant T43 owner remains live'
  checked.append({**job,'references_to_root':[]})
 return {'scope':'completed named T43 producer plus explicit current known T43 jobs only','completion':completion,'known_jobs':checked,'global_no_reference_assertion':False,'unknown_process_visibility_limit':LIMIT}
