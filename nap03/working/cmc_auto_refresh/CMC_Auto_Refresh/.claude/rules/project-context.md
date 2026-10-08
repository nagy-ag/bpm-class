# Project context

Entry: Main.xaml, Windows/VisualBasic. Dependencies owned by official CLI. Workbook is a working copy with a native local-JSON Power Query. The source fetch lives at nap03/working/fetch_cmc_power_query.py and uses bpa_access.py. Refresh does not send workbook data externally. Native Excel lifecycle is isolated; it never kills existing Excel processes. No macros, UI Automation, browser targets, login automation, or persistent local schedule. Run once per requested refresh; verify saved data against the fetched JSON.
