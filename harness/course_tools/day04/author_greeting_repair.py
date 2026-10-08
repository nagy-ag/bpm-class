from pathlib import Path
from xml.sax.saxutils import quoteattr

p=Path(__file__).parent/'Nap04_gyakorlas'
root=(p/'Main.xaml').read_text(encoding='utf-8').split('  <Sequence DisplayName=')[0]
q=quoteattr
def workflow(name,body,members=''):
    r=root.replace('x:Class="Main"',f'x:Class="{name}"')
    if members:r=r.replace('  <TextExpression.NamespacesForImplementation>',members+'\n  <TextExpression.NamespacesForImplementation>',1)
    (p/(name+'.xaml')).write_text(r+body+'\n</Activity>\n',encoding='utf-8')
def assign(to,value):
    return f'<Assign DisplayName="Eredmény"><Assign.To><OutArgument x:TypeArguments="x:String">[{to}]</OutArgument></Assign.To><Assign.Value><InArgument x:TypeArguments="x:String">{value}</InArgument></Assign.Value></Assign>'
def invoke(value,out='eredmeny'):
    return f'<ui:InvokeWorkflowFile DisplayName="Ellenőrzött számolás" WorkflowFileName="Calculation_Validated.xaml" UnSafe="False"><ui:InvokeWorkflowFile.Arguments><InArgument x:TypeArguments="x:String" x:Key="in_darab">{value}</InArgument><OutArgument x:TypeArguments="x:String" x:Key="out_text">[{out}]</OutArgument></ui:InvokeWorkflowFile.Arguments></ui:InvokeWorkflowFile>'
valid='[&quot;Évente kb. &quot; &amp; (napiDarab*250).ToString() &amp; &quot; e-mail.&quot;]'
invalid='0 és 1 000 000 közötti egész számot adj meg.'
workflow('Calculation_Validated','''<Sequence DisplayName="Éves becslés bemenetellenőrzéssel">
<Sequence.Variables><Variable x:TypeArguments="x:Int32" Name="napiDarab"/></Sequence.Variables>
<If DisplayName="Egész és megengedett tartomány" Condition="[Integer.TryParse(in_darab, napiDarab) AndAlso napiDarab &gt;= 0 AndAlso napiDarab &lt;= 1000000]">
<If.Then><Sequence DisplayName="Érvényes"><Assign DisplayName="Érvényes szám tárolása"><Assign.To><OutArgument x:TypeArguments="x:Int32">[napiDarab]</OutArgument></Assign.To><Assign.Value><InArgument x:TypeArguments="x:Int32">[CInt(in_darab)]</InArgument></Assign.Value></Assign>'''+assign('out_text',valid)+'''</Sequence></If.Then>
<If.Else><Sequence DisplayName="Hibás">'''+assign('out_text',invalid)+'''</Sequence></If.Else></If>
</Sequence>''','''<x:Members><x:Property Name="in_darab" Type="InArgument(x:String)"/><x:Property Name="out_text" Type="OutArgument(x:String)"/></x:Members>''')
s=(p/'Greeting_Initial.xaml').read_text(encoding='utf-8')
s=s.replace('x:Class="Greeting_Initial"','x:Class="Greeting_Repaired"').replace('– eredeti','– ellenőrzött')
s=s.replace('<Variable x:TypeArguments="x:String" Name="darab"/>','<Variable x:TypeArguments="x:String" Name="darab"/><Variable x:TypeArguments="x:String" Name="eredmeny"/>')
old=s.index('<ui:MessageBox DisplayName="Éves e-mail becslés – CInt"')
end=s.index('/>',old)+2
s=s[:old]+invoke('[darab]')+'\n<ui:MessageBox DisplayName="Ellenőrzött éves becslés" Text="[eredmeny]" AutoCloseAfter="00:00:00"/>\n'+s[end:]
(p/'Greeting_Repaired.xaml').write_text(s,encoding='utf-8')
cases=[('5','Évente kb. 1250 e-mail.'),('sok',invalid),('-1',invalid),('',invalid),('0','Évente kb. 0 e-mail.'),('1000000','Évente kb. 250000000 e-mail.'),('1000001',invalid),('2147483648',invalid)]
body='<Sequence DisplayName="Valódi számoló workflow regressziós teszt"><Sequence.Variables><Variable x:TypeArguments="x:String" Name="eredmeny"/></Sequence.Variables>\n'
for raw,expected in cases:
    body+=invoke('['+q(raw).replace('"','&quot;')+']')+'\n'
    cond='[eredmeny &lt;&gt; '+q(expected).replace('"','&quot;')+']'
    body+=f'<If DisplayName="Elvárt eredmény ellenőrzése" Condition="{cond}"><If.Then><Sequence DisplayName="Teszt hiba"><Throw Exception="[New System.InvalidOperationException(&quot;Regression mismatch&quot;)]"/></Sequence></If.Then></If>\n'
    body+='<ui:LogMessage DisplayName="Teszt eredménye" Level="Info" Message='+q('["PASS|'+(raw or '(blank)')+'|" & eredmeny]')+'/>\n'
workflow('Validation_Regression',body+'</Sequence>')
print('Shared TryParse workflow, interactive repair and8-case actual-workflow harness authored')
