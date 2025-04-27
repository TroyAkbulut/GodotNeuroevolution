extends Node

var levels : Array[LevelData]
var mainScene : Node2D
var loadedLevel : Level

func UnloadLevel() -> void:
	if is_instance_valid(loadedLevel):
		self.loadedLevel.queue_free()
		
	self.loadedLevel = null
	
func LoadLevel(levelID : int) -> void:
	print("loading " + str(levelID))
	self.UnloadLevel()
	
	var levelData = GetLevelData(levelID)
	if not levelData:
		return

	var levelRes := load(levelData.path)
	if levelRes:
		self.loadedLevel = levelRes.instantiate()
		self.mainScene.add_child(self.loadedLevel)
	else:
		print("failed to load level")

func GetLevelData(levelID : int) -> LevelData:
	var levelData : LevelData
	for level in self.levels:
		if level.levelID == levelID:
			levelData = level
			break
	return levelData
