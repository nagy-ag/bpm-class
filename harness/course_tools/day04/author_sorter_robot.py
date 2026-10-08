"""Author genuine lesson file activities; no sorting is performed by this helper."""
from pathlib import Path
from xml.sax.saxutils import quoteattr
import argparse

ap=argparse.ArgumentParser();ap.add_argument('--mini',action='store_true');a=ap.parse_args()
p=Path(__file__).parent/'Fajlrendezo';name='Sort_With_Images' if a.mini else 'Main'
r=(Path(__file__).parents[2]/'nap01/working/Proba/Main.xaml').read_text(encoding='utf-8').split('  <Sequence DisplayName=')[0]
r=r.replace('x:Class="Main"',f'x:Class="{name}"').replace('xmlns:ui=','xmlns:si="clr-namespace:System.IO;assembly=System.Private.CoreLib" xmlns:s="clr-namespace:System;assembly=System.Private.CoreLib" xmlns:ui=')
def q(s):return quoteattr(s)
def protect(body,label):
 return f'''<TryCatch DisplayName="{label}"><TryCatch.Try><Sequence DisplayName="{label} – művelet">{body}</Sequence></TryCatch.Try><TryCatch.Catches><Catch x:TypeArguments="s:Exception"><ActivityAction x:TypeArguments="s:Exception"><ActivityAction.Argument><DelegateInArgument x:TypeArguments="s:Exception" Name="exception"/></ActivityAction.Argument><Sequence DisplayName="Hiba rögzítése"><ui:LogMessage DisplayName="Fájlrendezési hiba" Level="Error" Message="[exception.ToString()]"/><Rethrow/></Sequence></ActivityAction></Catch></TryCatch.Catches></TryCatch>'''
rules=[('.pdf','PDF'),('.xlsx','Excel'),('.docx','Word')]+([('.png','Kepek')] if a.mini else [])
folders=''.join(protect(f'<ui:CreateDirectory DisplayName="{folder} mappa" Path={q("[System.IO.Path.Combine(exerciseRoot, "+chr(34)+folder+chr(34)+")] ".strip())} ContinueOnError="False"/>',f'{folder} mappa létrehozása') for _,folder in rules)
conditions=''
for ext,folder in rules:
 destination=f'[System.IO.Path.Combine(exerciseRoot, "{folder}", CurrentFile.Name)]'
 move=f'<ui:MoveFile DisplayName="{folder} fájl áthelyezése" Path="[CurrentFile.FullName]" Destination={q(destination)} Overwrite="False" ContinueOnError="False"/>'
 conditions+=f'''<If DisplayName="{ext} szabály" Condition={q('[CurrentFile.Extension.ToLower() = "'+ext+'"]')}><If.Then><Sequence DisplayName="{folder} áthelyezés">
{protect(move,folder+' fájlmozgatás')}
<Assign DisplayName="Mozgatások számlálása"><Assign.To><OutArgument x:TypeArguments="x:Int32">[moved]</OutArgument></Assign.To><Assign.Value><InArgument x:TypeArguments="x:Int32">[moved+1]</InArgument></Assign.Value></Assign>
<ui:LogMessage DisplayName="{folder} mozgatás naplója" Level="Info" Message={q('["MOVED|'+folder+'|" & CurrentFile.Name]')}/>
</Sequence></If.Then></If>'''
body='''<Sequence DisplayName="Gyakorlófájlok rendezése"><Sequence.Variables><Variable x:TypeArguments="x:String" Name="exerciseRoot"/><Variable x:TypeArguments="x:Int32" Name="moved" Default="0"/></Sequence.Variables>
<Assign DisplayName="Gyakorlómappa abszolút útvonala"><Assign.To><OutArgument x:TypeArguments="x:String">[exerciseRoot]</OutArgument></Assign.To><Assign.Value><InArgument x:TypeArguments="x:String">[System.IO.Path.GetFullPath("exercise/gyakorlo_mappa")]</InArgument></Assign.Value></Assign>
<If DisplayName="Létező elszigetelt forrás ellenőrzése" Condition="[Not System.IO.Directory.Exists(exerciseRoot)]"><If.Then><Sequence><Throw Exception="[New System.IO.DirectoryNotFoundException(&quot;Extract the lesson ZIP into this project exercise folder first.&quot;)]"/></Sequence></If.Then></If>
'''+folders+'''<ui:ForEachFileX DisplayName="Csak felső mappa fájljai" Folder="[exerciseRoot]" Filter="*" IncludeSubDirectories="False" SkipFolderWithoutPermission="False" OrderBy="NameAscFirst"><ui:ForEachFileX.Body><ActivityAction x:TypeArguments="si:FileInfo, x:Int32"><ActivityAction.Argument1><DelegateInArgument x:TypeArguments="si:FileInfo" Name="CurrentFile"/></ActivityAction.Argument1><ActivityAction.Argument2><DelegateInArgument x:TypeArguments="x:Int32" Name="CurrentIndex"/></ActivityAction.Argument2><Sequence DisplayName="Kiterjesztések vizsgálata">'''+conditions+'''</Sequence></ActivityAction></ui:ForEachFileX.Body></ui:ForEachFileX>
<ui:LogMessage DisplayName="Összes mozgatás" Level="Info" Message="[&quot;SORT_COMPLETE|moved=&quot; &amp; moved.ToString()]"/>
</Sequence></Activity>'''
(p/(name+'.xaml')).write_text(r+body,encoding='utf-8');print(name+': real file activities authored')
