; wowooai Desktop NSIS installer. Run makensis from repo root after
; building dist/win-unpacked (see scripts/pack/build_win.ps1).
; Usage: makensis /Dwowooai_VERSION=1.2.3 /DOUTPUT_EXE=dist\wowooai-Setup-1.2.3.exe scripts\pack\desktop.nsi

!include "MUI2.nsh"
!define MUI_ABORTWARNING
; Use custom icon from unpacked env (copied by build_win.ps1)
!define MUI_ICON "${UNPACKED}\icon.ico"
!define MUI_UNICON "${UNPACKED}\icon.ico"

!ifndef wowooai_VERSION
  !define wowooai_VERSION "0.0.0"
!endif
!ifndef OUTPUT_EXE
  !define OUTPUT_EXE "dist\wowooai-Setup-${wowooai_VERSION}.exe"
!endif

Name "wowooai Desktop"
OutFile "${OUTPUT_EXE}"
InstallDir "$LOCALAPPDATA\wowooai"
InstallDirRegKey HKCU "Software\wowooai" "InstallPath"
RequestExecutionLevel user

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "SimpChinese"

; Pass /DUNPACKED=full_path from build_win.ps1 so path works when cwd != repo root
!ifndef UNPACKED
  !define UNPACKED "dist\win-unpacked"
!endif

!define UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\wowooai"

Section "wowooai Desktop" SEC01
  SetOutPath "$INSTDIR"
  File /r "${UNPACKED}\*.*"
  WriteRegStr HKCU "Software\wowooai" "InstallPath" "$INSTDIR"
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  ; Main shortcut - uses VBS to hide console window
  CreateShortcut "$SMPROGRAMS\wowooai Desktop.lnk" "$INSTDIR\wowooai Desktop.vbs" "" "$INSTDIR\icon.ico" 0
  CreateShortcut "$DESKTOP\wowooai Desktop.lnk" "$INSTDIR\wowooai Desktop.vbs" "" "$INSTDIR\icon.ico" 0

  ; Debug shortcut - shows console window for troubleshooting
  CreateShortcut "$SMPROGRAMS\wowooai Desktop (Debug).lnk" "$INSTDIR\wowooai Desktop (Debug).bat" "" "$INSTDIR\icon.ico" 0

  ; Add/Remove Programs entry — DisplayIcon makes Settings/Control Panel
  ; show the brand icon instead of a blank/default placeholder.
  WriteRegStr HKCU "${UNINST_KEY}" "DisplayName" "wowooai Desktop"
  WriteRegStr HKCU "${UNINST_KEY}" "DisplayVersion" "${wowooai_VERSION}"
  WriteRegStr HKCU "${UNINST_KEY}" "Publisher" "wowooai"
  WriteRegStr HKCU "${UNINST_KEY}" "InstallLocation" "$INSTDIR"
  WriteRegStr HKCU "${UNINST_KEY}" "DisplayIcon" "$INSTDIR\icon.ico,0"
  WriteRegStr HKCU "${UNINST_KEY}" "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegDWORD HKCU "${UNINST_KEY}" "NoModify" 1
  WriteRegDWORD HKCU "${UNINST_KEY}" "NoRepair" 1
SectionEnd

Section "Uninstall"
  Delete "$SMPROGRAMS\wowooai Desktop.lnk"
  Delete "$SMPROGRAMS\wowooai Desktop (Debug).lnk"
  Delete "$DESKTOP\wowooai Desktop.lnk"
  RMDir /r "$INSTDIR"
  DeleteRegKey HKCU "Software\wowooai"
  DeleteRegKey HKCU "${UNINST_KEY}"
SectionEnd
