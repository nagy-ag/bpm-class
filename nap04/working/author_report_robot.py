"""Author the lesson's native Office activity route, never generate its outputs."""
from pathlib import Path
from xml.sax.saxutils import quoteattr
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('--records', type=int, choices=[12, 6], default=12)
ap.add_argument('--placeholder', default='TODO: saved content placeholder')
a = ap.parse_args()
p = Path(__file__).parent / 'RiportRobot'
name = 'Main' if a.records == 12 else 'Report_6'
folder = f'reports_{a.records}'
r = (Path(__file__).parents[2] / 'nap01/working/Proba/Main.xaml').read_text(encoding='utf-8').split('  <Sequence DisplayName=')[0]
r = r.replace('x:Class="Main"', f'x:Class="{name}"')
r = r.replace('xmlns:ui=', 'xmlns:ue="clr-namespace:UiPath.Excel;assembly=UiPath.Excel.Activities" xmlns:ueab="clr-namespace:UiPath.Excel.Activities.Business;assembly=UiPath.Excel.Activities" xmlns:s="clr-namespace:System;assembly=System.Private.CoreLib" xmlns:ui=')
r = r.replace('<AssemblyReference>UiPath.System.Activities</AssemblyReference>', '<AssemblyReference>UiPath.System.Activities</AssemblyReference><AssemblyReference>UiPath.Excel.Activities</AssemblyReference><AssemblyReference>UiPath.Presentations.Activities</AssemblyReference>')
def q(s): return quoteattr(s)
def protect(body, label):
    return f'''<TryCatch DisplayName="{label}"><TryCatch.Try><Sequence DisplayName="{label} – műveletek">{body}</Sequence></TryCatch.Try><TryCatch.Catches><Catch x:TypeArguments="s:Exception"><ActivityAction x:TypeArguments="s:Exception"><ActivityAction.Argument><DelegateInArgument x:TypeArguments="s:Exception" Name="exception"/></ActivityAction.Argument><Sequence DisplayName="Hiba naplózása"><ui:LogMessage Level="Error" DisplayName="Office hiba" Message="[exception.ToString()]"/><Rethrow/></Sequence></ActivityAction></Catch></TryCatch.Catches></TryCatch>'''
office = f'''
<ueab:ExcelApplicationCard DisplayName="Riport munkafüzet" WorkbookPath="{folder}/Riport_adatok.xlsx" CreateNewFile="False" AutoSave="True" KeepExcelFileOpen="False">
<ueab:ExcelApplicationCard.Body><ActivityAction x:TypeArguments="ue:IWorkbookQuickHandle"><ActivityAction.Argument><DelegateInArgument x:TypeArguments="ue:IWorkbookQuickHandle" Name="Excel"/></ActivityAction.Argument><Sequence DisplayName="Diagram és prezentáció">
<ueab:InsertExcelChartX DisplayName="Első {a.records} rekord diagramja" Range={q('[Excel.Sheet("us-500").Range("A1:B'+str(a.records+1)+'")]')} InsertIntoSheet={q('[Excel.Sheet("us-500")]')} ChartCategory="Column" ChartType="xlColumnClustered" ChartHeight="350" ChartWidth="640" Left="320" Top="20" InsertedChart="[diagram]"/>
<ueab:CopyChartToClipboardX DisplayName="Diagram a vágólapra" Chart="[diagram]" Action="CopyToClipboard"/>
<ui:PowerPointApplicationScope DisplayName="Riport prezentáció" PresentationPath="{folder}/Riport_eredmeny.pptx" AutoSave="True" CreateIfNotExists="False"><ui:PowerPointApplicationScope.Body><ActivityAction x:TypeArguments="ui:IPresentationQuickHandle"><ActivityAction.Argument><DelegateInArgument x:TypeArguments="ui:IPresentationQuickHandle" Name="PowerPoint"/></ActivityAction.Argument><Sequence DisplayName="Beillesztés a kilencedik diára">
<ui:PasteIntoSlide DisplayName="Diagram a tartalom-helyőrzőbe" Presentation="[PowerPoint]" SlideIndex="9" ShapeName={q(a.placeholder)} NewShapeName="BPA_{a.records}_rekord"/>
</Sequence></ActivityAction></ui:PowerPointApplicationScope.Body></ui:PowerPointApplicationScope>
</Sequence></ActivityAction></ueab:ExcelApplicationCard.Body></ueab:ExcelApplicationCard>
'''
body=f'''<Sequence DisplayName="Excel és PowerPoint riport">
<Sequence.Variables><Variable x:TypeArguments="ue:IChartRef" Name="diagram"/></Sequence.Variables>
<If DisplayName="Helyőrző konfigurálva" Condition={q('["'+a.placeholder+'".StartsWith("TODO:")]')}><If.Then><Sequence><Throw Exception="[New System.InvalidOperationException(&quot;Prepare slide9 layout and set actual content placeholder before execution.&quot;)]"/></Sequence></If.Then></If>
<If DisplayName="Új munkapéldány ellenőrzése" Condition={q('[System.IO.File.Exists("'+folder+'/run_started.lock")]')}><If.Then><Sequence><Throw Exception="[New System.IO.IOException(&quot;This copy has already started. Preserve outputs and use fresh copies before rerun.&quot;)]"/></Sequence></If.Then></If>
'''+protect(f'<ui:WriteTextFile DisplayName="Ismétlés elleni jelző" FileName="{folder}/run_started.lock" Encoding="utf-8" Text="Office run started; preserve files and reconcile before any retry."/>','Futás jelölése')+protect(office,'Office riport')+f'''<ui:LogMessage DisplayName="Riport kész" Level="Info" Message="Riport kész: {a.records} rekord; us-500 A1:B{a.records+1}; dia9."/>
</Sequence></Activity>'''
(p/(name+'.xaml')).write_text(r+body,encoding='utf-8')
print(f'{name}: native Office route authored; placeholder={a.placeholder}')
