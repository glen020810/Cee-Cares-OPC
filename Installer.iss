[Setup]
AppName=EMS Payroll System
AppVersion=1.0
DefaultDirName={pf}\EMS Payroll System
DefaultGroupName=EMS Payroll System
OutputBaseFilename=EMS_Installer
Compression=lzma
SolidCompression=yes
DisableWelcomePage=no
WizardStyle=modern

[Files]
; ✅ PyInstaller output folder
Source: "dist\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

; ✅ Include databases (only if outside dist\login)
Source: "emp_admin.db"; DestDir: "{app}"; Flags: ignoreversion
Source: "employees.db"; DestDir: "{app}"; Flags: ignoreversion
Source: "database.db"; DestDir: "{app}"; Flags: ignoreversion

; ✅ Include other assets or config files
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion

; ✅ Optional: include QSS files if not bundled in dist
Source: "styles\*.qss"; DestDir: "{app}\styles"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "icons\*"; DestDir: "{app}\icons"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "images\*"; DestDir: "{app}\images"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\EMS Payroll System"; Filename: "{app}\login.exe"
Name: "{commondesktop}\EMS Payroll System"; Filename: "{app}\login.exe"; Tasks: desktopicon
Name: "{group}\Uninstall EMS Payroll System"; Filename: "{uninstallexe}"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

[Run]
Filename: "{app}\login.exe"; Description: "Launch EMS Payroll System"; Flags: nowait postinstall skipifsilent
