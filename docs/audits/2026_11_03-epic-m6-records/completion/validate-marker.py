"""Invoke the existing schema1 validator."""
import datetime,json,pathlib,runpy
C=pathlib.Path(__file__).resolve().parent;R=C.parents[3];api=runpy.run_path(str(R/'tools/ceremony-check'),run_name='completion_validator')
ended,issue=api['completed_audit_marker'](C.parent/'audit-completion.json',R,datetime.datetime.now(datetime.timezone.utc));assert issue==1417
print(json.dumps({'result':'PASS','existing_validator':'tools/ceremony-check:completed_audit_marker','issue':issue,'completed_at':ended.isoformat()}))
