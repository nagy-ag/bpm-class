"""Prepare offline UiPath artifacts; never open, capture, or operate a browser."""
from copy import deepcopy
from pathlib import Path
import xml.etree.ElementTree as ET

BASE = Path(__file__).resolve().parent
PROJECT = BASE / "BPA_Setup_Smoke"
NS = {
    "": "http://schemas.microsoft.com/netfx/2009/xaml/activities",
    "x": "http://schemas.microsoft.com/winfx/2006/xaml",
    "ui": "http://schemas.uipath.com/workflow/activities",
    "uix": "http://schemas.uipath.com/workflow/activities/uix",
    "sap": "http://schemas.microsoft.com/netfx/2009/xaml/activities/presentation",
    "sap2010": "http://schemas.microsoft.com/netfx/2010/xaml/activities/presentation",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "scg": "clr-namespace:System.Collections.Generic;assembly=System.Private.CoreLib",
    "sco": "clr-namespace:System.Collections.ObjectModel;assembly=System.Private.CoreLib",
    "sd": "clr-namespace:System.Data;assembly=System.Data.Common",
    "s": "clr-namespace:System;assembly=System.Private.CoreLib",
}
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)


def q(name):
    prefix, local = name.split(":", 1) if ":" in name else ("", name)
    return "{" + NS[prefix] + "}" + local


counter = 0


def node(name, **attrs):
    global counter
    element = ET.Element(q(name), attrs)
    if "DisplayName" in attrs:
        counter += 1
        element.set(q("sap2010:WorkflowViewState.IdRef"), name.split(":")[-1] + "_" + str(counter))
    return element


def sub(parent, name, text=None, **attrs):
    result = node(name, **attrs)
    parent.append(result)
    if text is not None:
        result.text = text
    return result


def root(name):
    source = ET.parse(PROJECT / "Portal_Input_Preview.xaml").getroot()
    result = node("Activity")
    result.attrib.update(source.attrib)
    result.set(q("x:Class"), name)
    result.set(q("sap2010:WorkflowViewState.IdRef"), name + "_1")
    # Prefixes used in XAML type strings do not auto-serialize in ElementTree.
    for prefix in ("scg", "sd", "s", "sap"):
        result.set("xmlns:" + prefix, NS[prefix])
    for child in source:
        if child.tag in (q("TextExpression.NamespacesForImplementation"), q("TextExpression.ReferencesForImplementation")):
            result.append(deepcopy(child))
    refs = result.find(q("TextExpression.ReferencesForImplementation"))[0]
    for assembly in ("System.Collections", "System.Text.RegularExpressions"):
        if not any(item.text == assembly for item in refs):
            sub(refs, "AssemblyReference", assembly)
    return result


def save(name, element):
    ET.indent(element, space="  ")
    ET.ElementTree(element).write(PROJECT / (name + ".xaml"), encoding="utf-8", xml_declaration=True)


def variable(parent, name, kind="x:String", default=None):
    attrs = {q("x:TypeArguments"): kind, "Name": name}
    if default is not None:
        attrs["Default"] = default
    sub(parent, "Variable", **attrs)


def assign(parent, name, expr, kind="x:String"):
    activity = sub(parent, "Assign", DisplayName="Set " + name)
    sub(sub(activity, "Assign.To"), "OutArgument", "[" + name + "]", **{q("x:TypeArguments"): kind})
    sub(sub(activity, "Assign.Value"), "InArgument", "[" + expr + "]", **{q("x:TypeArguments"): kind})


def guard(parent, condition, message):
    activity = sub(parent, "If", Condition="[" + condition + "]", DisplayName="Guard: " + message)
    body = sub(sub(activity, "If.Then"), "Sequence", DisplayName="Fail visibly")
    sub(body, "Throw", Exception='[New System.InvalidOperationException("' + message + '")]', DisplayName="Stop: " + message)


def code(parent, label, vb, args):
    activity = sub(parent, "ui:InvokeCode", DisplayName=label, Code=vb)
    collection = sub(activity, "ui:InvokeCode.Arguments")
    for name, expression, kind in args:
        sub(collection, "InArgument", "[" + expression + "]", **{q("x:Key"): name, q("x:TypeArguments"): kind})
    return activity


def log(parent, event, detail='String.Empty', policy="policy", case_id="caseId"):
    activity = sub(parent, "ui:InvokeWorkflowFile", DisplayName="Log " + event, WorkflowFileName="Portal_Log.xaml", UnSafe="False")
    collection = sub(activity, "ui:InvokeWorkflowFile.Arguments")
    values = {"in_RunDir": "runDir", "in_Event": '"' + event + '"', "in_Policy": policy, "in_CaseId": case_id, "in_Detail": detail}
    for name, expression in values.items():
        sub(collection, "InArgument", "[" + expression + "]", **{q("x:Key"): name, q("x:TypeArguments"): "x:String"})


def build_logger():
    doc = root("Portal_Log")
    members = node("x:Members")
    for name in ("in_RunDir", "in_Event", "in_Policy", "in_CaseId", "in_Detail"):
        sub(members, "x:Property", Name=name, Type="InArgument(x:String)")
    doc.insert(0, members)
    sequence = sub(doc, "Sequence", DisplayName="Persist one credential-free progress event")
    vb = '''If String.IsNullOrWhiteSpace(folder) Then Throw New ArgumentException("Missing evidence folder")
System.IO.Directory.CreateDirectory(folder)
Dim quote As String = ChrW(34)
Dim fields As String() = {DateTimeOffset.UtcNow.ToString("o"), eventName, policyNumber, claimId, detail}
Dim encoded As New System.Collections.Generic.List(Of String)
For Each value As String In fields
    encoded.Add(quote & If(value, String.Empty).Replace(quote, quote & quote).Replace(vbCr, " ").Replace(vbLf, " ") & quote)
Next
Dim line As String = String.Join(",", encoded)
Dim path As String = System.IO.Path.Combine(folder, "events.csv")
Dim utf8 As New System.Text.UTF8Encoding(False)
If Not System.IO.File.Exists(path) Then System.IO.File.WriteAllText(path, "utc,event,policy,case_id,detail" & Environment.NewLine, utf8)
System.IO.File.AppendAllText(path, line & Environment.NewLine, utf8)
System.IO.File.WriteAllText(System.IO.Path.Combine(folder, "last_event.txt"), line & Environment.NewLine, utf8)'''
    code(sequence, "Append timestamp, event, fictional policy and actual case ID", vb, [
        ("folder", "in_RunDir", "x:String"), ("eventName", "in_Event", "x:String"),
        ("policyNumber", "in_Policy", "x:String"), ("claimId", "in_CaseId", "x:String"), ("detail", "in_Detail", "x:String")])
    sub(sequence, "ui:LogMessage", Level="Info", DisplayName="Show same progress in Studio Output", Message='[in_Event & " | policy=" & in_Policy & " | case=" & in_CaseId & " | " & in_Detail]')
    save("Portal_Log", doc)


def build_logger_smoke():
    doc = root("Portal_Log_Smoke")
    sequence = sub(doc, "Sequence", DisplayName="File-only logger smoke - no browser")
    variables = sub(sequence, "Sequence.Variables")
    variable(variables, "runDir")
    variable(variables, "policy", default="LOGGER-SMOKE")
    variable(variables, "caseId", default="NOT-A-PORTAL-CASE")
    assign(sequence, "runDir", 'System.IO.Path.Combine("' + BASE.as_posix() + '", "portal_runs", "logger_smoke_" & System.Guid.NewGuid().ToString("N"))')
    log(sequence, "logger_smoke_started", '"File-only check, not portal execution"')
    log(sequence, "logger_smoke_escaped", '"Comma, quote " & ChrW(34) & " Hungarian: vízkár"')
    log(sequence, "logger_smoke_complete", '"Expected exactly three events"')
    save("Portal_Log_Smoke", doc)


def screenshot(parent, filename, label, best_effort=False):
    # Target omitted intentionally: inside the application card, captures its window.
    return sub(parent, "uix:NTakeScreenshot", DisplayName=label, Version="V5", HealingAgentBehavior="Disabled", SaveScreenshotTo="File", FileName='[System.IO.Path.Combine(runDir, "' + filename + '")]', FileNameMode="None", ContinueOnError=str(best_effort))


def build_portal_stub():
    doc = root("Portal_Logged_Trial")
    sequence = sub(doc, "Sequence", DisplayName="One-row trial - target indication required before Run File")
    variables = sub(sequence, "Sequence.Variables")
    for name in ("runDir", "policy", "caseId", "stage"):
        variable(variables, name, default="" if name != "stage" else "initializing")
    variable(variables, "targetsConfigured", "x:Boolean", "False")
    variable(variables, "dt", "sd:DataTable")
    assign(sequence, "runDir", 'System.IO.Path.Combine("' + BASE.as_posix() + '", "portal_runs", DateTime.UtcNow.ToString("yyyyMMdd_HHmmss") & "_" & Guid.NewGuid().ToString("N"))')
    log(sequence, "run_started", '"One-row trial; no automatic retry"')
    guard(sequence, "Not targetsConfigured", "Targets are not indicated. Follow PORTAL_LOGGED_HANDOFF.md before running.")
    source = ET.parse(PROJECT / "Portal_Input_Preview.xaml").getroot()
    read = deepcopy(source.find('.//' + q("ui:ReadRange")))
    read.attrib.pop(q("sap:VirtualizedContainerService.HintSize"), None)
    read.set("DisplayName", "Read exactly bejelentesek A1:F2 with headers")
    sequence.append(read)
    guard(sequence, "dt Is Nothing OrElse dt.Rows.Count <> 1", "Expected exactly one input row")
    for name in ("kotvenyszam", "kartipus", "karesemeny_datum", "becsult_osszeg", "karleiras", "ugyszam"):
        guard(sequence, 'Not dt.Columns.Contains("' + name + '")', "Missing input column " + name)
    assign(sequence, "policy", 'dt.Rows(0)("kotvenyszam").ToString()')
    guard(sequence, 'Not System.Text.RegularExpressions.Regex.IsMatch(policy, "^TR-[0-9]{6}$")', "Invalid policy format")
    guard(sequence, 'Not String.IsNullOrWhiteSpace(dt.Rows(0)("ugyszam").ToString())', "Input already contains a case ID; reconcile before another run")
    sub(sequence, "ui:WriteRange", DisplayName="Save actual input snapshot without modifying original", WorkbookPath='[System.IO.Path.Combine(runDir, "input_snapshot.xlsx")]', SheetName="Input", DataTable="[dt]", AddHeaders="True")
    log(sequence, "input_read", '"One row saved in input_snapshot.xlsx"')
    # Atomic reservation survives success/failure, so re-running cannot silently duplicate.
    code(sequence, "Reserve fictional policy once; manual reconciliation before retry", '''Dim folder As String = System.IO.Path.Combine(root, "reservations")
System.IO.Directory.CreateDirectory(folder)
Dim path As String = System.IO.Path.Combine(folder, policyNumber & ".lock")
Using stream As New System.IO.FileStream(path, System.IO.FileMode.CreateNew, System.IO.FileAccess.Write, System.IO.FileShare.None)
    Using writer As New System.IO.StreamWriter(stream)
        writer.WriteLine(runFolder)
    End Using
End Using''', [("root", '"' + (BASE / "portal_runs").as_posix() + '"', "x:String"), ("policyNumber", "policy", "x:String"), ("runFolder", "runDir", "x:String")])
    log(sequence, "policy_reserved", '"Keep reservation until saved rows are reconciled"')
    card = sub(sequence, "uix:NApplicationCard", AttachMode="ByInstance", DisplayName="Use user-attached Brave portal - never open or close it", HealingAgentBehavior="Disabled", OpenMode="Never", CloseMode="Never", ScopeGuid="52e595f1-111f-455b-a1d8-7baabf5504d8", Version="V2")
    action = sub(sub(card, "uix:NApplicationCard.Body"), "ActivityAction", **{q("x:TypeArguments"): "x:Object"})
    sub(sub(action, "ActivityAction.Argument"), "DelegateInArgument", Name="WSSessionData", **{q("x:TypeArguments"): "x:Object"})
    body = sub(action, "Sequence", DisplayName="Do")
    loop = sub(body, "ui:ForEach", DisplayName="For each input row (guarded to one)", Values="[dt.Rows]", **{q("x:TypeArguments"): "sd:DataRow"})
    each = sub(sub(loop, "ui:ForEach.Body"), "ActivityAction", **{q("x:TypeArguments"): "sd:DataRow"})
    sub(sub(each, "ActivityAction.Argument"), "DelegateInArgument", Name="CurrentRow", **{q("x:TypeArguments"): "sd:DataRow"})
    transaction = sub(each, "Sequence", DisplayName="One fictional claim with durable checkpoints")
    attempt = sub(transaction, "TryCatch", DisplayName="Record uncertainty and stop; never retry submit")
    work = sub(sub(attempt, "TryCatch.Try"), "Sequence", DisplayName="Fill, submit once, capture confirmation")
    screenshot(work, "01_before.png", "Capture attached portal before filling")
    for number, label, column, activity in [
        (1, "Kötvényszám", "kotvenyszam", "NTypeInto"),
        (2, "Kár típusa", "kartipus", "NSelectItem"),
        (3, "Káresemény dátuma", "karesemeny_datum", "NTypeInto"),
        (4, "Becsült összeg", "becsult_osszeg", "NTypeInto"),
        (5, "A kár rövid leírása", "karleiras", "NTypeInto"),
    ]:
        assign(work, "stage", '"fill_' + column + '"')
        attrs = dict(DisplayName="TODO Indicate " + str(number) + " - " + label, Version="V5", HealingAgentBehavior="Disabled", ContinueOnError="False", Timeout="10")
        attrs["Text" if activity == "NTypeInto" else "Item"] = '[CurrentRow("' + column + '").ToString()]'
        if activity == "NTypeInto":
            attrs.update(ActivateBefore="True", ClickBeforeMode="Single", EmptyFieldMode="MultiLine" if column == "karleiras" else "SingleLine")
        sub(work, "uix:" + activity, **attrs)
        log(work, "field_activity_completed", '"' + column + '"')
    screenshot(work, "02_filled.png", "Capture filled portal before submit")
    assign(work, "stage", '"submit_attempted"')
    log(work, "submit_attempted", '"A click may commit; do not retry without readback"')
    sub(work, "uix:NClick", DisplayName="TODO Indicate 6 - Bejelentés rögzítése", Version="V5", HealingAgentBehavior="Disabled", ActivateBefore="True", ClickType="Single", KeyModifiers="None", MouseButton="Left", ContinueOnError="False", Timeout="10")
    check = sub(work, "uix:NCheckState", DisplayName="TODO Indicate 7 - A bejelentést rögzítettük", Version="V5", HealingAgentBehavior="Disabled", Timeout="10", CheckVisibility="True")
    success = sub(sub(check, "uix:NCheckState.IfExists"), "Sequence", DisplayName="Confirmation appeared - still verify saved data after run")
    assign(success, "stage", '"confirmation_seen"')
    log(success, "confirmation_seen")
    screenshot(success, "03_confirmation.png", "Capture confirmation and actual generated case number")
    sub(success, "uix:NGetText", DisplayName="TODO Indicate 8 - generated K-GY case number", Version="V5", HealingAgentBehavior="Disabled", TextString="[caseId]", ContinueOnError="False", Timeout="10")
    guard(success, 'Not System.Text.RegularExpressions.Regex.IsMatch(caseId.Trim(), "^K-GY-[0-9]+$")', "Case ID readback is missing or invalid; outcome requires reconciliation")
    assign(success, "caseId", "caseId.Trim()")
    log(success, "case_id_read")
    sub(success, "ui:WriteTextFile", DisplayName="Save actual generated case ID immediately", FileName='[System.IO.Path.Combine(runDir, "case_id.txt")]', Text="[caseId]")
    assign(success, "stage", '"return_to_form"')
    sub(success, "uix:NClick", DisplayName="TODO Indicate 9 - Új bejelentés rögzítése", Version="V5", HealingAgentBehavior="Disabled", ActivateBefore="True", ClickType="Single", KeyModifiers="None", MouseButton="Left", ContinueOnError="False", Timeout="10")
    log(success, "ui_sequence_complete", '"Await exported saved-record verification; not yet verified"')
    failure = sub(sub(check, "uix:NCheckState.IfNotExists"), "Sequence", DisplayName="Confirmation absent - do not resubmit")
    sub(failure, "Throw", DisplayName="Stop on absent confirmation", Exception='[New System.Exception("A bejelentés nem mentődött; ellenőrizd a portál hibaüzenetét. Submission outcome is uncertain; do not retry.")]')
    catch = sub(sub(attempt, "TryCatch.Catches"), "Catch", **{q("x:TypeArguments"): "s:Exception"})
    handler = sub(catch, "ActivityAction", **{q("x:TypeArguments"): "s:Exception"})
    sub(sub(handler, "ActivityAction.Argument"), "DelegateInArgument", Name="exception", **{q("x:TypeArguments"): "s:Exception"})
    recovery = sub(handler, "Sequence", DisplayName="Persist failure without replaying any portal action")
    log(recovery, "stopped_requires_review", '"stage=" & stage & "; type=" & exception.GetType().FullName')
    screenshot(recovery, "error.png", "Best-effort capture of attached portal only", best_effort=True)
    sub(recovery, "Rethrow", DisplayName="Keep original fault and stop")
    # Reuse only the existing user-indicated application descriptor, unchanged.
    original = ET.parse(PROJECT / "Portal_Brave_Check.xaml").getroot()
    target = original.find('.//' + q("uix:NApplicationCard.TargetApp"))
    card.append(deepcopy(target))
    log(sequence, "run_finished_pending_readback", '"Export own practice rows and compare before claiming success"')
    save("Portal_Logged_Trial", doc)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=("logger", "portal"))
    selected = parser.parse_args().stage
    if selected == "logger":
        build_logger()
        build_logger_smoke()
    else:
        build_portal_stub()
    print("Prepared " + selected + " artifacts offline; no browser execution.")
