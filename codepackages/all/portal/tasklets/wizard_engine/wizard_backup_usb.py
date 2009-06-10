
__tags__=('wizard',)
__author__='qlayer'
__priority__=99

def main(q,i,params,tags):
    USB_CONNECTED = False 
    USB_NO_STUB = False 
    USB_NO_ZFS = False 
    USB_NO_FS = True
    ALL_AUTO = True
    servers = {"EXCHANGE": "MS Exchange Server Employees", "AD": "MS Domain Controller", "SQLPROD": "MS SQL Server Production", "SQLDEV": "MS SQL Server Development"}
    smartClients = {"SC_BILLGATES": "Smart client of Bill Gates", "SC_STEVEJOBS": "Smart client of Steve Jobs", "SC_RECEPTION": "Smart client reception"} 
    disks = {"DISK1": "Disk 1", "DISK2": "Disk 2", "DISK3": "Disk 3"}
    diskStubs = {"DISK1": ("EXCHANGE", "SC_BILLGATES", "SC_STEVEJOBS"), "DISK2": ("AD", "SQLPROD"), "DISK3": ("SQLDEV", "SC_RECEPTION")}
    def _dayOfWeek():
      # day of the week of a given date
      # date.weekday() returns 0 for Monday and so on, so pick the string from a list
      from datetime import date
      dayofWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
      return dayofWeek[date.weekday(date.today())]      

    # STEP 1: Inform the end-user about the purpose of this wizard
    q.gui.dialog.message('This wizard will guide you through the process of creating offline backups to USB disks.')
    q.gui.dialog.showProgress(0, 10, 1)
    # STEP 2: Ask the customer if the USB drives are connected to the active appliance
    q.gui.dialog.message('Before this wizard can continue, the set of USB drives which will hold the backups for today (%s) must be connected to the appliance node.'%_dayOfWeek())
    yesNo = q.gui.dialog.askYesNo('Are the correct USB drives connected')
    if yesNo=='False':
        q.gui.dialog.message('Please connect the correct USB drives first and restart this wizard afterwards.')
        return 
    q.gui.dialog.showProgress(0,10,2)
    # STEP 3: Validate if the USB drives are connected
    # @@TODO: In this step, the wizard should check if USB drives are available on the appliance node
    if not USB_CONNECTED:
        q.gui.dialog.message('No USB drives were detected on the appliance node! Please connect the correct USB drives first and restart this wizard afterwards.')
        return   
    # STEP 4: Read stub information from USB drives
    # @@TODO: Try to read the backup stub from the USB drives. This stub will contain information about which server were backuped to the USB disk.
    #         If some disk contains an other filesystem or a disk is not formatted yet, ask the end-user if we can continue
    if USB_NO_ZFS:
        q.gui.dialog.message('Disk x contains an other filesystem then the one needed by this wizard!')
        q.gui.dialog.message('Continuing this wizard WILL ERASE ALL DATA ON THIS DISK!')
        yesNo = q.gui.dialog.askYesNo('Are you sure you want to continue')
        if yesNo=='False':
            q.gui.dialog.message('Please disconnect USB disk x from the appliance and restart this wizard afterwards.')
            return
    if USB_NO_FS:
        q.gui.dialog.message('A new USB disk was detected. This disk will be formatted automatically once this wizard completes successfully.')
    q.gui.dialog.showProgress(0,10,3)
    # STEP 5: Go over all USB disks and let the customer decide which servers should be backup on which disk
    # @@TODO: Add following logic:
    #         * Make sure that defaults work for selections
    #         * When showing list of smart clients or servers, if already selected, show for which disk
    #         * Inform user when selecting machines which are already backuped on other disk
    progress = 3
    for disk in disks.iterkeys():
        q.gui.dialog.message('Please select the machines to backup to %s'%disks[disk])
        selection = {}
        for machine in diskStubs[disk]:
            if machine in servers:
                selection[machine] = servers[machine]
            elif machine in smartClients:
                selection[machine] = smartClients[machine]

        q.gui.dialog.message('Following machines were backuped to this disk during the previous backup cycle:')
        message = ''
        for s in selection.iterkeys(): message = "%s%s\n"%(message,selection[s])
        q.gui.dialog.message(message)
        yesNo = q.gui.dialog.askYesNo('Would you like to edit this selection')
        if yesNo=='True':
            ALL_AUTO = False
            fullList = servers.copy()
            fullList.update(smartClients)
            selection = q.gui.dialog.askChoiceMultiple('Please make your selection', fullList, selection)
        progress = progress + 1
        q.gui.dialog.showProgress(0,10,progress)
    # STEP 6: If all stubs for all disks where detected automatically and customer didn't make any changes, ask customer to automate this
    # @@TODO: Will result in activating a policy for backups to USB
    if ALL_AUTO:
        q.gui.dialog.message('This wizard detected that you didn\'t made any changes.')
        q.gui.dialog.message('Exporting backups to external USB devices can be automated.')
        q.gui.dialog.message('When you attach the correct USB devices to the appliance before midnight every day, the process can be automated')
        yesNo = q.gui.dialog.askYesNo('Would you like to automate this process in the future')
    # STEP 7: All done, inform the customer of the next steps
    q.gui.dialog.message('This wizard now has all required information. You can follow the progress of the backups process in the Job Activity Window.')
    q.gui.dialog.message('Once the export is done, the backup overview page will be updated and an e-mail will be send to the administrator.')

def match(q,i,params,tags):
    return True
