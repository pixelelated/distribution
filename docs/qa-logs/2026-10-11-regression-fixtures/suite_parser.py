def suite_rows(text):
 header='| suite | result | time | log |'
 assert text.count(header)==1, 'missing or duplicate suite table'
 table=text.split(header+'\n',1)[1].split('\n\n',1)[0]
 lines=table.splitlines()
 assert lines[0]=='| --- | --- | --- | --- |', 'wrong table separator'
 pairs=[]
 for line in lines[1:]:
  fields=[x.strip() for x in line.split('|')]
  assert len(fields)==6 and fields[0]==fields[-1]=='',line
  pairs.append((fields[1],fields[2]))
 expected={'scripts','lifetime','wrapper','vocabulary','french','quoting','menumap','register','pair-identity','fresh','round-trip','exit','time-to-play','walks','frame-diff'}
 assert len(pairs)==len(expected) and {k for k,v in pairs}==expected,pairs
 rows=dict(pairs)
 assert rows.pop('scripts')=='FAIL (1)',rows
 assert all(v=='PASS' for v in rows.values()),rows
 return rows
