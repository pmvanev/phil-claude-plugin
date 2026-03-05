# Claude Code Stop notification — toast + chime
# Uses WinRT toast API (reliable on Windows 10/11) and system notification sound

# Play the Windows notification sound through audio device
(New-Object Media.SoundPlayer "$env:SystemRoot\Media\Windows Notify Messaging.wav").PlaySync()

# Load WinRT toast assemblies
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom, ContentType = WindowsRuntime] | Out-Null

$template = @"
<toast duration="short">
  <visual>
    <binding template="ToastGeneric">
      <text>Claude Code</text>
      <text>Finished working</text>
    </binding>
  </visual>
</toast>
"@

$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml($template)

$appId = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe'
$toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($appId).Show($toast)
