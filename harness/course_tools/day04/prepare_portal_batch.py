"""Offline-only cloning of the user-captured trial; never runs a browser activity."""
from pathlib import Path
from copy import deepcopy
from lxml import etree as E
import hashlib,json
from openpyxl import load_workbook

root=Path(__file__).parents[2]
p=root/'nap04/working/setup_2026-10-06/BPA_Setup_Smoke'
source=p/'Portal_Logged_Trial.xaml'
prepared=json.loads((p.parent/'portal_user_run_prepared.json').read_text())
assert hashlib.sha256(source.read_bytes()).hexdigest()==prepared['workflow_sha256']
doc=E.parse(str(source));r=doc.getroot();ns=r.nsmap
w=ns[None];x=ns['x'];ui=ns['ui'];uix=ns['uix'];sap2010=ns['sap2010']
def tag(n):return '{'+w+'}'+n
def make(n,**attrs):return E.Element(tag(n),attrib=attrs)
seq=r.find(tag('Sequence'))
r.set('{'+x+'}Class','Portal_Batch_Resume')
variables=seq.find(tag('Sequence.Variables'))
for name,typ,default in [('batchRunDir','x:String',None),('rowData','sd2:DataTable',None),('batchBaselineReviewed','x:Boolean','False')]:
 v=make('Variable',Name=name);v.set('{'+x+'}TypeArguments',typ)
 if default is not None:v.set('Default',default)
 variables.append(v)
def assign(name,value):
 n=make('Assign',DisplayName='Batch set '+name);to=E.SubElement(n,tag('Assign.To'));out=E.SubElement(to,tag('OutArgument'));out.set('{'+x+'}TypeArguments','x:String');out.text='['+name+']'
 val=E.SubElement(n,tag('Assign.Value'));arg=E.SubElement(val,tag('InArgument'));arg.set('{'+x+'}TypeArguments','x:String');arg.text='['+value+']';return n
def guard(condition,message):
 n=make('If',Condition='['+condition+']',DisplayName=message);then=E.SubElement(n,tag('If.Then'));s=E.SubElement(then,tag('Sequence'));E.SubElement(s,tag('Throw'),Exception='[New System.InvalidOperationException("'+message.replace('"','""')+'")]');return n
runassign=next(n for n in seq if n.get('DisplayName')=='Set runDir')
runassign.find('.//'+tag('InArgument')).text=runassign.find('.//'+tag('InArgument')).text.replace('"portal_runs"','"portal_batch_runs"')
i=list(seq).index(runassign);seq.insert(i+1,assign('batchRunDir','runDir'))
seq.insert(i+2,guard('Not batchBaselineReviewed','Fresh baseline CSV must be reconciled before user-operated batch; do not run yet.'))
read=seq.find('{'+ui+'}ReadRange');read.set('Range','');read.set('DisplayName','Read all10lesson rows with headers')
g=next(n for n in seq if n.get('DisplayName')=='Guard: Expected exactly one input row');g.set('Condition','[dt Is Nothing OrElse dt.Rows.Count <> 10]');g.set('DisplayName','Guard: Expected exactly ten input rows')
g.find('.//'+tag('Throw')).set('Exception','[New System.InvalidOperationException("Expected exactly ten input rows")]')
reserve=next(n for n in seq if E.QName(n).localname=='InvokeCode')
reservedlog=next(n for n in seq if n.get('DisplayName')=='Log policy_reserved')
seq.remove(reserve);seq.remove(reservedlog)
card=seq.find('{'+uix+'}NApplicationCard')
loop=card.find('.//{'+ui+'}ForEach');loop.set('DisplayName','All10rows; skip only verified first policy')
body=loop.find('.//'+tag('ActivityAction'));rowseq=body.find(tag('Sequence'));body.remove(rowseq)
skip=guard('False','unused') # replace its branches with the actual no-replay branch
skip.set('Condition','[CurrentRow("kotvenyszam").ToString() = "TR-402318"]');skip.set('DisplayName','Skip previously verified K-GY-4147; never submit twice')
then=skip.find(tag('If.Then'));then.clear();s=E.SubElement(then,tag('Sequence'))
E.SubElement(s,'{'+ui+'}LogMessage',DisplayName='Previously verified first row',Level='Info',Message='Skipped TR-402318: already verified as K-GY-4147; no portal action for this row.')
otherwise=E.SubElement(skip,tag('If.Else'));otherwise.append(rowseq);body.append(skip)
startlog=next(n for n in seq if n.get('DisplayName')=='Log run_started')
inputlog=next(n for n in seq if n.get('DisplayName')=='Log input_read')
finishlog=next(n for n in seq if n.get('DisplayName')=='Log run_finished_pending_readback')
def logclone(template,detail=None):
 n=deepcopy(template)
 if detail is not None:
  for a in n.iter(tag('InArgument')):
   if a.get('{'+x+'}Key')=='in_Detail':a.text='["'+detail+'"]'
 return n
snap=deepcopy(seq.find('{'+ui+'}WriteRange'));snap.set('DataTable','[rowData]');snap.set('AddHeaders','True');snap.set('StartingCell','A1');snap.set('DisplayName','Save one batch item snapshot')
code=E.Element('{'+ui+'}InvokeCode',DisplayName='One-row evidence data',Code='rowTable = inputTable.Clone()\nrowTable.ImportRow(inputRow)',Language='VBNet')
args=E.SubElement(code,'{'+ui+'}InvokeCode.Arguments')
for kind,key,typ,val in [('InArgument','inputTable','sd2:DataTable','dt'),('InArgument','inputRow','sd2:DataRow','CurrentRow'),('OutArgument','rowTable','sd2:DataTable','rowData')]:
 n=E.SubElement(args,tag(kind));n.set('{'+x+'}Key',key);n.set('{'+x+'}TypeArguments',typ);n.text='['+val+']'
preamble=[assign('policy','CurrentRow("kotvenyszam").ToString()'),assign('caseId','String.Empty'),assign('stage','"initializing"'),assign('runDir','System.IO.Path.Combine(batchRunDir, policy)'),guard('Not System.Text.RegularExpressions.Regex.IsMatch(policy,"^TR-[0-9]{6}$")','Invalid policy format; stop batch.'),guard('Not String.IsNullOrWhiteSpace(CurrentRow("ugyszam").ToString())','Input has existing case ID; reconcile before submit.'),logclone(startlog,'One batch item; no automatic retry'),code,snap,logclone(inputlog,'One row saved in input_snapshot.xlsx'),reserve,reservedlog]
# Insert after designer view-state property, before the original UI TryCatch.
pos=next(i for i,n in enumerate(rowseq) if E.QName(n).localname=='TryCatch')
for n in preamble:rowseq.insert(pos,n);pos+=1
rowseq.append(logclone(finishlog))
outerfinish=list(seq).index(finishlog);seq.insert(outerfinish,assign('runDir','batchRunDir'));finishlog.set('DisplayName','Batch finished pending exported readback')
for n in finishlog.iter(tag('InArgument')):
 if n.get('{'+x+'}Key')=='in_Event':n.text='["batch_finished_pending_readback"]'
 if n.get('{'+x+'}Key')=='in_Detail':n.text='["Ten input rows considered; first verified row skipped; export and compare all rows."]'
# IdRefs are local designer IDs; preserve every captured target descriptor unchanged.
for i,n in enumerate(r.iter()):
 if n.get('{'+sap2010+'}IdRef') is not None:n.set('{'+sap2010+'}IdRef','Batch_'+str(i))
original=E.parse(str(source))
def targets(tree):return [E.tostring(n,method='c14n') for n in tree.iter() if E.QName(n).localname in ('TargetAnchorable','TargetApp')]
assert targets(original)==targets(r)
input_path=root/'nap04/working/readiness_2026-10-06/karbejelentesek_input.xlsx'
rows=list(load_workbook(input_path,read_only=True,data_only=True)['bejelentesek'].values)
assert len(rows)==11 and len(set(row[0] for row in rows[1:]))==10 and rows[1][0]=='TR-402318'
assert all(row[5] is None for row in rows[1:])
out=p/'Portal_Batch_Resume.xaml';out.write_bytes(E.tostring(r,encoding='utf-8',xml_declaration=False,pretty_print=True))
report={'scope':'Offline preparation only; no portal execution','input_rows':10,'previously_verified_policy':'TR-402318','previously_verified_case':'K-GY-4147','remaining_policies':[row[0] for row in rows[2:]],'batchBaselineReviewed':False,'captured_target_descriptors_unchanged':True,'source_trial_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'batch_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'required_before_enable':'Fresh own-record CSV and user total count; check first row exact, no other input policies/uncertain reservation locks; preserve baseline.'}
(p.parent/'portal_batch_preparation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print('Prepared guarded batch:10inputs,9remaining, targets unchanged; NOT executed')
