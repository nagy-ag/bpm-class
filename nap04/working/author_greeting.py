"""Author course workflow from validated root plus documented activity shapes."""
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

p = Path(__file__).parent / 'Nap04_gyakorlas'
root = (p/'Main.xaml').read_text(encoding='utf-8').split('  <Sequence DisplayName=')[0]
def attr(s): return quoteattr(s)
def msg(s, name):
    return f'<ui:MessageBox DisplayName={attr(name)} Text={attr(s)} Caption="{{x:Null}}" ChosenButton="{{x:Null}}" AutoCloseAfter="00:00:00" />'
body = '''<Sequence DisplayName="Bemutatkozás és éves becslés – eredeti">
<Sequence.Variables><Variable x:TypeArguments="x:String" Name="nev"/><Variable x:TypeArguments="x:String" Name="darab"/></Sequence.Variables>
<ui:InputDialog DisplayName="Név bekérése" Title="Bemutatkozás" Label="Hogy hívnak?" IsPassword="False" TopMost="True"><ui:InputDialog.Result><OutArgument x:TypeArguments="x:String">[nev]</OutArgument></ui:InputDialog.Result></ui:InputDialog>
'''+msg('["Szia, " & nev & "! Ez az első robotod."]','Köszönés')+'''
<ui:InputDialog DisplayName="Napi e-mail darabszám" Title="Számoljunk" Label="Hány e-mailt írsz naponta?" IsPassword="False" TopMost="True"><ui:InputDialog.Result><OutArgument x:TypeArguments="x:String">[darab]</OutArgument></ui:InputDialog.Result></ui:InputDialog>
'''+msg('["Évente kb. " & (CInt(darab)*250).ToString() & " e-mail."]','Éves e-mail becslés – CInt')+'''
</Sequence>
</Activity>
'''
(p/'Greeting_Initial.xaml').write_text(root.replace('x:Class="Main"','x:Class="Greeting_Initial"')+body,encoding='utf-8')
print('Greeting_Initial authored; no execution claimed')
