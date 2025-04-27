extends Node

@export var platformManager : PlatformManager

var ticksToRun = 18*60
var currentTick = 0
var physicsErrorMessages = []

func _ready():
	test_SpawnStartPlatform()
	test_GetTotalPixelWidth()
	test_SpawnPlatform()
	test_GetPlatformDataForPrediction()
	test_Reset()
	
	platformManager.Reset()

#IT6
func _physics_process(delta):
	if platformManager.get_child_count() > 3:
		physicsErrorMessages.append("[color=red]> platform unloading failed at %s[/color]" % [currentTick])
	if platformManager.get_child_count() < 2:
		physicsErrorMessages.append("[color=red]> platform creation failed at %s[/color]" % [currentTick])
	
	currentTick += 1
	if ticksToRun == currentTick:
		var expectedScore = 0.2/60*ticksToRun + 0.5
		var roundedPlatformScore = snapped(platformManager.speed, 0.01)
		if expectedScore != roundedPlatformScore:
			physicsErrorMessages.append("[color=red]> expected speed = %s but got %s[/color]" % [expectedScore, roundedPlatformScore])

		PrintResults(physicsErrorMessages, "test_physics_process (IT6)")
		set_physics_process(false)
		platformManager.set_physics_process(false)

func PrintResults(errorMessages, testName):
	if errorMessages.is_empty():
		print_rich("PlatformTester: %s [color=green]PASSED[/color]" % [testName])
	else:
		print_rich("PlatformTester: %s [color=red]FAILED[/color]" % [testName])
		for message in errorMessages:
			print_rich(message)

#IT1
func test_SpawnStartPlatform():
	var childCount = platformManager.get_child_count()
	
	platformManager.SpawnStartPlatform()
	var newChildCount = platformManager.get_child_count()
	var newPlatform = platformManager.get_children().front()
	
	var errorMessages = []
	if childCount >= newChildCount:
		errorMessages.append("[color=red]> assertion %s < %s failed[/color]" % [childCount, newChildCount])
	if newPlatform.position != Vector2(0,0):
		errorMessages.append("[color=red]> assertion %s == %s failed[/color]" % [newPlatform.position, Vector2(0,0)])
	if newPlatform.GetTotalPixelWidth() != platformManager.startPlatformTotalPixelWidth:
		errorMessages.append("[color=red]> assertion %s == %s failed[/color]" % [newPlatform.GetTotalPixelWidth(), platformManager.startPlatformTotalPixelWidth])
	
	PrintResults(errorMessages, "test_SpawnStartPlatform (IT1)")
	
#IT2
func test_GetTotalPixelWidth():
	var platform = platformManager.get_children().front()
	var expectedResult = platform.tileWidth * platform.pixelWidthPerTile
	
	var returnedWidth = platform.GetTotalPixelWidth()
	
	var errorMessages = []
	if returnedWidth != expectedResult:
		errorMessages.append("[color=red]> expected %s but got %s[/color]" % [expectedResult, returnedWidth])
		
	PrintResults(errorMessages, "test_GetTotalPixelWidth (IT2)")

#IT3	
func test_SpawnPlatform():
	var childCount = platformManager.get_child_count()
	
	platformManager.SpawnPlatform(0,0)
	var newChildCount = platformManager.get_child_count()
	var newPlatform = platformManager.get_children().back()
	var expectedPosition = Vector2(newPlatform.GetTotalPixelWidth()/2, 0)
	
	var errorMessages = []
	if childCount >= newChildCount:
		errorMessages.append("[color=red]> assertion %s < %s failed[/color]" % [childCount, newChildCount])
	if newPlatform.position != expectedPosition:
		errorMessages.append("[color=red]> assertion %s == %s failed[/color]" % [newPlatform.position, expectedPosition])
	if newPlatform.GetTotalPixelWidth() != platformManager.spawnDelay:
		errorMessages.append("[color=red]> assertion %s == %s failed[/color]" % [newPlatform.GetTotalPixelWidth(), platformManager.startPlatformTotalPixelWidth])
	
	PrintResults(errorMessages, "test_SpawnPlatform (IT3)")
	
#IT4
func test_GetPlatformDataForPrediction():
	var platformCells = platformManager.zeroCellArray.duplicate(true)
	for y in range(len(platformCells)):
		if y <= 11:
			continue
		for x in range(len(platformCells[y])):
			platformCells[y][x] = 1

	var platformCells1D = []
	for cellArr in platformCells:
		for cell in cellArr:
			platformCells1D.append(cell)
	
	var returnedCells = platformManager.GetPlatformDataForPrediction()
	
	var errorMessages = []
	for cell in range(len(platformCells1D)):
		if platformCells1D[cell] != returnedCells[cell]:
			errorMessages.append("[color=red]> value at %s is incorrect[/color]" % [cell])
			
	PrintResults(errorMessages, "test_GetPlatformDataForPrediction (IT4)")

#IT5
func test_Reset():
	platformManager.Reset()
	
	var errorMessages = []
	if not platformManager.is_physics_processing():
		errorMessages.append("[color=red]> physics processes didn't start[/color]")
	if platformManager.get_child_count() > 1:
		errorMessages.append("[color=red]> platforms didn't unload correctly[/color]")
	if platformManager.get_child_count() < 1:
		errorMessages.append("[color=red]> start platform was not spawned[/color]")
	if platformManager.spawnDelay != 0:
		errorMessages.append("[color=red]> spawn delay was not reset[/color]")
	if platformManager.speed != 0.5:
		errorMessages.append("[color=red]> platform speed was not reset[/color]")
	if platformManager.nextPlatform != 0:
		errorMessages.append("[color=red]> next platform was not reset[/color]")
		
	PrintResults(errorMessages, "test_Reset (IT5)")
