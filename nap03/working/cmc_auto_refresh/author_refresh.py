"""Author a finite, native UiPath Excel refresh from the CLI scaffold."""
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr
import shutil

root = Path(__file__).resolve().parents[3]
project = Path(__file__).parent / 'CMC_Auto_Refresh'
book = project / 'CMC_Auto_Refresh.xlsx'
if not book.exists():
    shutil.copy2(root / 'nap03/deliverables/CMC_arfolyamok_SOL.xlsx', book)
main = project / 'Main.xaml'
original = main.read_text(encoding='utf-8-sig')
code = fr'''Dim info As New System.Diagnostics.ProcessStartInfo("C:\Users\nagya\AppData\Local\Programs\Python\Python312\python.exe")
info.ArgumentList.Add("{root / 'nap03/working/fetch_cmc_power_query.py'}")
info.ArgumentList.Add("--solana")
info.UseShellExecute = False
info.CreateNoWindow = True
info.RedirectStandardOutput = True
info.RedirectStandardError = True
Using child As System.Diagnostics.Process = System.Diagnostics.Process.Start(info)
    Dim output = child.StandardOutput.ReadToEndAsync()
    Dim errors = child.StandardError.ReadToEndAsync()
    If Not child.WaitForExit(90000) Then
        child.Kill(True)
        Throw New System.TimeoutException("CMC fetch timed out")
    End If
    If child.ExitCode <> 0 Then Throw New System.InvalidOperationException("CMC fetch failed; no Excel refresh attempted")
End Using'''
# This short non-UI process bridge uses no credentials; fetch owns secure API access.
code = code.replace('    Dim errors = child.StandardError.ReadToEndAsync()\n', '    child.StandardError.ReadToEndAsync()\n')
prefix = original[:original.index('    <Sequence DisplayName="Main Sequence"')]
prefix = prefix.replace('xmlns:x=', 'xmlns:ui="http://schemas.uipath.com/workflow/activities"\nxmlns:s="clr-namespace:System;assembly=System.Private.CoreLib"\nxmlns:scg="clr-namespace:System.Collections.Generic;assembly=System.Private.CoreLib"\nxmlns:ue="clr-namespace:UiPath.Excel;assembly=UiPath.Excel.Activities"\nxmlns:excel="clr-namespace:UiPath.Excel.Activities.Business;assembly=UiPath.Excel.Activities"\nxmlns:x=')
prefix = prefix.replace('<AssemblyReference>System.Net.Mail</AssemblyReference>', '<AssemblyReference>System.Net.Mail</AssemblyReference>\n<AssemblyReference>System.Diagnostics.Process</AssemblyReference>\n<AssemblyReference>UiPath.Excel.Activities</AssemblyReference>')
body = f'''<Sequence DisplayName="Fetch and refresh CMC workbook">
  <TryCatch DisplayName="Guard external fetch and native refresh">
    <TryCatch.Try><Sequence DisplayName="Fetch then refresh">
      <ui:InvokeCode DisplayName="Fetch credential-free CMC snapshot" Language="VBNet" Code={quoteattr(code)}>
        <ui:InvokeCode.Arguments><scg:Dictionary x:TypeArguments="x:String, Argument" /></ui:InvokeCode.Arguments>
      </ui:InvokeCode>
      <excel:ExcelProcessScopeX DisplayName="Isolated native Excel" ProcessMode="AlwaysCreateNew" ExistingProcessAction="None" FileConflictResolution="ThrowException" MacroSettings="DisableAll" DisplayAlerts="False" ShowExcelWindow="True">
        <excel:ExcelProcessScopeX.Body><ActivityAction x:TypeArguments="ui:IExcelProcess">
          <ActivityAction.Argument><DelegateInArgument x:TypeArguments="ui:IExcelProcess" Name="ExcelProcessScopeTag" /></ActivityAction.Argument>
          <Sequence DisplayName="Open working workbook">
            <excel:ExcelApplicationCard DisplayName="Use CMC working copy" WorkbookPath={quoteattr(str(book))} AutoSave="False" CreateNewFile="False" KeepExcelFileOpen="False" ResizeWindow="None">
              <excel:ExcelApplicationCard.Body><ActivityAction x:TypeArguments="ue:IWorkbookQuickHandle">
                <ActivityAction.Argument><DelegateInArgument x:TypeArguments="ue:IWorkbookQuickHandle" Name="Excel" /></ActivityAction.Argument>
                <Sequence DisplayName="Refresh and save">
                  <excel:RefreshDataConnectionsX DisplayName="Refresh native Power Query" Workbook="[Excel]" />
                  <excel:SaveExcelFileX DisplayName="Save refreshed workbook" Workbook="[Excel]" />
                </Sequence>
              </ActivityAction></excel:ExcelApplicationCard.Body>
            </excel:ExcelApplicationCard>
          </Sequence>
        </ActivityAction></excel:ExcelProcessScopeX.Body>
      </excel:ExcelProcessScopeX>
      <ui:LogMessage DisplayName="Refresh finished" Level="Info" Message="CMC fetch and native Excel refresh saved" />
    </Sequence></TryCatch.Try>
    <TryCatch.Catches><Catch x:TypeArguments="s:Exception"><ActivityAction x:TypeArguments="s:Exception">
      <ActivityAction.Argument><DelegateInArgument x:TypeArguments="s:Exception" Name="failure" /></ActivityAction.Argument>
      <Sequence DisplayName="Report and propagate failure"><ui:LogMessage DisplayName="Safe failure notice" Level="Error" Message="CMC refresh failed; inspect execution diagnostics" /><Rethrow DisplayName="Propagate refresh failure" /></Sequence>
    </ActivityAction></Catch></TryCatch.Catches>
  </TryCatch>
</Sequence>
</Activity>'''
main.write_text(prefix + body, encoding='utf-8')
print('Authored native Excel refresh workflow and copied original workbook')
