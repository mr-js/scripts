>!>^0::
    File = gamma-new.bin
    If !GetGammaRamp(File)
        MsgBox, Ошибка GetGammaRamp
Return


>!>^3::
    File = gamma-max.bin
    If !SetGammaRamp(File)
        MsgBox, Ошибка SetGammaRamp

Return

>!>^2::
    File = gamma-med.bin
    If !SetGammaRamp(File)
        MsgBox, Ошибка SetGammaRamp

Return

>!>^1::
    File = gamma-min.bin
    If !SetGammaRamp(File)
        MsgBox, Ошибка SetGammaRamp
Return


; =========================== Функции ==============================

GetGammaRamp(FileName)
{
    Static gamma, gammaSize := 256 * 6
    If (!gamma)
        VarSetCapacity(gamma, gammaSize)
    hdcScreen := DllCall("GetDC", "ptr", 0, "ptr")
    Ret := DllCall("GetDeviceGammaRamp", "ptr", hdcScreen, "ptr", &gamma)
    DllCall("ReleaseDC", "ptr", 0, "ptr", hdcScreen)
    If (!Ret)
        Return False
    If !(File := FileOpen(FileName, "w"))
        Return False
    File.Pos := 0
    File.RawWrite(&gamma, gammaSize)
    File.Close()
    Return True
}

SetGammaRamp(FileName)
{
    Static gamma, gammaSize := 256 * 6
    If (!gamma)
        VarSetCapacity(gamma, gammaSize)
    If !(File := FileOpen(FileName, "r"))
        Return False
    File.Pos := 0
    File.RawRead(&gamma, gammaSize)
    File.Close()
    hdcScreen := DllCall("GetDC", "ptr", 0, "ptr")
    Ret := DllCall("SetDeviceGammaRamp", "ptr", hdcScreen, "ptr", &gamma)
    DllCall("ReleaseDC", "ptr", 0, "ptr", hdcScreen)
    Return Ret? True:False
}