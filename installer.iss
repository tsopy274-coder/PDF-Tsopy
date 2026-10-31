; installer.iss — Inno Setup script για HarisPDF
; Ανοίγει με Inno Setup Compiler

#define MyAppName "HarisPDF"
#define MyAppVersion "1.0"
#define MyAppPublisher "Haris Tsopelas"
#define MyAppURL "https://github.com/tsopy274-coder/PDF-Tsopy"
#define MyAppExeName "PDF-Tsopy.exe"
#define MySourceDir "D:\Deepseek skipartner\PDF-Tsopy-main\dist\PDF-Tsopy"
#define MyIconFile "D:\Deepseek skipartner\PDF-Tsopy-main\assets\logo\PDF-by-tsopy.ico"

[Setup]
AppId={{B8F4E1A2-3C5D-4E6F-9A1B-2C3D4E5F6A7B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=installer_output
OutputBaseFilename=HarisPDF-Setup-{#MyAppVersion}
SetupIconFile={#MyIconFile}
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64compatible
ChangesAssociations=yes

[Languages]
Name: "greek"; MessagesFile: "translations\Greek.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "{#MySourceDir}\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#MySourceDir}\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#MyIconFile}"; DestDir: "{app}"; DestName: "PDF-by-tsopy.ico"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{#MyIconFile}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{#MyIconFile}"; Tasks: desktopicon

[Registry]
Root: HKCR; Subkey: ".pdf"; ValueType: string; ValueName: ""; ValueData: "PDF-Tsopy.pdf"; Flags: uninsdeletevalue
Root: HKCR; Subkey: "PDF-Tsopy.pdf"; ValueType: string; ValueName: ""; ValueData: "PDF Document (Tsopy)"; Flags: uninsdeletekey
Root: HKCR; Subkey: "PDF-Tsopy.pdf\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\PDF-by-tsopy.ico,0"
Root: HKCR; Subkey: "PDF-Tsopy.pdf\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKCR; Subkey: ".pdf\OpenWithProgids"; ValueType: none; ValueName: "PDF-Tsopy.pdf"; Flags: uninsdeletevalue

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Code]
var
  PasswordPage: TInputQueryWizardPage;
  ShowPasswordCheck: TNewCheckBox;

procedure ShowPasswordCheckClick(Sender: TObject);
begin
  PasswordPage.Edits[0].Password := not ShowPasswordCheck.Checked;
end;

procedure InitializeWizard;
begin
  PasswordPage := CreateInputQueryPage(wpWelcome,
    'Επαλήθευση Κωδικού',
    'Εισάγετε τον κωδικό που λάβατε',
    'Ο κωδικός είναι απαραίτητος για την εγκατάσταση.');

  PasswordPage.Add('Κωδικός:', True);

  ShowPasswordCheck := TNewCheckBox.Create(WizardForm);
  ShowPasswordCheck.Parent := PasswordPage.Surface;
  ShowPasswordCheck.Top := PasswordPage.Edits[0].Top + PasswordPage.Edits[0].Height + ScaleY(8);
  ShowPasswordCheck.Height := ScaleY(ShowPasswordCheck.Height);
  ShowPasswordCheck.Caption := 'Εμφάνιση κωδικού';
  ShowPasswordCheck.OnClick := @ShowPasswordCheckClick;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  if CurPageID = PasswordPage.ID then
  begin
    if PasswordPage.Values[0] <> 'Haris&PDF2026!' then
    begin
      MsgBox('Λάθος κωδικός. Παρακαλώ δοκιμάστε ξανά.', mbError, MB_OK);
      Result := False;
    end;
  end;
end;