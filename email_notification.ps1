# Getting Outlook Credentials used for sending and recieving emails
$credentials = Get-Credential -Message "Enter your outlook email credentials:"

# Email parameters used for the startup email
$TestParams = @{

    From = "$((gwmi Win32_ComputerSystem).Model) <$($credentials.UserName)>"
    To = "You <$($credentials.UserName)>"
    Subject = 'Notification Service Started'
    Body = "`nEmail notification service on $((gwmi Win32_ComputerSystem).Model) has started.`n`nTime: $(Get-Date)`n"
    SMTPServer = 'smtp-mail.outlook.com'
    Port = 587
    UseSsl = $true
    Credential = $credentials

}

# Sending Startup email
Send-MailMessage @TestParams -ErrorAction Stop

# Getting the size of "Medium_DAta.csv" file
$size = (Get-Item "$($HOME)\Documents\GitHub\Medium-Articles-Data-Analysis\Medium_Data.csv").length

while(1) {
    
    # Waiting for a certain amount of time.
    Start-Sleep -s 600
        
    # Checking if the data collection is done, by comparing the file size periodically.
    if($size -eq (Get-Item "$($HOME)\Documents\GitHub\Medium-Articles-Data-Analysis\Medium_Data.csv").length) {

                    
        $MailParams = @{

            From = "$((gwmi Win32_ComputerSystem).Model) <$($credentials.UserName)>"
            To = "You <$($credentials.UserName)>"
            Subject = 'Data Collection Ended'
            Body = "`nData collection on $((gwmi Win32_ComputerSystem).Model) has ended.`n`nTime: $(Get-Date)`n"
            SMTPServer = 'smtp-mail.outlook.com'
            Port = 587
            UseSsl = $true
            Credential = $credentials

        }

        Send-MailMessage @MailParams -ErrorAction Stop

        break
            
    } else {

        # If the size has changed, then update the size for the next iteration comparison.
        $size = (Get-Item "$($HOME)\Documents\GitHub\Medium-Articles-Data-Analysis\Medium_Data.csv").length

    }

}