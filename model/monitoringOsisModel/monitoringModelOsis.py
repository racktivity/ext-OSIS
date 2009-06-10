from pymonkey.baseclasses.BaseEnumeration import BaseEnumeration
from osis import model

#It is assumend that the OSIS framework has the concept of GUID and VERSION for each of the object in the model. This GUID is assumed to be constant across versions of the object. 
#Hence this will be used for references like ParentGUID.


#@todo 1 shiva: create ea model from this file and put ea file with right layout in this directory

class BoxTypeE(BaseEnumeration):
	@classmethod
	def _initItems(cls):
		cls.registerItem('Cpu')
		cls.registerItem('Storage')
		cls.registerItem('Management')
		cls.finishItemRegistration()

class Fan(model.Model):
	description = model.String(thrift_id=1)
	speed       = model.Integer(thrift_id=2)

class MotherBoard(model.Model):
	model       = model.String(thrift_id=1)
	fans        = model.List(model.Object(Fan),thrift_id=2)

class OperationalStatusE(BaseEnumeration):
	@classmethod
	def _initItems(cls):
		cls.registerItem('Online')
		cls.registerItem('Offline')
		cls.finishItemRegistration()

class Cpu(model.Model):
	deviceId    = model.String(thrift_id=1)
	description = model.String(thrift_id=2)
	modelName   = model.String(thrift_id=3)
	speedMhz    = model.Integer(thrift_id=4)
	noOfCores   = model.Integer(thrift_id=5)
	operStatus  = model.Enumeration(OperationalStatusE, thrift_id=6) #Online/Offline

class MemoryTypeE(BaseEnumeration):
	@classmethod
	def _initItems(cls):
		cls.registerItem('SD')
		cls.registerItem('DDR')
		cls.registerItem('DDR2')
		cls.registerItem('DDR3')
		cls.finishItemRegistration()

class Memory(model.Model):
	deviceId    = model.String(thrift_id=1)
	description = model.String(thrift_id=2)
	modelName   = model.String(thrift_id=3)
	type        = model.Enumeration(MemoryTypeE, thrift_id=4)      #SD, DDR, etc.
	capacityMB  = model.Integer(thrift_id=5)

class DisktypeE(BaseEnumeration):
	@classmethod
	def _initItems(cls):
		cls.registerItem('SATA')
		cls.registerItem('IDE')
		cls.registerItem('SCSI')
		cls.registerItem('ISCSI')
		cls.finishItemRegistration()

class Disk(model.Model):
	deviceId    = model.String(thrift_id=1)
	description = model.String(thrift_id=2)
	modelName   = model.String(thrift_id=3)
	type        = model.Enumeration(DisktypeE, thrift_id=4)       # SATA, IDE, SCSI, etc.
	capacityGB  = model.Integer(thrift_id=5)

class NicTypeE(BaseEnumeration):
	@classmethod
	def _initItems(cls):
		cls.registerItem('Ethernet')
		cls.registerItem('Virtual')
		cls.registerItem('LoopBack')
		cls.registerItem('Infiniband')
		cls.finishItemRegistration()

class Nic(model.Model):
	mac       = model.String(thrift_id=1)
	modelName = model.String(thrift_id=2)
	type      = model.Enumeration(NicTypeE, thrift_id=3)          #ethernet, infiniband, Virtualetc.
	speedMBps = model.Integer(thrift_id=4)

class Peripheral(model.Model):
	type = model.String(thrift_id=1)
	description = model.String(thrift_id=2)

class VMachineTypeE(BaseEnumeration):
	@classmethod
	def _initItems(cls):
		cls.registerItem('VirtualBox')
		cls.registerItem('Xen')
		cls.registerItem('VmPlayer')
		cls.registerItem('Qemu')
		cls.finishItemRegistration()

class VirtualDiskTypeE(BaseEnumeration):
	@classmethod
	def _initItems(cls):
		cls.registerItem('Iscsi')
		cls.registerItem('Zvol')
		cls.registerItem('File')
		cls.registerItem('Disk')
		cls.finishItemRegistration()

class VirtualDisk(model.Model):
	imagePath   = model.String(thrift_id=1)
	type        = model.Enumeration(VirtualDiskTypeE, thrift_id=2)#ISCSI,ZVOL,File

class CpuUtilization(model.Model):
	numberOfCores = model.Integer(thrift_id=1)
	currentUsage  = model.Float(thrift_id=2)
	AvgLastHour   = model.Float(thrift_id=3)

class FilesystemTypeE(BaseEnumeration):
	@classmethod
	def _initItems(cls):
		cls.registerItem('ZFS')
		cls.registerItem('UFS')
		cls.registerItem('ext3')
		cls.registerItem('NTFS')
		cls.finishItemRegistration()

class Partition(model.Model):
	deviceId   = model.String(thrift_id=1)
	capacityGB = model.Integer(thrift_id=2)
	usedGB     = model.Integer(thrift_id=3)
	filesystem = model.Enumeration(FilesystemTypeE, thrift_id=4) #swap, ext2, ext3, NTFS, Reiser, etc.

class ZFS(model.Model):
	zfsPool = model.List(model.Object(storagePool), thrift_id=1)

class storagePool(model.Model):
	name        = model.String(thrift_id=1)
	capacityGB  = model.Integer(thrift_id=2)
	usedGB      = model.Integer(thrift_id=3)
	operStatus  = model.Enumeration(OperationalStatusE, thrift_id=4) #Online, etc
	vdevs       = model.List(model.Object(Zvdev), thrift_id=5)
	zstorage    = model.List(model.Object(ZStorage), thrift_id=6)

class ZStorageTypeE(BaseEnumeration):
	@classmethod
	def _initItems(cls):
		cls.registerItem('ZVOL')
		cls.registerItem('ZFSFilesystem')
		cls.finishItemRegistration()

class ZStorage(model.Model):
	name          = model.String(thrift_id=1)
	type          = model.Enumeration(ZStorageTypeE, thrift_id=2) #Zvol, filesystem
	reservationGB = model.Integer(thrift_id=3)
	quotaGB       = model.Integer(thrift_id=4)
	usedGB        = model.Integer(thrift_id=5)

class AdminStateE(BaseEnumeration):
	@classmethod
	def _initItems(cls):
		cls.registerItem('Activated')
		cls.registerItem('DeActivated')
		cls.finishItemRegistration()

class NetworkConnectivity(model.Model):
	type          = model.Enumeration(NicTypeE, thrift_id=1)          #ethernet, infiniband, etc.
	isVirtual     = model.Boolean(thrift_id=2)       #crossbow
	speedMBps     = model.Integer(thrift_id=3)
	mac           = model.String(thrift_id=4)
	ipAddresses   = model.List(model.Object(IPAddress),thrift_id=5)
	adminstatus   = model.Enumeration(AdminStateE, thrift_id=6)          #Activated/DeActivated
	operstatus    = model.Enumeration(OperationalStatusE, thrift_id=7)          #Up/Down
	packetsin     = model.Integer(thrift_id=8)
	packetsout    = model.Integer(thrift_id=9)
	errpacketsin  = model.Integer(thrift_id=10)
	errpacketsout = model.Integer(thrift_id=11)

class IPTypeE(BaseEnumeration):
	@classmethod
	def _initItems(cls):
		cls.registerItem('IPV4')
		cls.registerItem('IPV6')
		cls.finishItemRegistration()

class IPAddress(model.Model):
	ipAddress      = model.String(thrift_id=1)
	type           = model.Enumeration(IPTypeE, thrift_id=2)
	defaultGateway = model.String(thrift_id=3)
	subnetMask     = model.String(thrift_id=4)
	isDHCP         = model.Boolean(thrift_id=5)

class Process(model.Model):
	processName        = model.String(thrift_id=1)
	processID          = model.Integer(thrift_id=2)
	processThreadCount = model.Integer(thrift_id=3)
	processParentID    = model.Integer(thrift_id=4)
	processCPU         = model.Float(thrift_id=5)
	processMemory      = model.Integer(thrift_id=6)
	processPageFaults  = model.Integer(thrift_id=7)
	processPeakMemory  = model.Integer(thrift_id=8)

class EventTypeE(BaseEnumeration):
	@classmethod
	def _initItems(cls):
		cls.registerItem('Process')
		cls.registerItem('HardWare')
		cls.registerItem('VirtualMachine')
		cls.finishItemRegistration()

class SourceTypeE(BaseEnumeration):
	@classmethod
	def _initItems(cls):
		cls.registerItem('Syslog')
		cls.registerItem('PyMonkey')
		cls.finishItemRegistration()

class Device(model.RootObjectModel):
	modelName 	       = model.String(thrift_id=1)
	role      	       = model.Enumeration(BoxTypeE, thrift_id=2)            #(CPU/Storage/Management)
	motherBoard            = model.Objet(MotherBoard,thrift_id=3)
	cpus                   = model.List(model.Object(Cpu),thrift_id=4)
	memory                 = model.List(model.Object(Memory),thrift_id=5)
	disks                  = model.List(model.Object(Disk),thrift_id=6)
	nics                   = model.List(model.Object(Nic),thrift_id=7)
	peripherals            = model.List(model.Object(Peripheral),thrift_id=8)
	pcicards               = model.List(model.Object(Peripheral),thrift_id=9)
	totalAvailableMemoryMB = model.Integer(thrift_id=10)
	totaldiskCapacityGB    = model.Integer(thrift_id=11)

class PMachine(model.RooObjectModel):
	timestamp            = model.Integer(thrift_id=1)
	availableHypervisors = model.Enumeration(VMachineTypeE, thrift_id=2) #VBox, Zen, Vmplayer, etc.
	swap                 = model.List(model.Object(Partition), thift_id=3)
	zfs                  = model.Object(ZFS, thrift_id = 4)
	diskPartitions       = model.List(model.Object(Partition), thrift_id=5)
	netConnectivity      = model.List(model.Object(NetworkConnectivity), thrift_id=6)
	processes            = model.List(model.Object(Process), thrift_id=7)

class Event(model.RootObjectModel):
	name              = model.String(thrift_id=1)
	ID                = model.Integer(thrift_id=2)
	affectedObject    = model.Integer(thrift_id=3)
	originalseverity  = model.Integer(thrift_id=4)
	perceivedseverity = model.Integer(thrift_id=5)
	timestamp         = model.Integer(thrift_id=6)
	description       = model.Integer(thrift_id=7)
	eventType         = model.Enumeration(EventTypeE, thrift_id=8)#Process,Hw,Virtual Machine
	source            = model.Enumeration(SourceTypeE, thrift_id=9)#syslog,pymonkey log

class VMachine(model.RootObjectModel):
	type             = model.Enumeration(VMachineTypeE, thrift_id=1)       #VBox, Zen, Vmplayer, etc.
	memoryCapacityMB = model.Integer(thrift_id=2)
	cpuUsage         = model.Object(CpuUtilization, thrift_id=3)
	vnics            = model.List(model.Object(Nic),thrift_id=4)
	vdisks           = model.Object(VirtualDisk, thrift_id=5)

class Temperature(model.RootObjectModel):
	description                   = model.String(thrift_id=1)
	currentTemperatureCelcius     = model.Float(thrift_id=2)
	avgTemperatureLastHourCelcius = model.Float(thrift_id=3)
	timeStamp                     = model.Integer(thrift_id=4)
	parentGUID                    = model.GUID(thrift_id=5) #MotherBoard, hardDisk, etc

