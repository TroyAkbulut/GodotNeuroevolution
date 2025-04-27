extends Node2D
class_name PlayerManager

@export var playerScenePath : String = "res://Player.tscn"
@export var platformManager : PlatformManager
@export var maxX : int
@export var maxY : int
@export var minX: int
@export var minY : int

var playerScene
var players : Array[Player] = []

const MOVE_LEFT : int = 0
const MOVE_RIGHT : int = 1
const MOVE_JUMP : int = 2

func _ready():
	playerScene = load(playerScenePath)

func SpawnPlayer(playerID : int = -1):
	var newPlayer : Player = playerScene.instantiate()
	newPlayer.playerID = playerID
	newPlayer.playerManager = self
	players.append(newPlayer)
	self.add_child(newPlayer)
	newPlayer.set_physics_process(false)
	
func StartPlayers():
	for player in players:
		player.set_physics_process(true)
		
func DoPlayerMove(moveData):
	var curPlayer: Player
	for player in players:
		if player.playerID == moveData.agentID:
			curPlayer = player
			break
	
	for move in moveData.moves:
		if move == MOVE_LEFT:
			curPlayer.Left()
		elif move == MOVE_RIGHT:
			curPlayer.Right()
		elif move == MOVE_JUMP:
			curPlayer.Jump()
	curPlayer.move_and_slide()
	
func GetScoresAndRemovePlayers() -> Array:
	var playerScores = []
	for player in players:
		var playerData	: Dictionary = {
			"playerID": player.playerID,
			"score": player.finalScore,
		}
		playerScores.append(playerData)
		remove_child(player)
		player.queue_free()
		
	players = []
	return playerScores
	
func NormalisePlayerCoords(player : Player) -> Dictionary:
	var x : float = player.position.x
	var y : float = player.position.y
	
	x = (x-minX)/(maxX-minX)
	y = (y-minY)/(maxY-minY)

	return {"x":x, "y":y}
