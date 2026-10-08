from pathlib import Path
from xml.sax.saxutils import quoteattr
import argparse

a=argparse.ArgumentParser();a.add_argument('--mini',action='store_true');args=a.parse_args()
p=Path(__file__).parent/'ExcelRobot'
base=Path(__file__).parents[2]/'nap01/working/Proba/Main.xaml'
r=base.read_text(encoding='utf-8').split('  <Sequence DisplayName=')[0]
r=r.replace('xmlns:ui=', 'xmlns:sd="clr-namespace:System.Data;assembly=System.Data.Common" xmlns:s="clr-namespace:System;assembly=System.Private.CoreLib" xmlns:ui=')
r=r.replace('<AssemblyReference>UiPath.System.Activities</AssemblyReference>','<AssemblyReference>UiPath.System.Activities</AssemblyReference><AssemblyReference>UiPath.Excel.Activities</AssemblyReference>')
name='Classify_150000' if args.mini else 'Main'; threshold=150000 if args.mini else 100000
output='ugyfelek_minositve_v2.xlsx' if args.mini else 'ugyfelek_minositve.xlsx'
r=r.replace('x:Class="Main"',f'x:Class="{name}"')
def protect(body,label):
    return f'''<TryCatch DisplayName="{label}"><TryCatch.Try><Sequence DisplayName="{label} – művelet">{body}</Sequence></TryCatch.Try><TryCatch.Catches><Catch x:TypeArguments="s:Exception"><ActivityAction x:TypeArguments="s:Exception"><ActivityAction.Argument><DelegateInArgument x:TypeArguments="s:Exception" Name="exception"/></ActivityAction.Argument><Sequence DisplayName="Naplózás és leállás"><ui:LogMessage DisplayName="Fájlművelet hiba" Level="Error" Message="[exception.ToString()]"/><Rethrow/></Sequence></ActivityAction></Catch></TryCatch.Catches></TryCatch>'''
read='<ui:ReadRange DisplayName="Ügyfelek beolvasása" WorkbookPath="input/ugyfelek.xlsx" SheetName="Ugyfelek" Range="[String.Empty]" AddHeaders="True" DataTable="[dt]"/>'
write=f'<ui:WriteRange DisplayName="Minősített ügyfelek mentése" WorkbookPath="output/{output}" SheetName="Ugyfelek" StartingCell="A1" AddHeaders="True" DataTable="[dt]"/>'
body='''<Sequence DisplayName="Ügyfélminősítés">
<Sequence.Variables><Variable x:TypeArguments="sd:DataTable" Name="dt"/></Sequence.Variables>
'''+f'''<If DisplayName="Új kimenet ellenőrzése" Condition="[System.IO.File.Exists(&quot;output/{output}&quot;)]"><If.Then><Sequence><Throw Exception="[New System.IO.IOException(&quot;Output already exists; preserve it and choose a fresh output before rerun.&quot;)]"/></Sequence></If.Then></If>
'''+protect(read,'Munkafüzet beolvasása')+'''
<ui:LogMessage DisplayName="Beolvasott sorok" Level="Info" Message="[dt.Rows.Count.ToString() &amp; &quot; ügyfelet olvastam be.&quot;]"/>
<If DisplayName="Tizenkét ügyfél ellenőrzése" Condition="[dt.Rows.Count &lt;&gt; 12]"><If.Then><Sequence><Throw Exception="[New UiPath.Core.BusinessRuleException(&quot;Expected12customer rows.&quot;)]"/></Sequence></If.Then></If>
<ui:ForEachRow DisplayName="Minősítés soronként" DataTable="[dt]"><ui:ForEachRow.Body><ActivityAction x:TypeArguments="sd:DataRow"><ActivityAction.Argument><DelegateInArgument x:TypeArguments="sd:DataRow" Name="CurrentRow"/></ActivityAction.Argument><Sequence DisplayName="Sor minősítése"><Assign DisplayName="Minősítés megadása"><Assign.To><OutArgument x:TypeArguments="x:Object">[CurrentRow("Minosites")]</OutArgument></Assign.To><Assign.Value><InArgument x:TypeArguments="x:Object">'''+f'''[If(CDbl(CurrentRow(&quot;EvesDij&quot;)) &gt;= {threshold}, &quot;kiemelt&quot;, &quot;normál&quot;)]</InArgument></Assign.Value></Assign></Sequence></ActivityAction></ui:ForEachRow.Body></ui:ForEachRow>
'''+protect(write,'Munkafüzet mentése')+f'''
<ui:LogMessage DisplayName="Sikeres mentés" Level="Info" Message="Kész: {output}; threshold={threshold}; rows=12"/>
<ui:MessageBox DisplayName="Kész munkafüzet" Text="Kész: {output}" AutoCloseAfter="00:00:00"/>
</Sequence></Activity>'''
(p/(name+'.xaml')).write_text(r+body,encoding='utf-8')
print(f'{name}: Workbook read/ForEachRow Assign/write authored; threshold{threshold}')
