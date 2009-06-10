__tags__=('wizard',)
__author__='qlayer'
__priority__=99

def main(q,i,params,tags):
    MODE_KIOSK = False
    smartClientImages = {'imagesc01':'Image creation smart client01 - Windows XP SP2', 'imagesc02':'Image creation smart client02 - Windows Vista SP1'}
    smartUserImages = {'amcloud':'Adam MacCloud - Windows XP', 'sjobs':'Steve Jobs - Windows Vista'}

    def _askName():
        # @@TODO: Put regex validation for characters + length 
        name = q.gui.dialog.askString('Please enter name')
        return name
    def _askModel():
        # @@TODO: Warning, chaning the model can lead to incompatible golden images in case of KIOSK smart client!
        smartNodeModels = {"BASE18":"Base Model 1.8", "BASE20":"Base Model 2.0"}  
        model = q.gui.dialog.askChoice('Please select the model', smartNodeModels)
        return model
    def _askMode():
        # @@TODO: When mode changes, explain end user + when switching to KIOSK, ask for golden image
        smartNodeTypes = {"KIOSK":"Kiosk mode", "USER":"User authentication mode"} 
        mode = q.gui.dialog.askChoice('Please select the mode', smartNodeTypes, "USER")
        return mode
    def _askGoldenImage():
        # @@TODO: When smart client is non-KIOSK smart client, ask to switch to this mode before choosing golden image
        goldenimages = ('Windows XP SP2', 'Windows Vista SP1', 'Window XP SP2 with Office 2007', 'Windows Vista SP1 with Office 2007')
        goldenimage = q.gui.dialog.askChoice('Select the type of smart client', goldenimages)
        return goldenimage
    def _updateNode(mac, name, model, mode, goldenimage):
        # @@TODO: Update user in the model + if necessary provision other smart client image 
        return

    # STEP 1: Inform the end-user about the purpose of this wizard
    q.gui.dialog.message('This wizard will guide you through the process of creating a new golden image')
    q.gui.dialog.showProgress(0,10,1)
    # STEP 2: Ask to start from smart client in Kiosk or user golden image
    q.gui.dialog.message('A new golden image can be created from:')
    q.gui.dialog.message('** Copy of a smart client node running in Kiosk mode')
    q.gui.dialog.message('** Copy of a smart client user\'s image')
    type = q.gui.dialog.askChoice('Please make your selection', {'KIOSK':'Smart client in Kiosk mode', 'USER':'Copy of an user image'})
    q.gui.dialog.showProgress(0,10,2)
    # STEP 3: Based on the user's choice, ask for the image to start from 
    if type=='KIOSK':
        user = q.gui.dialog.askChoice('Select smart client node to use as source', smartClientImages)
    else:
        smartClient = q.gui.dialog.askChoice('Select the user image to use as source', smartUserImages)

    q.gui.dialog.showProgress(0,10,3)
    # STEP 4: Ask for the name for this new golden image
    name = q.gui.dialog.askString('Please provide the name for this new golden image')
    q.gui.dialog.showProgress(0,10,7)
    q.gui.dialog.message('Creating a new golden image might take a minute or two')
    yesNo = q.gui.dialog.askYesNo('Start the creation of this new golden image')
    if yesNo=='False':
        q.gui.dialog.message('Golden image creation was aborted!')
        return
    q.gui.dialog.message('The new golden image is being created.\nYou can follow the progress in the Job Activities window.')
    q.gui.dialog.message('Once the job completed successfully new smart clients can be provisioned from this new golden image.')
    q.gui.dialog.showProgress(0,10, 10)

def match(q,i,params,tags):
    return True
