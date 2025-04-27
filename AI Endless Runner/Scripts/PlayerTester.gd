extends Node

@export var playerManager: PlayerManager

var ticksToRun = 1*60
var currentTick = 0
var physicsErrorMessages = []

# Called when the node enters the scene tree for the first time.
func _ready():
	test_SpawnPlayer()
	test_OnDeath()
	test_StartPlayers()
	test_NormalisePlayerCoords()
	test_GetScoresAndRemovePlayers()
	
	for i in range(3):
		playerManager.SpawnPlayer(i)
	
	playerManager.StartPlayers()

#IT12
func _physics_process(delta):
	var moves = []
	var jsonConverter = JSON.new()
	for player in playerManager.players:
		var moveDict = {"agentID": player.playerID, "moves": [player.playerID]}
		var moveString = JSON.stringify(moveDict)
		jsonConverter.parse(moveString)
		moves.append(jsonConverter.data)
	
	for moveData in moves:
		playerManager.DoPlayerMove(moveData)
		
	currentTick += 1
	if currentTick == ticksToRun:
		for player in playerManager.players:
			if player.playerID == playerManager.MOVE_LEFT and player.position.x > -300:
				physicsErrorMessages.append("[color=red]> expected at least 300 units left, actual %s[/color]" % [player.position.x*-1])
			if player.playerID == playerManager.MOVE_RIGHT and player.position.x < 200:
				physicsErrorMessages.append("[color=red]> expected at least 200 units right, actual %s[/color]" % [player.position.x])
			if player.playerID == playerManager.MOVE_JUMP and player.is_on_floor():
				physicsErrorMessages.append("[color=red]> player is not airborne[/color]")
			if player.playerID == playerManager.MOVE_JUMP and player.position.x > -40:
				physicsErrorMessages.append("[color=red]> player was not correctly affected by platform movement[/color]")
				
			player.set_physics_process(false)
		set_physics_process(false)
		PrintResults(physicsErrorMessages, "test_physics_process (IT12)")

func PrintResults(errorMessages, testName):
	if errorMessages.is_empty():
		print_rich("PlayerTester: %s [color=green]PASSED[/color]" % [testName])
	else:
		print_rich("PlayerTester: %s [color=red]FAILED[/color]" % [testName])
		for message in errorMessages:
			print_rich(message)

#IT7
func test_SpawnPlayer():
	var newPlayerID = 1
	var childCount = playerManager.get_child_count()
	
	playerManager.SpawnPlayer(newPlayerID)
	var newChildCount = playerManager.get_child_count()
	
	var errorMessages = []
	if newChildCount <= childCount:
		errorMessages.append("[color=red]> assertion %s < %s failed[/color]" % [childCount, newChildCount])
	if newChildCount != len(playerManager.players):
		errorMessages.append("[color=red]> new player was not stored[/color]")
	
	var newPlayer: Player = playerManager.players.back()
	
	if newPlayer.playerID != newPlayerID:
		errorMessages.append("[color=red]> player id was incorrectly set (expected %s, got %s)[/color]" % [newPlayerID, newPlayer.playerID])
	if newPlayer.is_physics_processing():
		errorMessages.append("[color=red]> player's physics processes were not stopped[/color]")
		
	PrintResults(errorMessages, "test_SpawnPlayer (IT7)")

#IT8
func test_OnDeath():
	var newPlayerID = 2
	playerManager.SpawnPlayer(newPlayerID)
	var player: Player = playerManager.players.back()
	player.set_physics_process(true)
	
	player.OnDeath()
	
	var errorMessages = []
	if player.is_physics_processing():
		errorMessages.append("[color=red]> player's physics processes were not stopped[/color]")
	if player.alive:
		errorMessages.append("[color=red]> player is still considered alive[/color]")
	if player.finalScore <= 0:
		errorMessages.append("[color=red]> player fitness was not set[/color]")
		
	PrintResults(errorMessages, "test_OnDeath (IT8)")

#IT9
func test_StartPlayers():
	playerManager.StartPlayers()
	
	var errorMessages = []
	for player in playerManager.players:
		if not player.is_physics_processing():
			errorMessages.append("[color=red]> player %s's physics processes were not started[/color]" % [player.playerID])
			player.set_physics_process(false)
	
	PrintResults(errorMessages, "test_StartPlayers (IT9)")

#IT10
func test_NormalisePlayerCoords():
	var result = playerManager.NormalisePlayerCoords(playerManager.players.back())
	
	var errorMessages = []
	if result["x"] != 0.5:
		errorMessages.append("[color=red]> normalised x coordinate expected %s but got %s[/color]" % [0.5, result["x"]])
	if result["y"] != 0.5:
		errorMessages.append("[color=red]> normalised y coordinate expected %s but got %s[/color]" % [0.5, result["x"]])
		
	PrintResults(errorMessages, "test_NormalisePlayerCoords (IT10)")

#IT11
func test_GetScoresAndRemovePlayers():
	var numPlayers = len(playerManager.players)
	for player in playerManager.players:
		player.OnDeath()
	
	var result = playerManager.GetScoresAndRemovePlayers()
	
	var errorMessages = []
	if len(result) != numPlayers:
		errorMessages.append("[color=red]> incorrect number of players were returned (expected %s, got %s)[/color]" % [numPlayers, len(result)])
	for playerData in result:
		if playerData["score"] <= 0:
			errorMessages.append("[color=red]> player %s's score was incorrectly set (%s)[/color]" % [playerData["playerID"], playerData["score"]])
			
	PrintResults(errorMessages, "test_GetScoresAndRemovePlayers (IT11)")
