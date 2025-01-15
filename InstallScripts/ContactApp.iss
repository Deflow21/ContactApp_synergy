[Setup]
AppName=ContactApp
AppVersion=1.0
DefaultDirName={commonpf}\ContactApp
DefaultGroupName=ContactApp
OutputBaseFilename=ContactAppSetup
Compression=lzma
SolidCompression=yes

[Files]
Source: "C:\Users\culic\ContactApp_synergy\dist\contacts_app.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\culic\ContactApp_synergy\ContactApp\*"; DestDir: "{app}\ContactApp"; Flags: recursesubdirs

[Icons]
Name: "{group}\ContactApp"; Filename: "{app}\contacts_app.exe"; Comment: "Запустить приложение"
Name: "{commondesktop}\ContactApp"; Filename: "{app}\contacts_app.exe"; Comment: "Запустить приложение"

[Run]
Filename: "{app}\contacts_app.exe"; Description: "Запустить приложение"; Flags: nowait
