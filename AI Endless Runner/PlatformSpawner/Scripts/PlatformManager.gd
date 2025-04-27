extends Node2D
class_name PlatformManager

@export var spawnerPath : String = "res://PlatformSpawner"

var platforms = []
var speed : float = 0.5
var spawnDelay : float = 0
var startPlatformTotalPixelWidth : int
var zeroCellArray : Array[Array]
var nextPlatform = 0


func _ready():
	var platformFolder := DirAccess.open(spawnerPath + "/Platforms")
	if platformFolder == null:
		print("Failed to open platform directory")
		
	platformFolder.list_dir_begin()
	var fileName = platformFolder.get_next()
	while fileName != "":
		if fileName.ends_with(".remap"):
			fileName = fileName.replace(".remap", "")
		if fileName != "PlatformLayout_Start.tscn":
			platforms.append(load(platformFolder.get_current_dir() + "/" + fileName))
		fileName = platformFolder.get_next()
		
	for y in range(0,24):
		var arr : Array[int] = []
		for x in range(0,44):
			arr.append(0)
		zeroCellArray.append(arr)

	self.set_physics_process(false)

func _physics_process(delta):
	spawnDelay -= speed
	if spawnDelay <= 0:
		#start platform should be the size of the screen so this spawns a platform at the edge of the screen
		SpawnPlatform(startPlatformTotalPixelWidth/2, 0)
	
	else:
		for platform in self.get_children():
			if platform.position.x < -platform.GetTotalPixelWidth():
				platform.queue_free()
			platform.position.x -= speed
		
	speed += 0.2/60

func Reset():
	for platform in self.get_children():
		self.remove_child(platform)
		platform.queue_free()
	
	spawnDelay = 0
	speed = 0.5
	nextPlatform = 0
	SpawnStartPlatform()
	self.set_physics_process(true)

func SpawnStartPlatform():
	var startingPlatform = load(spawnerPath + "/Platforms/PlatformLayout_Start.tscn").instantiate()
	startPlatformTotalPixelWidth = startingPlatform.GetTotalPixelWidth()
	startingPlatform.position = Vector2(0,0)
	self.add_child(startingPlatform)

func SpawnPlatform(x : int, y : int):
	var platform = platforms[randi() % len(platforms)].instantiate()
	#var platform = platforms[nextPlatform].instantiate()
	var platformWidth = platform.GetTotalPixelWidth()
	
	spawnDelay = platformWidth
	platform.position = Vector2(x + platformWidth/2, y)
	self.add_child(platform)
	
	nextPlatform += 1
	if nextPlatform == len(platforms):
		nextPlatform = 0

func GetPlatformDataForPrediction():
	var platformCells : Array = []
	for platform in self.get_children():
		platformCells += GetCellsOnScreen(platform)
		
	return OnehotEncodePlatformCells(platformCells)

func GetCellsOnScreen(platform : TileMap):
	var xOffset : int  = int(platform.position.x) / platform.pixelWidthPerTile
	var platformCells : Array[Vector2i] = platform.get_used_cells(0)
	
	var adjustedPlatformCells : Array = platformCells.map(func(cell): return Vector2i(cell.x + xOffset, cell.y))
	var isOnScreen : Callable = func(cell): return (-22 <= cell.x and cell.x <= 21) and (-12 <= cell.y and cell.y <= 11)
	var platformCellsOnScreen : Array = adjustedPlatformCells.filter(isOnScreen)
	
	return platformCellsOnScreen

func OnehotEncodePlatformCells(cells : Array):
	var onehotCells2D : Array[Array] = zeroCellArray.duplicate(true)
	for cell in cells:
		onehotCells2D[cell.y+12][cell.x+22] = 1

	var onehotCells1D : Array[int]
	for cellArr in onehotCells2D:
		for cell in cellArr:
			onehotCells1D.append(cell)
	
	return onehotCells1D
