$credential = Get-Credential -Message "Enter your outlook email credentials:"

$TestParams = @{

    From = "$((gwmi Win32_ComputerSystem).Model) <$($credential.UserName)>"
    To = "You <$($credential.UserName)>"
    Subject = 'Notification Service Started'
    Body = "`nEmail notification service on $((gwmi Win32_ComputerSystem).Model) has started.`n`nTime: $(Get-Date)`n"
    SMTPServer = 'smtp-mail.outlook.com'
    Port = 587
    UseSsl = $true
    Credential = $credential

}

Send-MailMessage @TestParams -ErrorAction Stop

$size = (Get-Item "$($HOME)\Documents\GitHub\Medium-Articles-Data-Analysis\Medium_Data.csv").length

while(1) {

    Start-Sleep -s 90
    
    if($size -eq (Get-Item "$($HOME)\Documents\GitHub\Medium-Articles-Data-Analysis\Medium_Data.csv").length) {

                    
        $MailParams = @{

            From = "$((gwmi Win32_ComputerSystem).Model) <$($credential.UserName)>"
            To = "You <$($credential.UserName)>"
            Subject = 'Data Collection Ended'
            Body = "`nData collection on $((gwmi Win32_ComputerSystem).Model) has ended.`n`nTime: $(Get-Date)`n"
            SMTPServer = 'smtp-mail.outlook.com'
            Port = 587
            UseSsl = $true
            Credential = $credential

        }

        Send-MailMessage @MailParams -ErrorAction Stop

        break
            
    } else {

        $size = (Get-Item "$($HOME)\Documents\GitHub\Medium-Articles-Data-Analysis\Medium_Data.csv").length

    }

}